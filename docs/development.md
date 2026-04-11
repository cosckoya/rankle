# Development Guide

This comprehensive guide covers everything you need to contribute to Rankle, from setup to releasing new versions.

## Table of Contents

1. [Contributing Guidelines](#contributing-guidelines)
2. [Development Setup](#development-setup)
3. [Testing](#testing)
4. [Code Quality](#code-quality)
5. [Pre-commit Hooks](#pre-commit-hooks)
6. [CI/CD](#cicd)
7. [Python Coding Standards](#python-coding-standards)
8. [Security Best Practices](#security-best-practices)
9. [Adding Detection Patterns](#adding-detection-patterns)
10. [Release Process](#release-process)

---

## Contributing Guidelines

### How to Contribute

Thank you for your interest in contributing to Rankle.

#### Reporting Bugs

If you find a bug, please open an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Relevant logs or error messages

#### Suggesting Enhancements

Enhancement suggestions are welcome. Please include:

- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Examples of similar features (if any)

#### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**

   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**

   ```bash
   # Run tests
   pytest

   # Test manually
   uv run python main.py example.com

   # Run linting
   ruff check .
   ```

5. **Commit with clear messages**

   ```bash
   git commit -m "Add: Enhanced detection for XYZ CMS"
   ```

6. **Push to your fork**

   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Focus on the code, not the person
- Remember: we're all here to learn and improve security

---

## Development Setup

### Requirements

- Python 3.13+
- Git
- uv (package manager)

### Clone the Repository

```bash
git clone https://github.com/javicosvml/rankle.git
cd rankle
```

### Install Dependencies

```bash
# Install all dependencies (creates venv automatically)
uv sync

# Install pre-commit hooks
pre-commit install
```

### Verify Installation

```bash
# Check Python version
python --version  # Should be 3.13+

# Run a test scan
uv run python main.py example.com

# Verify linting tools
ruff --version
pyright --version
pytest --version
```

---

## Testing

Rankle uses pytest for testing with a minimum coverage requirement of 85%.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_validators.py

# Run specific test function
pytest tests/test_validators.py::test_validate_domain

# Run with coverage report
pytest --cov=src/rankle --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src/rankle --cov-report=html
# Open htmlcov/index.html in browser
```

### Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = [
    "-ra",                           # Show all test summary info
    "-q",                            # Quiet mode
    "--strict-markers",              # Error on unknown markers
    "--cov=src/rankle",              # Coverage for rankle package
    "--cov-report=term-missing",     # Show missing lines
    "--cov-fail-under=85",           # Require 85%+ coverage
]
```

### Coverage Requirements

- Minimum coverage: 85%
- Branch coverage enabled
- Reports show missing lines
- HTML reports generated in `htmlcov/`

### Test Structure

```
tests/
├── test_validators.py      # Input validation tests
├── test_dns.py             # DNS module tests
├── test_ssl.py             # SSL module tests
└── test_detectors.py       # Detection logic tests
```

### Writing Tests

```python
# tests/test_example.py
import pytest
from rankle.utils.validators import validate_domain

def test_validate_domain():
    """Test domain validation."""
    assert validate_domain("example.com") is True
    assert validate_domain("invalid..com") is False

def test_validate_domain_edge_cases():
    """Test edge cases for domain validation."""
    assert validate_domain("") is False
    assert validate_domain("a.b.c.d.e.example.com") is True
```

---

## Code Quality

Rankle enforces strict code quality standards using modern Python tools.

### Linting with Ruff

Ruff is a modern, fast linter that replaces Black, isort, flake8, and more.

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .

# Check specific file
uv run ruff check src/rankle/core/scanner.py
```

### Type Checking with Pyright

```bash
# Run type checking
uv run pyright src/rankle/

# Check specific file
uv run pyright src/rankle/core/scanner.py
```

### Security Scanning with Bandit

```bash
# Run security checks
bandit -c pyproject.toml -r src/rankle/

# Verbose output
bandit -c pyproject.toml -r src/rankle/ -v

# Check specific file
bandit src/rankle/core/session.py
```

### Dependency Vulnerability Scanning

```bash
# Scan for vulnerable dependencies
pip-audit

# Generate JSON report
pip-audit --output json > audit-report.json
```

### All Quality Checks

```bash
# Run all quality checks in sequence
uv run ruff check . && \
uv run ruff format . && \
uv run pyright src/rankle/ && \
bandit -c pyproject.toml -r src/rankle/ && \
pytest --cov=src/rankle --cov-fail-under=85
```

---

## Pre-commit Hooks

Pre-commit hooks automatically check code quality before each commit.

### Installation

```bash
# Install pre-commit via uv
uv pip install pre-commit

# Install git hooks
pre-commit install

# Install commit message hooks
pre-commit install --hook-type commit-msg
```

### Running Pre-commit

```bash
# Run on all files
pre-commit run --all-files

# Run on staged files (happens automatically on commit)
git commit -m "Your message"

# Update hook versions
pre-commit autoupdate
```

### Skip Hooks (When Necessary)

```bash
# Skip specific hook
SKIP=pyright git commit -m "WIP: Experimental feature"

# Skip all hooks (use sparingly)
git commit --no-verify -m "Emergency fix"
```

### Configured Hooks

The following hooks run automatically on commit:

1. **General File Checks**
   - Trailing whitespace removal
   - End-of-file fixer
   - Mixed line ending fixer
   - YAML/JSON/TOML validation

2. **Python Checks**
   - Syntax validation
   - Debug statement detection

3. **Security Checks**
   - Merge conflict detection
   - Large file detection (500KB limit)
   - Private key detection

4. **Code Quality**
   - Ruff linting with auto-fix
   - Ruff formatting
   - Pyright type checking

5. **Commit Standards**
   - Commitizen commit message format enforcement

---

## CI/CD

Rankle uses GitHub Actions for continuous integration and deployment.

### Workflows

#### 1. Quality Checks

Runs on every push and pull request to `main`:

```yaml
- Checkout code
- Set up Python 3.13+
- Install dependencies via uv sync
- Run ruff check + format
- Run pyright
- Run pytest with coverage
```

**Triggers:**

- Push to `main` branch
- Pull requests to `main`

**Purpose:** Ensure code quality and test coverage are maintained.

### CI Best Practices

1. **Always test locally before pushing**
2. **Keep workflows fast** — use caching
3. **Fail fast** — critical checks first
4. **Parallel jobs** — run independent checks concurrently
5. **Clear failure messages** — easy debugging

---

## Python Coding Standards

Rankle follows Python 3.13+ best practices and modern conventions.

### Type Hints

**Always use type hints** for function signatures and complex variables.

```python
# Use built-in generics (Python 3.9+)
def analyze(self) -> dict[str, Any]:    # YES
def analyze(self) -> Dict[str, Any]:    # NO (deprecated)

# Use union syntax (Python 3.10+)
def query(self) -> str | None:          # YES
def query(self) -> Optional[str]:       # NO (deprecated)

# PEP 695 type aliases (Python 3.13+)
type IPList = list[str]
type ConfigDict = dict[str, Any]
```

### Docstrings

Use **Google-style docstrings** for all public functions and classes:

```python
def validate_domain(domain: str) -> bool:
    """
    Validate domain name format using regex.

    Args:
        domain: Domain name to validate (e.g., "example.com")

    Returns:
        True if domain format is valid, False otherwise

    Examples:
        >>> validate_domain("example.com")
        True
        >>> validate_domain("invalid..com")
        False
    """
    # Implementation
```

### Error Handling

**Use specific exceptions**, never bare `except`:

```python
# Good
try:
    answers = resolver.resolve(domain, "A")
except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
    return []
except dns.exception.Timeout as e:
    print(f"DNS timeout: {e}")
    return []

# Bad
try:
    answers = resolver.resolve(domain, "A")
except:  # Never do this
    return []
```

### Design Patterns

#### Lazy Initialization

Use properties for lazy initialization:

```python
class RankleScanner:
    def __init__(self, domain: str):
        self._dns_analyzer: DNSAnalyzer | None = None

    @property
    def dns_analyzer(self) -> DNSAnalyzer:
        if self._dns_analyzer is None:
            self._dns_analyzer = DNSAnalyzer(self.domain)
        return self._dns_analyzer
```

#### Context Managers

Implement context managers for resource cleanup:

```python
class RankleScanner:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Usage
with RankleScanner(domain) as scanner:
    results = scanner.run_full_scan()
# Cleanup happens automatically
```

### Code Organization

#### Single Responsibility Principle

Each module should have one clear purpose:

```python
# validators.py - Input validation only
def validate_domain(domain: str) -> bool: ...
def sanitize_filename(filename: str) -> str: ...

# dns.py - DNS queries only
class DNSAnalyzer:
    def analyze(self) -> dict[str, Any]: ...

# scanner.py - Orchestration only
class RankleScanner:
    def run_full_scan(self) -> dict[str, Any]: ...
```

#### DRY (Don't Repeat Yourself)

- Centralized configuration in `src/config/settings.py`
- Shared patterns in `src/config/patterns.py`
- Reusable utilities in `src/rankle/utils/`

#### Meaningful Names

```python
# Good
def validate_domain(domain: str) -> bool:
def extract_domain(url: str) -> str:
def truncate_list(items: list, max_items: int = 3) -> str:

# Bad
def check(d: str) -> bool:
def get_d(u: str) -> str:
def trunc(l: list, m: int = 3) -> str:
```

#### Guard Clauses

Use early returns for cleaner code:

```python
def analyze_geolocation(self, ip: str) -> dict | None:
    if not ip:
        return None
    if not self.is_valid_ip(ip):
        return None
    # Main logic here
```

---

## Security Best Practices

### Input Validation

**Always validate user input** before processing:

```python
from rankle.utils.validators import validate_domain, sanitize_filename

# Validate domain
if not validate_domain(user_input):
    raise ValueError("Invalid domain format")

# Sanitize filenames
safe_filename = sanitize_filename(user_input)
```

### Safe Subprocess Usage

**Never use `shell=True`** — it enables shell injection attacks:

```python
# Good
subprocess.run(["nslookup", domain], capture_output=True)

# Bad - NEVER DO THIS
subprocess.run(f"nslookup {domain}", shell=True)
```

### Timeout Controls

**Always set timeouts** to prevent hanging requests:

```python
from src.config.settings import DEFAULT_TIMEOUT

# HTTP requests
response = session.get(url, timeout=DEFAULT_TIMEOUT)

# DNS queries
resolver.timeout = DNS_TIMEOUT
resolver.lifetime = DNS_TIMEOUT
```

### Error Handling

**Graceful degradation** — don't crash on failures:

```python
try:
    results = self.dns_analyzer.analyze()
except Exception as e:
    print(f"DNS analysis failed: {e}")
    results = {"error": str(e)}
```

### Sensitive Data

**Never log or expose sensitive information**:

```python
# Remove sensitive patterns from filenames
def sanitize_filename(filename: str) -> str:
    # Removes: <>:"/\|?*
    return re.sub(r'[<>:"/\\|?*]', '', filename)
```

### Rate Limiting

**Respect server resources** with rate limiting:

```python
from src.config.settings import RATE_LIMIT_DELAY
import time

for subdomain in subdomains:
    check_subdomain(subdomain)
    time.sleep(RATE_LIMIT_DELAY)
```

### Ethical Scanning

**All methods must be passive and use public data**:

- DNS queries (public records)
- Certificate Transparency logs (public)
- SSL certificate analysis (public)
- Port scanning is not implemented (active)
- Vulnerability exploitation is not implemented
- Unauthorized access attempts are not implemented

---

## Adding Detection Patterns

### Adding CMS Detection

Edit `src/rankle/detectors/technology.py`:

```python
def _detect_cms(self, html_lower: str, soup) -> str | None:
    cms_patterns = {
        'YourCMS': [
            r'unique-pattern-1',
            r'unique-pattern-2',
            r'characteristic-url-path',
            r'cms-specific-identifier'
        ],
        # ... existing patterns
    }

    for cms, patterns in cms_patterns.items():
        for pattern in patterns:
            if re.search(pattern, html_lower):
                return cms
    return None
```

**Test your detection:**

```bash
uv run python main.py example-with-your-cms.com
pytest tests/test_detectors.py::test_cms_detection
```

### Adding CDN Detection

Edit `src/config/patterns.py` or `src/rankle/detectors/cdn.py`:

```python
cdn_indicators = {
    'YourCDN': [
        'x-cdn-header',
        'cdn-specific-identifier',
        'cache-status-header'
    ],
    # ... existing CDNs
}
```

**Headers to check:**

- Custom CDN headers (X-CDN-*, X-Cache-*)
- Server headers
- Via headers
- Edge/cache status headers

### Adding WAF Detection

Edit `src/rankle/detectors/waf.py`:

```python
waf_indicators = {
    'YourWAF': [
        'x-waf-header',
        'protection-identifier',
        'challenge-cookie'
    ],
    # ... existing WAFs
}
```

**Common WAF indicators:**

- Protection headers
- Challenge cookies
- Bot detection scripts
- Specific error pages

### Adding Cloud Provider Detection

Edit `src/config/patterns.py`:

```python
# Cloud provider patterns (ASN, hostnames, ISP names)
CLOUD_PROVIDERS: dict[str, dict[str, Any]] = {
    "YourCloudProvider": {
        "asns": [12345, 67890],
        "isp_patterns": [
            r"your.*cloud",
            r"ycp-infrastructure"
        ],
        "hostname_patterns": [
            r".*\.yourcloud\.com$",
            r".*\.ycp\.net$"
        ]
    },
    # ... existing providers
}
```

### Testing Detection Patterns

Create unit tests for new patterns:

```python
# tests/test_detectors.py
def test_new_cms_detection():
    """Test detection of NewCMS."""
    html = "<html><meta name='generator' content='NewCMS 2.0'></html>"
    detector = TechnologyDetector()
    result = detector.detect(html)
    assert result['cms'] == 'NewCMS'
```

---

## Release Process

### Version Numbering

Rankle follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 2.1.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Pre-release Checklist

1. **Update CHANGELOG.md**

   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD

   ### Added
   - New feature description

   ### Changed
   - Modified behavior

   ### Fixed
   - Bug fix description
   ```

2. **Update version in `pyproject.toml`**

   ```toml
   [project]
   version = "X.Y.Z"
   ```

3. **Run all tests and checks**

   ```bash
   pytest --cov=src/rankle --cov-fail-under=85
   uv run ruff check .
   uv run ruff format .
   uv run pyright src/rankle/
   bandit -c pyproject.toml -r src/rankle/
   ```

4. **Manual testing**

   ```bash
   uv run python main.py example.com
   uv run python main.py example.com -o
   uv run python main.py example.com -v
   ```

### Creating a Release

#### Option 1: Git Tag

```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release v1.2.0 - New features"

# Push tag to remote
git push origin v1.2.0
```

#### Option 2: GitHub CLI

```bash
# Create release with notes
gh release create v1.2.0 \
  --title "v1.2.0 - Feature Release" \
  --notes "$(cat CHANGELOG.md | sed -n '/## \[1.2.0\]/,/## \[1.1/p' | head -n -1)"
```

#### Option 3: GitHub Web Interface

1. Go to repository on GitHub
2. Click "Releases" → "Draft a new release"
3. Choose tag: `v1.2.0`
4. Release title: `v1.2.0 - Feature Release`
5. Copy release notes from CHANGELOG.md
6. Publish release

### Post-release Tasks

1. **Update documentation**

   - Ensure README.md is current
   - Update examples if APIs changed
   - Check all links work

2. **Announce release**

   - GitHub Discussions
   - Social media (if applicable)
   - Security community forums

### Hotfix Releases

For urgent bug fixes:

```bash
# Create hotfix branch from main
git checkout -b hotfix/critical-fix main

# Make fix
# Update CHANGELOG.md (PATCH version)
# Update pyproject.toml version

# Test thoroughly
pytest
uv run python main.py example.com

# Commit and tag
git commit -m "Fix: Critical security issue"
git tag -a v1.2.1 -m "Hotfix v1.2.1 - Security fix"
git push origin v1.2.1

# Merge back to main
git checkout main
git merge hotfix/critical-fix
git push origin main
```

---

## Development Workflow Summary

### Daily Development

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/new-detection

# 3. Make changes
# Edit files...

# 4. Run quality checks (pre-commit does this automatically)
uv run ruff check .
pytest

# 5. Commit (pre-commit hooks run automatically)
git commit -m "Add: New detection pattern"

# 6. Push
git push origin feature/new-detection

# 7. Open PR on GitHub
```

### Before Committing

```bash
# Format code
uv run ruff format .

# Fix linting issues
uv run ruff check . --fix

# Run tests with coverage
pytest --cov=src/rankle

# Type check
uv run pyright src/rankle/

# Security scan
bandit -c pyproject.toml -r src/rankle/

# Or run pre-commit manually
pre-commit run --all-files
```

### Continuous Improvement

- Write tests for new features
- Maintain 85%+ code coverage
- Keep dependencies updated
- Document complex logic
- Follow Python best practices
- Review security implications

---

## Additional Resources

### Documentation

- [README.md](../README.md) - Project overview and usage
- [Changelog](changelog.md) - Version history
- [Security Policy](security.md) - Security policy
- [CLAUDE.md](../CLAUDE.md) - AI assistant instructions

### External Resources

- [Python 3.13+ Documentation](https://docs.python.org/3.13/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pyright Documentation](https://github.com/microsoft/pyright)
- [pytest Documentation](https://docs.pytest.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

### Community

- [GitHub Issues](https://github.com/javicosvml/rankle/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/javicosvml/rankle/discussions) - Community discussions
- [Pull Requests](https://github.com/javicosvml/rankle/pulls) - Code contributions

---

## Quick Reference

### Common Commands

```bash
# Setup
uv sync
pre-commit install

# Testing
pytest                                       # Run tests
pytest --cov=src/rankle                      # With coverage
pytest tests/test_validators.py              # Specific file

# Code Quality
uv run ruff check .                          # Lint
uv run ruff format .                         # Format
uv run pyright src/rankle/                   # Type check
bandit -c pyproject.toml -r src/rankle/      # Security scan
pre-commit run --all-files                   # Run all hooks

# Git
git checkout -b feature/name                 # New branch
git commit -m "Add: Description"             # Commit
git tag -a v1.2.0 -m "Release v1.2.0"        # Tag release
```

### File Structure

```
rankle/
├── pyproject.toml          # Python packaging and tool configuration
├── uv.lock                 # Locked dependency versions
├── main.py                 # Entry point
├── src/
│   ├── rankle/             # Main package
│   │   ├── core/          # Scanner & session management
│   │   ├── modules/       # Reconnaissance modules
│   │   ├── detectors/     # Technology detectors
│   │   └── utils/         # Utilities
│   └── config/             # Configuration
│       ├── settings.py    # Settings
│       ├── patterns.py    # Detection patterns
│       └── tech_signatures.json
├── tests/                  # Unit tests
├── reports/                # Scan output reports
├── docs/                   # Documentation
└── .github/workflows/      # CI/CD
```

---

If you have questions, open an issue or start a discussion on GitHub.
