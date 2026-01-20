# Rankle Documentation Directory

This directory contains comprehensive documentation for the Rankle web infrastructure reconnaissance tool.

**Quick Start:** Begin with [index.md](index.md) for complete navigation.

---

## 📚 Documentation Files

### **Core Documentation**

#### [index.md](index.md)
**Purpose:** Main documentation hub with navigation to all resources
**Content:** Overview, quick links, ethical use guidelines
**Audience:** All users
**Status:** ✅ Up-to-date (2026-01-20)

#### [getting-started.md](getting-started.md)
**Purpose:** Installation, usage, and first scan
**Content:** Requirements, installation methods, command-line options, Docker usage
**Audience:** New users
**Status:** ✅ Core content current

#### [architecture.md](architecture.md)
**Purpose:** Technical design and API reference
**Content:** Modular structure, key classes, configuration, adding modules
**Audience:** Developers, contributors
**Status:** ✅ Covers v2.0 architecture

#### [detection-capabilities.md](detection-capabilities.md)
**Purpose:** Feature documentation and integration examples
**Content:** CMS/CDN/WAF detection, technology fingerprinting, integration with Nuclei/Nmap
**Audience:** Security researchers, power users
**Status:** ⚠️ May need v2.0 updates (check enhanced detection coverage)

#### [development.md](development.md)
**Purpose:** Contributing guide and development setup
**Content:** Environment setup, testing, pre-commit hooks, coding standards
**Audience:** Contributors, developers
**Status:** ✅ Current with 2026 best practices

---

### **Advanced Documentation**

#### [TECHNOLOGY_DETECTION_ENHANCEMENT.md](TECHNOLOGY_DETECTION_ENHANCEMENT.md)
**Purpose:** Complete v2.0 enhancement documentation
**Content:**
- 7 new detection modules (favicon hashing, error fingerprinting, JS extraction, WordPress, CVE mapping)
- Before/after comparisons
- API usage examples
- Performance metrics
- Testing results
**Audience:** Developers, security researchers
**Status:** ✅ Comprehensive v2.0 reference (360 lines)
**Created:** 2026-01-20

#### [MYPY_GUIDE.md](MYPY_GUIDE.md)
**Purpose:** Type checking configuration and best practices
**Content:** mypy setup, common errors, Python 3.11+ type hints
**Audience:** Developers
**Status:** ✅ Current with modern Python typing

#### [troubleshooting.md](troubleshooting.md)
**Purpose:** Solutions to common issues and error messages
**Content:**
- Installation problems
- Dependency issues
- Network/connection errors
- DNS resolution failures
- SSL/TLS certificate errors
- Rate limiting & blocking
- Timeout errors
- Detection issues
- Docker-specific problems
- Type checking errors
**Audience:** All users
**Status:** ✅ Comprehensive troubleshooting guide (850+ lines)
**Created:** 2026-01-20

#### [performance-tuning.md](performance-tuning.md)
**Purpose:** Optimize Rankle for speed and efficiency
**Content:**
- Timeout configuration strategies
- Rate limiting tuning
- DNS optimization
- Memory optimization
- Network optimization
- Detection trade-offs (traditional vs. enhanced)
- Batch scanning techniques
- Profiling & benchmarking
**Audience:** Power users, administrators
**Status:** ✅ Complete optimization guide (550+ lines)
**Created:** 2026-01-20

#### [api-usage-examples.md](api-usage-examples.md)
**Purpose:** Use Rankle as a Python library in your projects
**Content:**
- Installation as library
- Module-by-module examples
- Complete integration examples (security audit, inventory, monitoring)
- Custom detection logic
- Error handling
- Async/concurrent usage
- Integration patterns (Flask, Django, Celery)
**Audience:** Developers, integrators
**Status:** ✅ Comprehensive API guide (850+ lines)
**Created:** 2026-01-20

---

### **Examples and Migration**

#### [examples/README.md](examples/README.md)
**Purpose:** Usage examples and code samples
**Content:** Practical demonstrations, integration patterns
**Audience:** Developers integrating Rankle
**Status:** ✅ Active examples

#### [examples/MIGRATION.md](examples/MIGRATION.md)
**Purpose:** Migration guide between versions
**Content:** Breaking changes, upgrade paths, API changes
**Audience:** Existing users upgrading
**Status:** ✅ Covers version transitions

---

## 🗂️ Documentation Organization

### **Root-Level Documentation** (`/`)

These files remain in the repository root for standard GitHub conventions:

- **[README.md](../README.md)** - Project overview, badges, quick start (primary entry point)
- **[CLAUDE.md](../CLAUDE.md)** - Claude Code project instructions (245 lines)
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history following Keep a Changelog format
- **[SECURITY.md](../SECURITY.md)** - Security policy and vulnerability reporting
- **LICENSE** - MIT License

### **Claude Code Configuration** (`/.claude/`)

Configuration files for Claude Code development:

- **[README.md](../.claude/README.md)** - Claude configuration documentation
- **[CODEBASE_MAP.md](../.claude/CODEBASE_MAP.md)** - Token-optimized quick reference (class locations, file purposes)
- **settings.json** - Shared team configuration (tracked)
- **settings.local.json** - Local overrides (not tracked)

### **Utility Scripts** (`/scripts/`)

Documentation for development and diagnostic scripts:

- **[README.md](../scripts/README.md)** - Scripts documentation
  - `demo_enhanced_detection.py` - v2.0 feature demonstration
  - `verify_dependencies.py` - Dependency verification tool

---

## 📊 Documentation Coverage Analysis

### **Well-Covered Areas:**
- ✅ Installation and quick start
- ✅ Architecture and design patterns
- ✅ Development setup and contributing
- ✅ Type checking and code standards
- ✅ Enhanced detection features (v2.0)
- ✅ Claude Code integration

### **Recent Expansions (2026-01-20):**
- ✅ Updated `detection-capabilities.md` with comprehensive v2.0 section (464 lines added)
- ✅ Created `troubleshooting.md` - Complete troubleshooting guide (850+ lines)
- ✅ Created `performance-tuning.md` - Optimization strategies (550+ lines)
- ✅ Created `api-usage-examples.md` - Library usage examples (850+ lines)

---

## 🎯 Documentation Standards

All documentation in this repository follows these standards:

### **Markdown Style:**
- GitHub-flavored Markdown (GFM)
- Code blocks with language identifiers
- Headers use ATX style (`#`, `##`, etc.)
- Lists use consistent markers (- for unordered, 1. for ordered)

### **Content Standards:**
- **Accuracy:** All examples tested and verified
- **Currency:** Dates and versions kept current
- **Completeness:** Covers all user personas (new users, developers, researchers)
- **Clarity:** Technical but accessible language
- **Examples:** Practical, runnable code samples

### **Update Frequency:**
- Major releases: All docs reviewed
- Minor releases: Affected docs updated
- Patches: CHANGELOG.md updated minimum
- Documentation bugs: Fixed immediately

---

## 🔗 External References

Documentation may reference:

- **Official Python Docs:** https://docs.python.org/3/
- **OWASP Testing Guide:** https://owasp.org/www-project-web-security-testing-guide/
- **PortSwigger Research:** https://portswigger.net/research
- **ProjectDiscovery Tools:** https://projectdiscovery.io/
- **Anthropic Claude Code:** https://docs.anthropic.com/claude-code

All external links checked periodically for validity.

---

## 📝 Contributing to Documentation

When contributing documentation:

1. **Follow existing structure** - Match style and formatting of similar docs
2. **Include examples** - Show, don't just tell
3. **Test commands** - Verify all code blocks execute correctly
4. **Update index.md** - Add new docs to navigation
5. **Update this README** - Document new files here
6. **Check links** - Ensure all internal links resolve
7. **Date your work** - Add "Last Updated: YYYY-MM-DD" to major docs

### **Documentation PRs Should Include:**
- The new/modified documentation
- Updated navigation in `index.md`
- Updated entry in this README
- Verification that all links work
- Spell-check and grammar review

---

## 🔍 Finding Documentation

### **I want to...**

- **Install Rankle** → [getting-started.md](getting-started.md)
- **Run my first scan** → [getting-started.md#usage](getting-started.md)
- **Understand the architecture** → [architecture.md](architecture.md)
- **Contribute code** → [development.md](development.md)
- **Use v2.0 enhanced detection** → [TECHNOLOGY_DETECTION_ENHANCEMENT.md](TECHNOLOGY_DETECTION_ENHANCEMENT.md)
- **Fix type errors** → [MYPY_GUIDE.md](MYPY_GUIDE.md)
- **Integrate with other tools** → [detection-capabilities.md](detection-capabilities.md)
- **Configure Claude Code** → [../.claude/README.md](../.claude/README.md)
- **Find code quickly** → [../.claude/CODEBASE_MAP.md](../.claude/CODEBASE_MAP.md)
- **Run utility scripts** → [../scripts/README.md](../scripts/README.md)
- **Report security issues** → [../SECURITY.md](../SECURITY.md)
- **Check version history** → [../CHANGELOG.md](../CHANGELOG.md)

---

## 📈 Documentation Metrics

**Total Documentation:**
- **Lines:** 5,472+ across 15 files
- **Files:** 15 markdown files
- **Directories:** 3 (docs/, .claude/, scripts/)
- **Last Major Update:** 2026-01-20 (v2.0 Enhanced)

**Coverage by Category:**
- User Guides: 30%
- Technical References: 40%
- Development Guides: 20%
- Configuration: 10%

---

**Maintained By:** Rankle Development Team
**Last Updated:** 2026-01-20
**Documentation Version:** 2.0 Enhanced
