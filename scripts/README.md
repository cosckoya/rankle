# Rankle Utility Scripts

This directory contains utility and demonstration scripts for the Rankle project.

## Available Scripts

### `demo_enhanced_detection.py`

**Purpose:** Demonstration of enhanced technology detection capabilities (v2.0)

**Description:**
Shows off the new technology detection features including:

- Wappalyzer integration (3000+ signatures)
- Favicon hashing (mmh3)
- Error page fingerprinting
- JavaScript endpoint extraction
- WordPress plugin/theme detection
- CVE vulnerability mapping

**Usage:**

```bash
# Activate virtual environment first
source .venv/bin/activate

# Test with default domain (example.com)
python scripts/demo_enhanced_detection.py

# Test with custom domain
python scripts/demo_enhanced_detection.py yourdomain.com
```

**Output:**

- Console: Pretty-printed detection results
- File: `{domain}_enhanced_detection.json` (detailed JSON results)

---

### `verify_dependencies.py`

**Purpose:** Dependency verification and diagnostic tool

**Description:**
Checks that all required dependencies are installed and importable. Useful for:

- Post-installation verification
- Troubleshooting import errors
- CI/CD environment validation
- Development environment setup

**Usage:**

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run verification
python scripts/verify_dependencies.py
```

**Output:**

- ✅ Core dependencies: 5 packages (required)
- 📦 Optional dependencies: 2 packages (WHOIS features)
- 🔧 Dev dependencies: 4+ packages (testing, linting)
- Exit code 0 if all core dependencies OK, 1 otherwise

**Categories Checked:**

- **Core:** requests, dnspython, beautifulsoup4, python-Wappalyzer, mmh3
- **Optional:** python-whois, ipwhois
- **Dev:** ruff, mypy, pytest, bandit

---

## Development Guidelines

### Adding New Scripts

Scripts in this directory should:

1. **Be executable** - `chmod +x script.py`
2. **Include shebang** - `#!/usr/bin/env python3`
3. **Have docstrings** - Module and function documentation
4. **Accept arguments** - Use `argparse` for command-line options
5. **Use virtual environment** - Assume `.venv` activation
6. **Be documented here** - Add entry to this README

### Script Template

```python
#!/usr/bin/env python3
"""
Brief description of script purpose.

This script provides [functionality] for [use case].
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rankle import RankleScanner


def main() -> None:
    """Main entry point."""
    # Implementation here
    pass


if __name__ == "__main__":
    main()
```

---

## Script Categories

### Demonstration Scripts

- `demo_enhanced_detection.py` - Show v2.0 detection features

### Diagnostic Scripts

- `verify_dependencies.py` - Dependency verification

### (Future) Build Scripts

- TBD: Build automation, release packaging

### (Future) Benchmark Scripts

- TBD: Performance benchmarking, comparison tests

---

## Notes

- All scripts assume Python 3.11+ environment
- Scripts are NOT part of the installed package
- Scripts are for development/testing/demonstration only
- For production usage, use `main.py` or import `rankle` package

---

**Last Updated:** 2026-01-20
**Maintained By:** Rankle Development Team
