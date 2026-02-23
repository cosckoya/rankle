# Rankle - Claude Code Documentation

**Purpose:** Complete reference for Claude Code when working with this repository.

**Version:** 2.0 (Enhanced Technology Detection)
**Last Updated:** 2026-02-19
**Maintained By:** Claude Code + Human collaboration

---

**LANGUAGE POLICY: Always respond in English, regardless of user's language.**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Available Skills](#available-skills)
3. [Quick Command Reference](#quick-command-reference)
4. [Architecture & Codebase Map](#architecture--codebase-map)
5. [Code Standards](#code-standards)
6. [Security Guidelines](#security-guidelines)
7. [Research Protocol](#research-protocol)
8. [Claude Code Configuration](#claude-code-configuration)
9. [Dependencies](#dependencies)

---

## Project Overview

**Rankle** - Web infrastructure reconnaissance tool for authorized security testing. Named after "Rankle, Master of Pranks" from Magic: The Gathering.

### Key Features

- **DNS Enumeration:** A/AAAA/MX/NS/TXT/SOA/CNAME records
- **Subdomain Discovery:** Certificate Transparency (crt.sh)
- **Enhanced Technology Detection:** 3000+ technologies via Wappalyzer (CMS, frameworks, CDN, WAF, libraries)
- **Advanced Fingerprinting:** Favicon hashing (mmh3), error page analysis, JS endpoint extraction
- **WordPress Detection:** Plugin and theme enumeration (60+ plugins, 20+ themes)
- **CVE Vulnerability Mapping:** Automatic CVE search URL generation for detected technologies
- **Cloud Provider Detection:** AWS, Azure, GCP, DigitalOcean, OVH, Hetzner
- **Origin Infrastructure Discovery:** Behind WAF/CDN (passive techniques only)
- **TLS/SSL Certificate Analysis**
- **HTTP Fingerprinting:** Methods, API endpoints, exposed files

### Ethical Use

**CRITICAL:** All methods are passive reconnaissance. For authorized testing only.
- ONLY passive reconnaissance techniques (public DNS/SSL/CT logs)
- NO active attacks or unauthorized access attempts
- Origin discovery uses only publicly accessible information
- Document the source of each reconnaissance technique

---

## Available Skills

This project uses Claude Code's global skill system (17 global skills). All skills work across projects.

### Task Orchestration

**For complex or multi-domain tasks:**
- `/task-router` ⭐ - Intelligent task orchestrator
  - Analyzes tasks, routes to appropriate skill(s)
  - Creates execution plans, coordinates multi-skill workflows
  - **Production Mode:** "make rankle production ready"
    - 5 quality gates (Code, Security, Testing, Documentation, Pre-production)
    - Automatic rollback plan generation
    - 2-4 hour full production workflow
    - Guide: `~/.claude/skills/PRODUCTION_WORKFLOW_GUIDE.md`

### Most Relevant Skills for Rankle

**Development:**
- `/python-architect` - Python 3.11+ standards, type hints, Ruff formatting
- `/test-automator` - Pytest tests, pre-commit hooks, CI/CD pipelines
- `/docker-specialist` - Container optimization and security

**Security:**
- `/security-scanner-expert` - Security reconnaissance tool development, detection logic
- `/recon-researcher` - Research latest OSINT/reconnaissance techniques
- `/pattern-updater` - Manage detection signatures (config/patterns.py, tech_signatures.json)
- `/security-auditor` - OWASP Top 10 review, bandit scans, input validation

**Integration & Validation:**
- `/api-integrator` - Integration scripts for Nuclei, Nmap, httpx
- `/config-validator` - Validate pyproject.toml, settings.py, patterns.py

**Documentation:**
- `/changelog-maintainer` - Maintain CHANGELOG.md (Keep a Changelog format)
- `/cheatsheet-generator` - Create command reference sheets

**See all skills:** `~/.claude/skills/README.md` or `find ~/.claude/skills/ -name SKILL.md`

---

## Quick Command Reference

```bash
# Run scans
python main.py example.com                    # Basic scan
python main.py example.com --output json      # JSON output
python main.py example.com --verbose          # Verbose mode

# Development
python3 -m venv venv && source venv/bin/activate
pip install -e ".[dev]"                       # Install with dev dependencies
pre-commit install                            # Enable git hooks

# Quality checks
ruff check . --fix && ruff format .           # Lint and format
mypy rankle/                                  # Type checking
bandit -c pyproject.toml -r rankle/           # Security scan
pytest -v --cov=rankle                        # Tests with coverage

# Docker
docker build -t rankle .
docker run --rm rankle example.com
```

---

## Architecture & Codebase Map

### Directory Structure

```
rankle/
├── main.py                      # CLI entry point (argparse, output formatters)
├── rankle/
│   ├── __init__.py             # Package exports: RankleScanner
│   ├── core/                   # Core orchestration
│   │   ├── scanner.py          # RankleScanner class (795 lines) - main orchestrator
│   │   └── session.py          # SessionManager (195 lines) - HTTP client with retry
│   ├── modules/                # Reconnaissance modules
│   │   ├── dns.py              # DNS queries (191 lines)
│   │   ├── ssl.py              # TLS/SSL analysis (402 lines)
│   │   ├── subdomains.py       # Subdomain discovery (543 lines) - crt.sh integration
│   │   ├── whois.py            # WHOIS lookups (480 lines)
│   │   ├── geolocation.py      # IP geolocation (202 lines)
│   │   ├── http_fingerprint.py # HTTP fingerprinting (573 lines)
│   │   └── security_headers.py # Security header auditing (513 lines)
│   ├── detectors/              # Detection engines
│   │   ├── technology.py       # Technology detection (1179 lines) ⚠️ LARGE
│   │   ├── cdn.py              # CDN detection (549 lines)
│   │   ├── waf.py              # WAF detection (496 lines)
│   │   └── origin.py           # Origin IP discovery (447 lines)
│   ├── utils/                  # Utility functions
│   │   ├── validators.py       # Input validation (160 lines)
│   │   ├── confidence.py       # Confidence scoring (148 lines)
│   │   ├── rate_limiter.py     # Rate limiting (323 lines)
│   │   ├── favicon_hash.py     # Favicon fingerprinting (NEW v2.0)
│   │   ├── error_fingerprint.py # Error page analysis (NEW v2.0)
│   │   ├── js_extractor.py     # JS endpoint extraction (NEW v2.0)
│   │   ├── wordpress_plugins.py # WordPress detection (NEW v2.0)
│   │   └── cve_mapper.py       # CVE mapping (NEW v2.0)
│   └── reports/                # Output formatting
│       ├── text_report.py      # Human-readable output
│       └── json_report.py      # Machine-readable output
├── config/                     # Configuration files
│   ├── settings.py             # Global configuration
│   ├── patterns.py             # Cloud/ASN patterns
│   └── tech_signatures.json    # Technology signatures database
├── scripts/                    # Utility and demo scripts
│   ├── demo_enhanced_detection.py  # v2.0 feature demonstration
│   ├── verify_dependencies.py      # Dependency verification tool
│   └── README.md                   # Scripts documentation
├── tests/                      # Unit tests (pytest)
└── docs/                       # Documentation
    └── TECHNOLOGY_DETECTION_ENHANCEMENT.md  # v2.0 enhancement details
```

### Key Classes and Locations

#### Core Orchestration
- **RankleScanner** (`rankle/core/scanner.py:15`)
  - Lines: 795
  - Purpose: Main orchestrator, lazy module initialization
  - Key Methods: `run_full_scan()`, `run_basic_scan()`

- **SessionManager** (`rankle/core/session.py`)
  - Lines: 195
  - Purpose: HTTP client with retry logic and connection pooling
  - Key Methods: `get()`, `head()`, `options()`

#### Detection Engines
- **TechnologyDetector** (`rankle/detectors/technology.py:647`)
  - Lines: 1179 total (class starts at 647)
  - Purpose: Multi-technique technology detection
  - Key Methods:
    - `detect()` - Traditional detection (headers, cookies, HTML)
    - `detect_enhanced()` - NEW v2.0: Wappalyzer, favicon, error pages, JS analysis
  - Detection Techniques:
    1. HTML pattern matching (800+ signatures)
    2. HTTP headers analysis
    3. Cookie analysis
    4. Meta tags parsing
    5. JavaScript globals detection
    6. Wappalyzer (3000+ signatures) - NEW v2.0
    7. Favicon hashing (mmh3) - NEW v2.0
    8. Error page fingerprinting - NEW v2.0
    9. JavaScript endpoint extraction - NEW v2.0
    10. WordPress plugin/theme detection - NEW v2.0

- **CDNDetector** (`rankle/detectors/cdn.py`) - 549 lines, 20+ CDN providers
- **WAFDetector** (`rankle/detectors/waf.py`) - 496 lines, 15+ WAF solutions
- **OriginDiscovery** (`rankle/detectors/origin.py`) - 447 lines, find origin IPs behind CDN/WAF

#### Utility Modules (NEW in v2.0)
- **Favicon Hashing** (`rankle/utils/favicon_hash.py`) - mmh3 hash, 25+ known favicon hashes
- **Error Fingerprinting** (`rankle/utils/error_fingerprint.py`) - Django, Laravel, Rails, Flask, FastAPI
- **JS Extractor** (`rankle/utils/js_extractor.py`) - LinkFinder-style, React, Vue, Angular, Next.js
- **WordPress Detection** (`rankle/utils/wordpress_plugins.py`) - 60+ plugins, 20+ themes
- **CVE Mapper** (`rankle/utils/cve_mapper.py`) - CPE identifiers, NVD, MITRE, CVEDetails, Vulners

### Common Tasks and File Locations

| Task | Primary File | Secondary Files |
|------|-------------|----------------|
| Add Technology Signatures | config/tech_signatures.json | rankle/detectors/technology.py |
| Add CDN/WAF Detection | detectors/cdn.py or detectors/waf.py | - |
| Modify HTTP Behavior | rankle/core/session.py | config/settings.py |
| Input Validation | rankle/utils/validators.py | - |
| DNS Enumeration | modules/dns.py | config/settings.py (DNS_SERVERS) |
| Technology Detection | detectors/technology.py | config/tech_signatures.json, utils/* |
| Origin Discovery | detectors/origin.py | modules/dns.py, detectors/cdn.py |
| Output Formatting | reports/* | main.py |

### Code Patterns

**Lazy Initialization (Scanner):**
```python
@property
def module_name(self) -> ModuleClass:
    if self._module_name is None:
        self._module_name = ModuleClass(self.domain)
    return self._module_name
```

**Detection Results Structure:**
```python
{
    "detected": bool,
    "technologies": [
        {
            "name": str,
            "category": str,
            "confidence": float,  # 0.0-1.0
            "version": str | None,
            "evidence": list[dict]
        }
    ]
}
```

**Confidence Scoring:**
- 0.9-1.0: High confidence (explicit signature match)
- 0.6-0.8: Medium confidence (multiple weak signals)
- 0.3-0.5: Low confidence (single weak signal)
- < 0.3: Filtered out (below MINIMUM_DETECTION_CONFIDENCE)

### Token Optimization Tips

1. For technology detection changes, read `technology.py` in chunks (file is 1179 lines)
2. Scanner orchestration: Start with `scanner.py:15-100` for class definition
3. For adding modules: Read `scanner.py:700-795` for integration patterns
4. Configuration changes: Read `config/settings.py` (usually <200 lines)

---

## Code Standards

### Python 3.11+ Requirements

- **Built-in generics:** `dict[str, Any]` not `Dict[str, Any]`
- **Union syntax:** `str | None` not `Optional[str]`
- **Google-style docstrings**
- **Type hints required** on all public functions
- **Ruff** for linting/formatting (replaces Black, isort, flake8)

### Pre-commit Hooks Enforce

1. Trailing whitespace, EOF fixes, YAML/JSON/TOML validation
2. Black formatting (88 char line length)
3. isort import sorting
4. Ruff linting
5. Bandit security checks
6. mypy type checking

### Design Patterns

- Lazy initialization for module instances
- Context managers for resource cleanup (`with` statement)
- Single responsibility per module
- Guard clauses for early returns
- Centralized configuration in `config/settings.py`

### Adding New Detection Modules

**3-Step Integration:**
1. Create module with `analyze()` method returning `dict[str, Any]`
2. Add lazy property to `RankleScanner` class (`rankle/core/scanner.py`)
3. Integrate in `run_full_scan()` method

**Pattern:** See existing detectors in `rankle/detectors/` for examples. All use lazy initialization via `@property` decorators.

---

## Security Guidelines

### Input Validation

- All domains validated via `validate_domain()` (regex-based)
- URLs sanitized via `extract_domain()`
- Filenames sanitized via `sanitize_filename()` (removes `<>:"/\|?*`)

### Safe Practices

- Never use `shell=True` with subprocess
- All HTTP requests have timeout controls
- Rate limiting between requests (configurable in settings)
- Realistic User-Agent to avoid detection

### Ethical Scanning Constraints

- **ONLY** passive reconnaissance techniques (public DNS/SSL/CT logs)
- **NO** active attacks or unauthorized access attempts
- Origin discovery uses only publicly accessible information
- Document the source of each reconnaissance technique

---

## Research Protocol

### When to Research

**MANDATORY: Research modern techniques before implementing new features.**

- Adding new detection modules (CDN, WAF, CMS)
- Improving origin discovery methods
- Adding subdomain enumeration sources
- Enhancing technology fingerprinting

### Research Sources

Use WebFetch/WebSearch for:
- PortSwigger Web Security Blog, OWASP Testing Guide
- Bug bounty methodology searches ("passive reconnaissance 2026")
- Security tool documentation (Amass, Subfinder, httpx, nuclei)
- GitHub Security Research topics

### Research Workflow

1. Search latest techniques
2. Read documentation
3. Implement ONLY passive methods
4. Update config/patterns.py
5. Document source in code comments

### Ethical Constraint

**ONLY passive reconnaissance. No active attacks. All data from public sources (DNS, SSL, CT logs).**

---

## Claude Code Configuration

### Configuration Files

This directory (`.claude/`) contains Claude Code configuration files following 2026 best practices.

#### `settings.json` (Tracked in Git)
Shared team configuration:
- Project metadata
- Permissions for common development tasks
- Context optimization strategies
- Development tooling preferences

#### `settings.local.json` (NOT Tracked)
Local overrides for individual developers:
- Personal API keys
- Local paths
- Machine-specific permissions
- Experimental features

Settings are merged with local overrides taking precedence.

### Token Optimization Strategies

1. **`.claudeignore`** - Excludes high-token-cost files:
   - Build artifacts and caches
   - Virtual environments
   - Test coverage reports
   - JSON scan results
   - IDE files

2. **Context Prioritization** - `settings.json` specifies:
   - Primary files: .claude/README.claude.md, README.md, pyproject.toml
   - Important directories: rankle/core, rankle/detectors, etc.

3. **Targeted Operations**:
   - Use specific file reads instead of full directory scans
   - Focus on changed files in git operations
   - Summarize large dependency files

### Best Practices (2026)

**Version Control:**
- ✅ Track `settings.json` (shared config)
- ❌ Don't track `settings.local.json` (personal config)
- ❌ Don't track `cache/` or `logs/` directories

**Permissions:**
- Allow development tools (python, pip, git, ruff, mypy)
- Allow research sources (portswigger.net, owasp.org, github.com)
- Restrict dangerous operations (unless explicitly needed)

**Context Management:**
- Use `.claudeignore` to reduce noise
- Specify primary documentation files
- Identify critical code directories

**Token Budget:**
- Conservative mode for large codebases
- Aggressive mode for small focused work
- Balance between context and cost

### Usage

Claude Code automatically reads configuration from this directory.

To override settings locally:
```bash
cp .claude/settings.json .claude/settings.local.json
# Edit settings.local.json with your overrides
```

---

## Dependencies

### Core Dependencies

- **requests** - HTTP client
- **dnspython** - DNS queries
- **beautifulsoup4** - HTML parsing
- **python-wappalyzer>=0.3.1** - 3000+ technology signatures (NEW v2.0)
- **mmh3>=5.0.0** - Favicon hashing for fingerprinting (NEW v2.0)

### Optional Dependencies

- **python-whois** - WHOIS lookups
- **ipwhois** - IP WHOIS data

### Dev Dependencies

- **pytest** - Testing framework
- **ruff** - Linting and formatting
- **mypy** - Type checking
- **bandit** - Security scanning
- **pre-commit** - Git hooks
- **setuptools** - Package building

See `pyproject.toml` and `requirements.txt` for version requirements.

---

## Testing

### Test Files

- `tests/` directory (pytest framework)
- Coverage target: Core modules > 80%

### Manual Testing

```bash
# Basic functionality
python main.py example.com

# Enhanced detection (v2.0)
python scripts/demo_enhanced_detection.py example.com

# Dependencies verification
python scripts/verify_dependencies.py
```

---

## Docker & CI/CD

**Docker:**
- Alpine base for minimal attack surface (~370MB image)
- Non-root user (UID 1000) for container security
- Volume mount at `/output` for results persistence
- Built-in healthcheck for monitoring
- OCI-compliant labels

**CI/CD:**
- GitHub Actions for Docker build/publish
- Pre-commit hooks (run locally and in CI)
- Type checking (mypy)
- Security scanning (bandit, pip-audit)
- Test coverage requirements

---

## Additional Documentation

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Configuration Reference](https://docs.anthropic.com/claude-code/configuration)
- [Token Optimization Guide](https://docs.anthropic.com/claude-code/optimization)

---

**Note:** This documentation is optimized for token efficiency. For detailed implementation, refer to specific files.
