#!/usr/bin/env python3
"""
Rankle - Web Infrastructure Reconnaissance Tool
Main entry point with multiple subcommands

100% Open Source - No API keys required
"""

import argparse
import json
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
    from rankle.db.repository import ScanRepository
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nPlease ensure all dependencies are installed:")
    print("  uv sync")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


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


def cmd_scan(args):
    """Scan a domain and output results."""
    domain = extract_domain(args.domain)

    if not validate_domain(domain):
        print(f"❌ Invalid input: Invalid domain format: {args.domain}")
        sys.exit(1)

    backend_type = args.backend
    if args.output and args.backend == OUTPUT_BACKEND:
        backend_type = "json"

    print("=" * 80)
    print("🃏 RANKLE - Web Infrastructure Reconnaissance")
    print("=" * 80)
    print(f"🎯 Target: {domain}")
    print(f"⏰ Timestamp: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📤 Backend: {backend_type}")
    print("=" * 80)

    try:
        if backend_type == "sqlite":
            engine = get_engine(DATABASE_URL.replace("sqlite:///", ""))
            create_all_tables(engine)

        scanner = RankleScanner(domain, verbose=args.verbose)
        start_time = datetime.now(UTC)
        results = scanner.run_full_scan()
        duration_ms = int((datetime.now(UTC) - start_time).total_seconds() * 1000)

        metadata = {
            "domain": domain,
            "scan_type": "full",
            "scanned_at": start_time.isoformat(),
            "duration_ms": duration_ms,
            "status": "completed",
        }

        if backend_type == "console":
            backend = OutputRegistry.get_backend("console")
            backend.write("1", results, metadata)
        elif backend_type == "json":
            backend = OutputRegistry.get_backend("json", output_dir=str(REPORTS_DIR))
            backend.write("1", results, metadata)
        elif backend_type == "sqlite":
            with get_db_session(engine) as session:
                repo = ScanRepository(session)
                scan = repo.create_scan(domain, "full")
                scan_id = scan.id

                formatted_results = {}
                for module_name, module_data in results.items():
                    if isinstance(module_data, dict):
                        formatted_results[module_name] = [module_data]
                    elif isinstance(module_data, list):
                        formatted_results[module_name] = module_data
                    else:
                        formatted_results[module_name] = [{"value": str(module_data)}]

                backend = OutputRegistry.get_backend("sqlite", session=session)
                backend.write(str(scan_id), formatted_results, metadata)
                print(f"✓ Scan #{scan_id} saved to database")

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


def cmd_history(args):
    """Show scan history for a domain."""
    if not validate_domain(args.domain):
        print(f"❌ Invalid domain: {args.domain}")
        sys.exit(1)

    engine = get_engine(DATABASE_URL.replace("sqlite:///", ""))

    with get_db_session(engine) as session:
        repo = ScanRepository(session)
        scans = repo.get_scan_history(args.domain, limit=args.limit)

        if not scans:
            print(f"❌ No scan history for {args.domain}")
            return

        if console and RICH_AVAILABLE:
            table = Table(title=f"Scan History: {args.domain}")
            table.add_column("ID", style="cyan")
            table.add_column("Timestamp", style="magenta")
            table.add_column("Type", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Duration (ms)", style="blue")

            for scan in scans:
                status_color = "green" if scan.status == "completed" else "red"
                table.add_row(
                    str(scan.id),
                    scan.scanned_at.strftime("%Y-%m-%d %H:%M:%S"),
                    scan.scan_type,
                    f"[{status_color}]{scan.status}[/{status_color}]",
                    str(scan.duration_ms or "N/A"),
                )

            console.print(table)
        else:
            print(f"\nScan History for {args.domain}:")
            for scan in scans:
                print(f"  #{scan.id} | {scan.scanned_at} | {scan.scan_type} | {scan.status} | {scan.duration_ms}ms")


def cmd_diff(args):
    """Show differences between last two scans of a domain."""
    if not validate_domain(args.domain):
        print(f"❌ Invalid domain: {args.domain}")
        sys.exit(1)

    engine = get_engine(DATABASE_URL.replace("sqlite:///", ""))

    with get_db_session(engine) as session:
        repo = ScanRepository(session)
        changes = repo.get_dns_changes(args.domain)

        if not changes:
            print(f"No DNS changes found for {args.domain}")
            return

        for change in changes:
            if change["added"]:
                print(f"\n✅ Added ({len(change['added'])} records):")
                for rec in change["added"][:5]:
                    print(f"  + {json.dumps(rec, default=str)}")
                if len(change["added"]) > 5:
                    print(f"  ... and {len(change['added']) - 5} more")

            if change["removed"]:
                print(f"\n❌ Removed ({len(change['removed'])} records):")
                for rec in change["removed"][:5]:
                    print(f"  - {json.dumps(rec, default=str)}")
                if len(change["removed"]) > 5:
                    print(f"  ... and {len(change['removed']) - 5} more")


def cmd_list(args):
    """List all scans in database."""
    engine = get_engine(DATABASE_URL.replace("sqlite:///", ""))

    with get_db_session(engine) as session:
        repo = ScanRepository(session)
        scans = repo.list_all_scans(limit=args.limit)

        if not scans:
            print("❌ No scans found in database")
            return

        if console and RICH_AVAILABLE:
            table = Table(title="All Scans")
            table.add_column("ID", style="cyan")
            table.add_column("Domain", style="green")
            table.add_column("Type", style="yellow")
            table.add_column("Status", style="magenta")
            table.add_column("Timestamp", style="blue")
            table.add_column("Duration (ms)")

            for scan in scans:
                status_color = "green" if scan.status == "completed" else "red"
                table.add_row(
                    str(scan.id),
                    scan.domain,
                    scan.scan_type,
                    f"[{status_color}]{scan.status}[/{status_color}]",
                    scan.scanned_at.strftime("%Y-%m-%d %H:%M:%S"),
                    str(scan.duration_ms or "N/A"),
                )

            console.print(table)
        else:
            print("\nAll Scans:")
            for scan in scans:
                print(f"  #{scan.id} | {scan.domain} | {scan.scan_type} | {scan.status} | {scan.scanned_at}")


def main():
    """Main entry point with subcommand parsing."""
    print_banner()

    parser = argparse.ArgumentParser(
        description="Rankle - Web Infrastructure Reconnaissance Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Subcommands:
  scan       Scan a domain (default if no subcommand given)
  history    Show scan history for a domain
  diff       Show DNS changes between last 2 scans
  list       List all scans in database

Examples:
  uv run python main.py example.com                    # Scan
  uv run python main.py scan example.com --backend sqlite
  uv run python main.py history example.com
  uv run python main.py diff example.com
  uv run python main.py list
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Scan subcommand
    scan_parser = subparsers.add_parser("scan", help="Scan a domain")
    scan_parser.add_argument("domain", help="Domain to scan")
    scan_parser.add_argument("-o", "--output", action="store_true", help="Save JSON output (deprecated)")
    scan_parser.add_argument("--backend", choices=["console", "json", "sqlite"], default=OUTPUT_BACKEND)
    scan_parser.add_argument("-v", "--verbose", action="store_true")
    scan_parser.set_defaults(func=cmd_scan)

    # History subcommand
    history_parser = subparsers.add_parser("history", help="Show scan history")
    history_parser.add_argument("domain", help="Domain to show history for")
    history_parser.add_argument("--limit", type=int, default=10, help="Max scans to show")
    history_parser.set_defaults(func=cmd_history)

    # Diff subcommand
    diff_parser = subparsers.add_parser("diff", help="Show DNS changes")
    diff_parser.add_argument("domain", help="Domain to compare scans")
    diff_parser.set_defaults(func=cmd_diff)

    # List subcommand
    list_parser = subparsers.add_parser("list", help="List all scans")
    list_parser.add_argument("--limit", type=int, default=100, help="Max scans to show")
    list_parser.set_defaults(func=cmd_list)

    # Global options (not on main parser to avoid shadowing subcommand args)
    parser.add_argument("-o", "--output", action="store_true")
    parser.add_argument("--backend", choices=["console", "json", "sqlite"], default=OUTPUT_BACKEND)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--version", action="version", version="Rankle v0.1-alpha")

    args = parser.parse_args()

    # Execute the command if one was selected
    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()
        return None


if __name__ == "__main__":
    main()
