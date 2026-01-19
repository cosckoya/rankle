# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

**LANGUAGE POLICY: Always respond in English, regardless of user's language.**

## Custom Skills

10 custom skills available. Invoke with `/skill-name`.

**Core Skills:**
- `/security-scanner-expert` - Security reconnaissance tool development, detection logic review
- `/pattern-updater` - Manage detection signatures in config/patterns.py and config/tech_signatures.json
- `/python-architect` - Enforce Python 3.11+ standards, PEP compliance, Ruff formatting, type hints
- `/test-automator` - Pytest tests, pre-commit hooks, CI/CD pipelines, coverage monitoring
- `/docker-specialist` - Dockerfile optimization, container security, deployment best practices

**Specialized Skills:**
- `/recon-researcher` - Research latest OSINT/reconnaissance techniques from security blogs
- `/api-integrator` - Create integration scripts for Nuclei, Nmap, httpx, jq filters
- `/changelog-maintainer` - Maintain CHANGELOG.md with Keep a Changelog format
- `/config-validator` - Validate configuration files (pyproject.toml, settings.py, patterns.py)
- `/security-auditor` - Code security review, OWASP Top 10, bandit scans, input validation

## Project Overview

**Rankle** - Web infrastructure reconnaissance tool for authorized security testing. Named after "Rankle, Master of Pranks" from Magic: The Gathering.

**Key Features:**
- DNS enumeration (A/AAAA/MX/NS/TXT/SOA/CNAME)
- Subdomain discovery via Certificate Transparency (crt.sh)
- Technology detection: 16+ CMS, 20+ CDN, 15+ WAF solutions
- Cloud provider detection (AWS, Azure, GCP, DigitalOcean, OVH, Hetzner)
- Origin infrastructure discovery behind WAF/CDN (passive techniques only)
- TLS/SSL certificate analysis
- Advanced fingerprinting (HTTP methods, API endpoints, exposed files)

**Ethical Use:** All methods are passive reconnaissance. For authorized testing only.

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
ruff check . --fix                            # Lint and auto-fix
ruff format .                                 # Format code
mypy rankle/                                  # Type checking
bandit -c pyproject.toml -r rankle/           # Security scan
pytest -v --cov=rankle                        # Tests with coverage

# Docker
docker build -t rankle .
docker run --rm rankle example.com
```

## Architecture Overview

**Core Structure:**
```
rankle/
├── main.py                 # Entry point
├── rankle/
│   ├── core/
│   │   ├── scanner.py      # RankleScanner - orchestrates all modules
│   │   └── session.py      # SessionManager - HTTP with retry logic
│   ├── modules/            # DNS, SSL, subdomains, WHOIS, geolocation, fingerprinting
│   ├── detectors/          # Technology, CDN, WAF, origin discovery
│   ├── utils/              # Validators, helpers, rate limiter
│   └── reports/            # Report generation
├── config/
│   ├── settings.py         # Centralized configuration
│   ├── patterns.py         # Cloud providers, ASN patterns
│   └── tech_signatures.json # Technology detection signatures
└── tests/                  # Unit tests (pytest)
```

**Key Classes:**
- **RankleScanner** (`rankle/core/scanner.py:15`) - Main orchestrator with lazy module initialization
- **SessionManager** (`rankle/core/session.py`) - HTTP sessions with retry logic and connection pooling
- **DNSAnalyzer** (`rankle/modules/dns.py:23`) - DNS enumeration using dnspython

**Configuration:** See `config/settings.py` for timeouts, DNS servers, rate limits, User-Agent.

## Code Standards

**Python 3.11+ Requirements:**
- Built-in generics: `dict[str, Any]` not `Dict[str, Any]`
- Union syntax: `str | None` not `Optional[str]`
- Google-style docstrings
- Type hints required on all public functions
- Ruff for linting/formatting (replaces Black, isort, flake8)

**Pre-commit hooks enforce:**
1. Trailing whitespace, EOF fixes, YAML/JSON/TOML validation
2. Black formatting (88 char line length)
3. isort import sorting
4. Ruff linting
5. Bandit security checks
6. mypy type checking

**Design Patterns:**
- Lazy initialization for module instances
- Context managers for resource cleanup (`with` statement)
- Single responsibility per module
- Guard clauses for early returns
- Centralized configuration in `config/settings.py`

## Adding New Detection Modules

**3-Step Integration:**

1. **Create module** with `analyze()` method returning `dict[str, Any]`
2. **Add lazy property** to `RankleScanner` class
3. **Integrate** in `run_full_scan()` method

Example:
```python
# 1. Create rankle/detectors/new_detector.py
class NewDetector:
    def __init__(self, domain: str):
        self.domain = domain

    def analyze(self) -> dict[str, Any]:
        return {"detected": True}

# 2. Add to scanner.py
@property
def new_detector(self) -> NewDetector:
    if self._new_detector is None:
        self._new_detector = NewDetector(self.domain)
    return self._new_detector

# 3. Call in run_full_scan()
self.results["new_feature"] = self.new_detector.analyze()
```

## Security Guidelines

**Input Validation:**
- All domains validated via `validate_domain()` (regex-based)
- URLs sanitized via `extract_domain()`
- Filenames sanitized via `sanitize_filename()` (removes `<>:"/\|?*`)

**Safe Practices:**
- Never use `shell=True` with subprocess
- All HTTP requests have timeout controls
- Rate limiting between requests (configurable in settings)
- Realistic User-Agent to avoid detection

**Ethical Scanning:**
- ONLY passive reconnaissance techniques (public DNS/SSL/CT logs)
- NO active attacks or unauthorized access attempts
- Origin discovery uses only publicly accessible information
- Document the source of each reconnaissance technique

## Research Protocol for New Features

**MANDATORY: Research modern techniques before implementing new features.**

**When to Research:**
1. Adding new detection modules (CDN, WAF, CMS)
2. Improving origin discovery methods
3. Adding subdomain enumeration sources
4. Enhancing technology fingerprinting

**Research Sources (Use WebFetch/WebSearch):**
- PortSwigger Web Security Blog (portswigger.net/research)
- OWASP Testing Guide (owasp.org/www-project-web-security-testing-guide)
- Bug Bounty Methodology searches ("bug bounty recon methodology 2025")
- Security tool documentation (Amass, Subfinder, httpx, nuclei)
- GitHub Security Research ("passive reconnaissance", "asset discovery")

**Key Research Areas:**
1. **Subdomain Enumeration** - CT APIs (crt.sh, certspotter, censys), passive DNS
2. **Origin Discovery** - Historical DNS, SSL certificates, SPF/DMARC/DKIM, favicon hashing
3. **Technology Detection** - HTTP fingerprinting, JavaScript library detection, error signatures
4. **Cloud Infrastructure** - AWS/Azure/GCP IP ranges, cloud metadata endpoints

**Research Workflow:**
```
1. WebSearch: "passive reconnaissance techniques 2025 bug bounty"
2. WebSearch: "[specific_feature] bypass detection methods"
3. WebFetch: Read relevant blog posts or documentation
4. Analyze and implement ONLY passive techniques
5. Update config/patterns.py with new signatures
6. Document the source in code comments
```

**Ethical Constraint:** ONLY implement passive techniques. All data sources must be publicly accessible.

## Docker Best Practices

**Security Features:**
- Alpine base for minimal attack surface (~370MB image)
- Non-root user (UID 1000) for container security
- Volume mount at `/output` for results persistence
- Built-in healthcheck for monitoring
- OCI-compliant labels

## CI/CD

**GitHub Actions:**
- `.github/workflows/docker-build.yml` - Tests Docker build on PR/push
- `.github/workflows/docker-publish.yml` - Publishes images on tags

**Quality Gates:**
- Pre-commit hooks (run locally and in CI)
- Type checking (mypy)
- Security scanning (bandit, pip-audit)
- Test coverage requirements

## Dependencies

**Core:** requests, dnspython, beautifulsoup4
**Optional:** python-whois, ipwhois
**Dev:** pytest, ruff, mypy, bandit, pre-commit

See `pyproject.toml` for version requirements.

---

**Last Updated:** 2026-01-19
**Maintained By:** Claude Code + Human collaboration
