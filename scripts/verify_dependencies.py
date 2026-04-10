#!/usr/bin/env python3
"""
Dependency verification script for Rankle.

Checks that all required dependencies are installed and importable.
"""

import sys
from typing import Any


def check_dependency(
    package_name: str, import_name: str | None = None
) -> dict[str, Any]:
    """
    Check if a dependency is installed and importable.

    Args:
        package_name: Package name as listed in requirements.txt
        import_name: Module name for import (if different from package_name)

    Returns:
        Dictionary with status and version info
    """
    if import_name is None:
        import_name = package_name.replace("-", "_")

    try:
        module = __import__(import_name)
        version = getattr(module, "__version__", "Unknown")
        return {
            "package": package_name,
            "status": "✅ OK",
            "version": version,
            "importable": True,
        }
    except ImportError as e:
        return {
            "package": package_name,
            "status": "❌ MISSING",
            "version": None,
            "importable": False,
            "error": str(e),
        }


def main() -> None:
    """Verify all Rankle dependencies."""
    print("=" * 80)
    print("🔍 Rankle Dependency Verification")
    print("=" * 80)

    # Core production dependencies
    core_deps = [
        ("requests", "requests"),
        ("dnspython", "dns"),
        ("beautifulsoup4", "bs4"),
        ("python-Wappalyzer", "Wappalyzer"),
        ("mmh3", "mmh3"),
    ]

    # Optional dependencies
    optional_deps = [
        ("python-whois", "whois"),
        ("ipwhois", "ipwhois"),
    ]

    # Development dependencies
    dev_deps = [
        ("ruff", "ruff"),
        ("mypy", "mypy"),
        ("pytest", "pytest"),
        ("bandit", "bandit"),
    ]

    print("\n📦 Core Dependencies (Required):")
    print("-" * 80)

    core_results = []
    for package, import_name in core_deps:
        result = check_dependency(package, import_name)
        core_results.append(result)
        status = result["status"]
        version = result.get("version", "Unknown")
        print(f"  {status} {package:25} {version}")

    print("\n📦 Optional Dependencies (Extended features):")
    print("-" * 80)

    optional_results = []
    for package, import_name in optional_deps:
        result = check_dependency(package, import_name)
        optional_results.append(result)
        status = result["status"]
        version = result.get("version", "Unknown")
        print(f"  {status} {package:25} {version}")

    print("\n🔧 Development Dependencies (Optional):")
    print("-" * 80)

    dev_results = []
    for package, import_name in dev_deps:
        result = check_dependency(package, import_name)
        dev_results.append(result)
        status = result["status"]
        version = result.get("version", "Unknown")
        print(f"  {status} {package:25} {version}")

    # Summary
    print("\n" + "=" * 80)
    print("📊 Summary:")
    print("=" * 80)

    core_ok = sum(1 for r in core_results if r["importable"])
    core_total = len(core_results)
    optional_ok = sum(1 for r in optional_results if r["importable"])
    optional_total = len(optional_results)
    dev_ok = sum(1 for r in dev_results if r["importable"])
    dev_total = len(dev_results)

    print(f"  Core Dependencies:     {core_ok}/{core_total} OK")
    print(f"  Optional Dependencies: {optional_ok}/{optional_total} OK")
    print(f"  Dev Dependencies:      {dev_ok}/{dev_total} OK")

    # Check if core dependencies are satisfied
    if core_ok == core_total:
        print("\n✅ All core dependencies are installed!")
        print("   Rankle is ready to run.")

        # Test import of Rankle modules
        print("\n🔬 Testing Rankle module imports...")
        try:
            from rankle import RankleScanner
            from rankle.utils import (
                analyze_favicon,
                analyze_javascript,
                analyze_wordpress,
                fingerprint_error_page,
                map_technology_to_cve_urls,
            )

            print("   ✅ All Rankle modules import successfully")
        except ImportError as e:
            print(f"   ❌ Rankle module import failed: {e}")

        sys.exit(0)
    else:
        print("\n❌ Some core dependencies are missing!")
        print("   Install with: pip install -r requirements.txt")
        print("   Or: pip install -e '.[dev]'")

        # Show missing packages
        missing = [r["package"] for r in core_results if not r["importable"]]
        if missing:
            print(f"\n   Missing packages: {', '.join(missing)}")
            print("\n   Install missing:")
            print(f"   pip install {' '.join(missing)}")

        sys.exit(1)


if __name__ == "__main__":
    main()
