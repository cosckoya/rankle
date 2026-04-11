#!/usr/bin/env python3
"""
Rankle - Web Infrastructure Reconnaissance Tool
Main entry point

Named after Rankle, Master of Pranks from Magic: The Gathering

A comprehensive web infrastructure analyzer:
- DNS enumeration and configuration
- Subdomain discovery via Certificate Transparency
- Technology stack detection (CMS, frameworks, libraries)
- TLS/SSL certificate analysis
- HTTP security headers audit
- CDN and WAF detection
- Geolocation and hosting provider information
- WHOIS lookup

100% Open Source - No API keys required
"""

import argparse
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path


# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from config.settings import REPORTS_DIR, OUTPUT_BACKEND, DATABASE_URL
    from rankle.core.scanner import RankleScanner
    from rankle.utils.helpers import save_json_file
    from rankle.utils.validators import (
        extract_domain,
        sanitize_filename,
        validate_domain,
    )
    from rankle.output.registry import OutputRegistry
    from rankle.db.engine import get_engine, create_all_tables, get_db_session
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nPlease ensure all dependencies are installed:")
    print("  uv sync")
    sys.exit(1)


def print_banner():
    """Print Rankle banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ██████╗  █████╗ ███╗   ██╗██╗  ██╗██╗     ███████╗                     ║
║   ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██║     ██╔════╝                     ║
║   ██████╔╝███████║██╔██╗ ██║█████╔╝ ██║     █████╗                       ║
║   ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██║     ██╔══╝                       ║
║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗███████╗███████╗                     ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚══════╝                     ║
║                                                                           ║
║              Web Infrastructure Reconnaissance Tool                       ║
║          Named after Rankle, Master of Pranks (MTG)                      ║
║                                                                           ║
║                      100% Open Source - No API Keys                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Rankle - Web Infrastructure Reconnaissance Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python main.py example.com           # Scan and print to terminal
  uv run python main.py example.com -o json   # Save JSON to reports/
  uv run python main.py example.com -v        # Verbose output

For more information, visit: https://github.com/javicosvml/rankle
        """,
    )

    parser.add_argument(
        "domain",
        help="Domain or URL to analyze (e.g., example.com or https://example.com)",
    )

    parser.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="Save JSON output to reports/ directory (deprecated, use --backend json).",
    )

    parser.add_argument(
        "--backend",
        choices=["console", "json", "sqlite"],
        default=OUTPUT_BACKEND,
        help=f"Output backend. Default: {OUTPUT_BACKEND}",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    parser.add_argument("--version", action="version", version="Rankle v1.0.0")

    return parser.parse_args()


def main():
    """Main entry point"""
    print_banner()

    args = parse_arguments()

    # Extract and validate domain
    domain = extract_domain(args.domain)

    if not validate_domain(domain):
        print(f"❌ Invalid input: Invalid domain format: {args.domain}")
        sys.exit(1)

    # Print scan info
    print("=" * 80)
    print("🃏 RANKLE - Web Infrastructure Reconnaissance")
    print("=" * 80)
    print(f"🎯 Target: {domain}")
    print(f"⏰ Timestamp: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    try:
        # Determine output backend
        # Priority: --backend flag > -o flag > OUTPUT_BACKEND env var > console default
        backend_type = args.backend
        if args.output and args.backend == OUTPUT_BACKEND:
            # -o flag was used and no explicit --backend, so use json
            backend_type = "json"

        # Initialize database if using SQLite backend
        scan_id = None
        if backend_type == "sqlite":
            engine = get_engine(DATABASE_URL.replace("sqlite:///", ""))
            create_all_tables(engine)

        # Initialize scanner
        scanner = RankleScanner(domain, verbose=args.verbose)

        # Run comprehensive scan
        start_time = datetime.now(UTC)
        results = scanner.run_full_scan()
        duration_ms = int((datetime.now(UTC) - start_time).total_seconds() * 1000)

        # Prepare metadata for output backend
        metadata = {
            "domain": domain,
            "scan_type": "full",
            "scanned_at": start_time.isoformat(),
            "duration_ms": duration_ms,
            "status": "completed",
        }

        # Write results using selected backend
        try:
            if backend_type == "console":
                backend = OutputRegistry.get_backend("console")
                backend.write("1", results, metadata)
            elif backend_type == "json":
                backend = OutputRegistry.get_backend("json", output_dir=str(REPORTS_DIR))
                backend.write("1", results, metadata)
            elif backend_type == "sqlite":
                with get_db_session(engine) as session:
                    from rankle.db.repository import ScanRepository
                    repo = ScanRepository(session)
                    scan = repo.create_scan(domain, "full")
                    scan_id = scan.id

                    # Convert results to list-of-dicts format
                    formatted_results = {}
                    for module_name, module_data in results.items():
                        if isinstance(module_data, dict):
                            formatted_results[module_name] = [module_data]
                        elif isinstance(module_data, list):
                            formatted_results[module_name] = module_data
                        else:
                            formatted_results[module_name] = [{"value": str(module_data)}]

                    backend = OutputRegistry.get_backend("sqlite", session=session)
                    metadata["status"] = "completed"
                    backend.write(str(scan_id), formatted_results, metadata)
                    print(f"✓ Scan #{scan_id} saved to database")
        except Exception as e:
            print(f"⚠️  Error writing output: {e}")
            if args.verbose:
                traceback.print_exc()

        print("\n" + "=" * 80)
        print("✅ Scan completed successfully!")
        print("=" * 80)

    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error during scan: {e!s}")
        if args.verbose:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
