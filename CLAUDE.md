# CLAUDE.md

<!-- Project: Rankle v2.0 | Last Updated: 2026-03-26 -->

**LANGUAGE POLICY: Always respond in English, regardless of user's language.**

## Project: Rankle

Web infrastructure reconnaissance tool for authorized security testing.
Named after "Rankle, Master of Pranks" from Magic: The Gathering.

**Architecture reference:** `.claude/rules/architecture.md` (auto-loaded when editing Python files)

---

## Commands

### Setup

```bash
uv sync                    # Install all dependencies (preferred)
pip install -e ".[dev]"    # Fallback if uv not available
pre-commit install         # Install git hooks
```

### Run Scans

```bash
python main.py example.com          # Basic scan
python main.py example.com -o json  # Save as JSON
python main.py example.com -v       # Verbose
```

### Code Quality

```bash
ruff check . --fix          # Lint and auto-fix
ruff format .               # Format
mypy rankle/                # Type check
bandit -c pyproject.toml -r rankle/  # Security scan
pre-commit run --all-files  # All checks at once
```

### Testing

```bash
pytest -v --cov=rankle      # All tests with coverage
pytest -n auto              # Parallel
pytest -m "not slow"        # Skip slow
```

### Docker

```bash
docker build -t rankle .
docker run --rm rankle example.com
docker run --rm -v $(pwd)/output:/output rankle example.com -o json
```

---

## Architecture Summary

**Entry point:** `main.py` → `RankleScanner(domain)` → `run_full_scan()`

Key pattern: lazy initialization via `@property` decorators on `RankleScanner`.
Full reference: `.claude/rules/architecture.md`

---

## Critical Constraints

### Security: ONLY Passive Reconnaissance

**Allowed:**

- DNS queries (public DNS servers)
- SSL/TLS certificate inspection
- HTTP GET/HEAD/OPTIONS to target
- Certificate Transparency logs (crt.sh)
- Public WHOIS data

**YOU MUST NEVER implement:**

- Active attacks (XSS, SQLi, etc.)
- Brute force or credential stuffing
- Unauthorized access or exploitation

**Input validation:** `rankle/utils/validators.py` (regex, prevents injection)

### Type Hints

Use Python 3.11+ syntax: `dict[str, Any]` not `Dict`, `str | None` not `Optional[str]`.
Full style guide: `.claude/rules/python-style.md`

---

## Testing Strategy

- Coverage target: 50% minimum (pyproject.toml `--cov-fail-under=50`)
- Markers: `@pytest.mark.slow`, `@pytest.mark.integration`
- Fixtures in `tests/conftest.py`

---

## Docker Architecture

Alpine base, non-root user (UID 1000), volume at `/output`, built-in healthcheck.

---

**Last Updated:** 2026-03-26
**Version:** 2.0 (Enhanced Technology Detection)
