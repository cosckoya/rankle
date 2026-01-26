# Examples Directory Migration

**Date:** January 20, 2026
**Status:** ✅ Complete

---

## Summary

Moved integration examples from `examples/` to `docs/examples/` to eliminate code duplication and establish a single source of truth for documentation.

---

## Changes Made

### 1. Directory Restructure

**Before:**
```
rankle/
├── examples/
│   ├── enhanced_detection_example.py  ❌ Broken (used non-existent API)
│   ├── full_recon_chain.sh
│   ├── nmap_pipeline.sh
│   └── nuclei_pipeline.sh
└── docs/
    ├── getting-started.md
    ├── architecture.md
    └── detection-capabilities.md  (contained duplicate script code)
```

**After:**
```
rankle/
└── docs/
    ├── examples/
    │   ├── README.md               ✅ New comprehensive guide
    │   ├── full_recon_chain.sh     ✅ Moved from examples/
    │   ├── nmap_pipeline.sh        ✅ Moved from examples/
    │   └── nuclei_pipeline.sh      ✅ Moved from examples/
    ├── getting-started.md          ✅ Updated references
    ├── architecture.md             ✅ Updated directory tree
    └── detection-capabilities.md   ✅ Now references scripts, no duplication
```

### 2. Files Deleted

- ❌ `examples/enhanced_detection_example.py` - Broken Python example using non-existent v2.0 API
- ❌ `examples/` directory - Removed entirely

**Reason for deletion:** The Python example taught incorrect API usage:
```python
from rankle import Rankle  # ❌ Wrong - Should be RankleScanner
rankle.detect_technologies_enhanced()  # ❌ Method doesn't exist
```

### 3. Files Created

- ✅ `docs/examples/README.md` (7KB) - Comprehensive guide covering:
  - Script descriptions and usage
  - Tool installation requirements
  - Output structure
  - Customization examples
  - Troubleshooting guide
  - Security and ethics guidelines

### 4. Documentation Updates

**docs/architecture.md:**
- Updated directory structure to show `docs/examples/`
- Added documentation file references

**docs/detection-capabilities.md:**
- Replaced 3 embedded shell scripts (~60 lines each) with links to actual files
- Eliminated code duplication (DRY principle)
- Added workflow descriptions and usage instructions

**docs/getting-started.md:**
- Added reference to `docs/examples/README.md` in "Next Steps" section

### 5. Configuration Updates

**pyproject.toml:**
- Removed Ruff linting rules for `examples/**/*.py` (no longer needed)
- Removed mypy override for `examples.*` module
- Kept exclusion patterns (harmless, won't match anything)

**mypy.ini:**
- Removed `^examples/` from exclude pattern
- Removed `[mypy-examples.*]` override section

---

## Benefits Achieved

### ✅ **Eliminated Code Duplication (DRY Principle)**

**Before:**
- Shell scripts existed in `examples/`
- Identical scripts embedded in `docs/detection-capabilities.md`
- **Problem:** Changes required updates in 2 places
- **Risk:** Documentation divergence (already happening - scripts used `--output both`, docs showed `--output json`)

**After:**
- Single source of truth: `docs/examples/*.sh`
- Documentation references files instead of duplicating content
- **Benefit:** Changes propagate automatically

### ✅ **Removed Broken Examples**

**Before:**
- `enhanced_detection_example.py` taught incorrect API usage
- Would fail immediately if users tried to run it
- **Problem:** Misleading users about v2.0 API

**After:**
- Only working, tested scripts remain
- All examples use correct v2.0 CLI interface

### ✅ **Improved Discoverability**

**Before:**
- Scripts in `examples/` directory
- Minimal documentation
- Users had to read scripts to understand usage

**After:**
- Comprehensive `README.md` with:
  - Installation instructions
  - Usage examples
  - Output descriptions
  - Troubleshooting guide
  - Security guidelines

### ✅ **Better Organization**

**Before:**
- Examples separate from documentation
- Unclear relationship between scripts and docs

**After:**
- Examples integrated with documentation
- Clear navigation path: docs → examples
- Logical grouping of related content

---

## Verification

### Type Checking
```bash
$ mypy rankle/ --config-file=pyproject.toml
Success: no issues found in 24 source files
```

### Scripts Location
```bash
$ ls -lah docs/examples/
-rwxrwxr-x 1 cosckoya cosckoya 1.9K full_recon_chain.sh
-rwxrwxr-x 1 cosckoya cosckoya  970 nmap_pipeline.sh
-rwxrwxr-x 1 cosckoya cosckoya 1.1K nuclei_pipeline.sh
-rw-rw-r-- 1 cosckoya cosckoya 6.9K README.md
```

### Old Directory Removed
```bash
$ test -d examples/ && echo "EXISTS" || echo "DELETED"
DELETED
```

---

## Impact Assessment

### No Breaking Changes

- ✅ Python package structure unchanged (`rankle/` remains the same)
- ✅ CLI interface unchanged
- ✅ API unchanged
- ✅ All tests still pass
- ✅ Mypy still clean

### User Experience Improvements

- 📈 **Easier to find examples** - Now under docs/ with other guides
- 📈 **Better documentation** - Comprehensive README explains usage
- 📈 **No confusion** - Broken Python example removed
- 📈 **Maintainability** - Single source of truth for scripts

### Developer Experience Improvements

- 🛠️ **Reduced maintenance** - Update scripts in one place only
- 🛠️ **No sync issues** - Documentation always matches actual scripts
- 🛠️ **Cleaner configuration** - Removed unnecessary Ruff/mypy rules

---

## Migration Checklist

- [x] Move shell scripts to `docs/examples/`
- [x] Delete broken Python example
- [x] Remove old `examples/` directory
- [x] Create comprehensive `docs/examples/README.md`
- [x] Update `docs/architecture.md` directory structure
- [x] Update `docs/detection-capabilities.md` to reference scripts
- [x] Update `docs/getting-started.md` to reference examples
- [x] Remove Ruff rules for Python examples from `pyproject.toml`
- [x] Remove mypy overrides from `pyproject.toml`
- [x] Remove mypy exclusions from `mypy.ini`
- [x] Verify mypy still passes
- [x] Verify scripts are executable
- [x] Document migration in MIGRATION.md

---

## Future Considerations

### Python Example Restoration (Optional)

If Python API examples are needed in the future:

1. **Use correct v2.0 API:**
```python
from rankle import RankleScanner

scanner = RankleScanner("example.com")
results = scanner.run_full_scan()
print(f"Found {len(results['subdomains'])} subdomains")
```

2. **Add proper documentation:**
   - Explain each API method
   - Show expected output
   - Include error handling

3. **Test before committing:**
   - Verify examples work with current API
   - Run mypy on examples
   - Test with multiple Python versions

### Script Enhancements

Consider adding:
- Exit status codes for CI integration
- JSON output mode for parsing
- Configurable rate limiting
- Proxy support
- Authentication options

---

## References

- [Architecture Documentation](../architecture.md)
- [Detection Capabilities](../detection-capabilities.md)
- [Getting Started Guide](../getting-started.md)
- [Examples README](README.md)

---

**Migration performed by:** Research Assistant + Python Architect
**Verified by:** Mypy type checker
**Status:** Production ready ✅
