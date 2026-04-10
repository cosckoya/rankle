# CLAUDE.md — Rankle

Web infrastructure reconnaissance tool for authorized security testing.
Named after "Rankle, Master of Pranks" from Magic: The Gathering.

**Architecture reference:** `.claude/rules/architecture.md` (auto-loaded when editing Python files)
**Python style guide:** `.claude/rules/python-style.md` (auto-loaded when editing Python files)

---

## Commands

```bash
# Setup
uv sync                              # Install all dependencies
pre-commit install                   # Install git hooks

# Run scans
python main.py example.com           # Basic scan
python main.py example.com -o json   # Save as JSON
python main.py example.com -v        # Verbose

# Code quality (also available via make)
ruff check . --fix && ruff format .  # Lint and format
mypy rankle/                         # Type check
bandit -c pyproject.toml -r rankle/  # Security scan
pre-commit run --all-files           # All checks at once

# Testing
pytest -v --cov=rankle               # All tests with coverage (70% minimum)
pytest -n auto                       # Parallel
pytest -m "not slow"                 # Skip slow

# Docker
docker build -t rankle .
docker run --rm rankle example.com
docker run --rm -v $(pwd)/output:/output rankle example.com -o json

# Makefile shortcuts
make lint            # ruff check + format
make test            # pytest with coverage
make audit-quality   # full quality audit
make sprint-report   # coverage + type check report
```

---

## Security Constraints — CRITICAL

This tool performs **passive reconnaissance only**. Never implement or suggest active techniques.

**Allowed:**
- DNS queries (public DNS servers)
- SSL/TLS certificate inspection
- HTTP GET/HEAD/OPTIONS to target
- Certificate Transparency logs (crt.sh)
- Public WHOIS data

**Never implement:**
- Active attacks (XSS, SQLi, CSRF, etc.)
- Brute force or credential stuffing
- Unauthorized access or exploitation

Input validation lives in `rankle/utils/validators.py`.

---

## Architecture Summary

**Entry point:** `main.py` → `RankleScanner(domain)` → `run_full_scan()`

Key pattern: lazy initialization via `@property` on `RankleScanner`.
Full details: `.claude/rules/architecture.md`

---

## Testing Strategy

- Coverage target: **70% minimum** (`pyproject.toml` `--cov-fail-under=70`)
- Markers: `@pytest.mark.slow`, `@pytest.mark.integration`
- Fixtures in `tests/conftest.py`

---

**Last Updated:** 2026-04-10
**Version:** 2.1
