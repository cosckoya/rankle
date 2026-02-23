# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**LANGUAGE POLICY: Always respond in English, regardless of user's language.**

---

## Project: Rankle

Web infrastructure reconnaissance tool for authorized security testing. Named after "Rankle, Master of Pranks" from Magic: The Gathering.

**Complete documentation:** `.claude/README.claude.md`

---

## Common Commands

### Development Setup
```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Scans
```bash
# Basic scan
python main.py example.com

# Save as JSON for automation
python main.py example.com -o json

# Verbose output
python main.py example.com -v
```

### Testing
```bash
# Run all tests with coverage
pytest -v --cov=rankle

# Run single test file
pytest tests/test_scanner.py -v

# Run single test function
pytest tests/test_scanner.py::test_specific_function -v

# Run tests in parallel
pytest -n auto

# Skip slow tests
pytest -m "not slow"
```

### Code Quality
```bash
# Lint and auto-fix
ruff check . --fix

# Format code
ruff format .

# Type check
mypy rankle/

# Security scan
bandit -c pyproject.toml -r rankle/

# All checks at once (pre-commit)
pre-commit run --all-files
```

### Docker
```bash
# Build
docker build -t rankle .

# Run scan
docker run --rm rankle example.com

# Save output
docker run --rm -v $(pwd)/output:/output rankle example.com -o json
```

---

## High-Level Architecture

### Core Design Pattern: Lazy Initialization

**Key Insight:** `RankleScanner` (`rankle/core/scanner.py:15`) orchestrates all modules using lazy initialization via `@property` decorators. Modules are only instantiated when accessed, reducing memory and improving startup time.

```python
# Pattern used throughout:
@property
def module_name(self) -> ModuleClass:
    if self._module_name is None:
        self._module_name = ModuleClass(self.domain)
    return self._module_name
```

### Request Flow

1. **Entry Point:** `main.py` → creates `RankleScanner(domain)`
2. **Orchestration:** `RankleScanner.run_full_scan()` coordinates all modules
3. **HTTP Layer:** `SessionManager` (`rankle/core/session.py`) handles all HTTP with:
   - Automatic retry logic (exponential backoff)
   - Connection pooling (requests.Session)
   - Timeout controls
4. **Module Execution:** Each module in `rankle/modules/` and `rankle/detectors/` returns `dict[str, Any]`
5. **Output:** Reports generated via `rankle/reports/`

### Configuration Architecture

**Centralized configuration in `config/` directory:**
- `settings.py` - Timeouts, DNS servers, User-Agent, rate limits
- `patterns.py` - Cloud provider ASN patterns, detection rules
- `tech_signatures.json` - Technology detection signatures (loaded at runtime)

**Key principle:** All configuration is file-based, no hardcoded values in detection logic.

### Module Categories

**Core (`rankle/core/`):**
- `scanner.py` - Main orchestrator (lazy init pattern)
- `session.py` - HTTP client with retry logic

**Reconnaissance (`rankle/modules/`):**
- DNS, SSL/TLS, WHOIS, subdomains, HTTP fingerprinting
- Each module is independent, called by scanner

**Detection (`rankle/detectors/`):**
- Technology detection (1179 lines, uses Wappalyzer + custom patterns)
- CDN, WAF, cloud provider detection
- Origin discovery behind WAF/CDN

**Utilities (`rankle/utils/`):**
- Input validation (domain, URL sanitization)
- Confidence scoring (0.0-1.0 scale)
- Rate limiting between requests
- V2.0 additions: favicon hashing, error fingerprinting, JS extraction, WordPress detection, CVE mapping

### Adding New Detection Modules

**3-step integration pattern:**

1. Create module in `rankle/modules/` or `rankle/detectors/` with `analyze()` method returning `dict[str, Any]`
2. Add lazy `@property` to `RankleScanner` class
3. Call in `run_full_scan()` method

**Example locations:**
- Detection signatures: `config/tech_signatures.json` or `rankle/detectors/technology.py:42-646`
- CDN/WAF patterns: `rankle/detectors/cdn.py` or `rankle/detectors/waf.py`

---

## Critical Constraints

### Security: ONLY Passive Reconnaissance

**This tool uses ONLY passive techniques:**
- DNS queries (public DNS servers)
- SSL/TLS certificate inspection
- HTTP requests to target (standard GET/HEAD/OPTIONS)
- Certificate Transparency log queries (crt.sh)
- Public WHOIS data

**NEVER implement:**
- Active attacks (XSS, SQLi, etc.)
- Brute force attempts
- Unauthorized access
- Vulnerability exploitation

**Input validation:** All domains validated via `rankle/utils/validators.py` (regex-based, prevents injection)

### Python 3.11+ Requirements

**Type hints (PEP 604):**
- Use built-in generics: `dict[str, Any]` not `Dict[str, Any]`
- Use union syntax: `str | None` not `Optional[str]`

**Tooling:**
- Ruff (linting + formatting) replaces Black, isort, flake8
- Type checking with mypy (gradual strictness)
- Security scanning with bandit

---

## Testing Strategy

**Coverage target:** 50% minimum (configured in pyproject.toml)

**Test organization:**
- `tests/` directory uses pytest
- Markers: `@pytest.mark.slow`, `@pytest.mark.integration`
- Parallel execution: `pytest -n auto`

**Pre-commit hooks enforce:**
1. Trailing whitespace, EOF fixes
2. Ruff formatting (88 char line length)
3. Ruff linting
4. Bandit security checks
5. mypy type checking

---

## Docker Architecture

**Security features:**
- Alpine base (~370MB image)
- Non-root user (UID 1000)
- Volume mount at `/output` for results
- Built-in healthcheck

---

**Last Updated:** 2026-02-19
**Version:** 2.0 (Enhanced Technology Detection)
