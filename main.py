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
    from config.settings import REPORTS_DIR
    from rankle.core.scanner import RankleScanner
    from rankle.utils.helpers import save_json_file
    from rankle.utils.validators import (
        extract_domain,
        sanitize_filename,
        validate_domain,
    )
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
        help="Save JSON output to reports/ directory.",
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
        # Initialize scanner
        scanner = RankleScanner(domain, verbose=args.verbose)

        # Run comprehensive scan
        results = scanner.run_full_scan()

        # Save JSON report if requested
        if args.output:
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            base_filename = f"rankle_{sanitize_filename(domain)}_{timestamp}"
            json_path = REPORTS_DIR / f"{base_filename}.json"
            if save_json_file(results, json_path):
                print(f"\n📁 JSON saved: {json_path}")

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
