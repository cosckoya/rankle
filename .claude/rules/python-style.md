---
description: Python style rules for Rankle — 3.11+ type syntax, ruff, mypy, project-specific patterns
paths: rankle/**/*.py, config/**/*.py, tests/**/*.py
---

<!-- Loaded lazily when editing Python files in this project -->

## Python Version Target

**Minimum: 3.11** (pyproject.toml `requires-python = ">=3.11"`).
**Recommended runtime: 3.13+** — use 3.13+ syntax when possible, test compatibility on 3.11.

## Type Syntax (3.11+ required, 3.13+ preferred)

```python
# Always use built-in generics (3.9+)
dict[str, Any]        # not Dict[str, Any]
list[str]             # not List[str]
tuple[str, int]       # not Tuple[str, int]

# Union syntax (3.10+)
str | None            # not Optional[str]
str | int | None      # not Union[str, int, None]

# Return types on ALL public methods — no exceptions
def analyze(self) -> dict[str, Any]: ...

# TYPE_CHECKING for circular imports (already used in scanner.py)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rankle.utils.rate_limiter import RateLimiter
```

### Self (Python 3.11+) for lazy-init pattern

The `Self` type improves the existing `@property` lazy-init pattern:

```python
from typing import Self

class RankleScanner:
    def with_timeout(self, timeout: int) -> Self:
        self.timeout = timeout
        return self
```

### TypeIs for confidence scoring (Python 3.13+)

```python
from typing import TypeIs

def is_high_confidence(score: float) -> TypeIs[float]:
    """Narrow float to high-confidence range [0.8, 1.0]."""
    return 0.8 <= score <= 1.0
```

## Project-Specific Patterns

### Lazy Initialization (@property)

Every module uses lazy init. Type the private backing field explicitly:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rankle.modules.dns import DNSAnalyzer

class RankleScanner:
    def __init__(self) -> None:
        self._dns: DNSAnalyzer | None = None  # Always annotate as T | None

    @property
    def dns(self) -> "DNSAnalyzer":
        if self._dns is None:
            self._dns = DNSAnalyzer(self.domain, self.session)
        return self._dns
```

### Module Return Type

All modules and detectors return `dict[str, Any]`. Use the project type aliases from `rankle/types.py`:

```python
from rankle.types import ScanResults, DetectionResults, Evidence

def analyze(self) -> DetectionResults:
    return {"detected": True, "confidence": 0.9, "evidence": []}
```

### Error Handling

Use specific exceptions, never bare `except Exception`:

```python
import requests

try:
    response = self.session.get(url, timeout=self.timeout)
    response.raise_for_status()
except requests.exceptions.Timeout:
    return {"error": "timeout", "url": url}
except requests.exceptions.HTTPError as exc:
    return {"error": f"http_{exc.response.status_code}", "url": url}
```

## Tooling Commands

```bash
# Development workflow
uv sync                            # Install deps (prefer over pip)
ruff check . --fix                 # Lint + auto-fix
ruff format .                      # Format
mypy rankle/                       # Type check (gradual strictness, see pyproject.toml)
bandit -c pyproject.toml -r rankle/ # Security scan
pre-commit run --all-files         # All checks at once
```

```bash
# Testing
pytest -v --cov=rankle             # All tests with coverage
pytest tests/test_scanner.py -v   # Single file
pytest -n auto                     # Parallel (pytest-xdist)
pytest -m "not slow"              # Skip slow tests
pytest -m "not integration"       # Skip integration tests
```

## Coverage Targets

| Module | Minimum | Target |
|--------|---------|--------|
| `rankle/core/` | 70% | 85%+ |
| `rankle/utils/validators.py` | 85% | 95%+ |
| `rankle/modules/` | 60% | 80%+ |
| `rankle/detectors/` | 55% | 75%+ |
| Overall | 50% | 65%+ |

Currently configured: `--cov-fail-under=50` in pyproject.toml.

## Docstrings

Google style. Required on all public `analyze()` methods and scanner properties.

```python
def analyze(self) -> dict[str, Any]:
    """Perform DNS enumeration for the target domain.

    Queries A, AAAA, MX, NS, TXT, SOA, and CNAME records using
    configured DNS resolvers with retry on timeout.

    Returns:
        Dictionary with keys: records (dict), nameservers (list),
        errors (list), timestamp (str).

    Raises:
        dns.exception.DNSException: On unrecoverable resolver failure.
    """
```

## What NOT to Change

- **Do NOT switch to pyright** — mypy is already configured with gradual strictness in `pyproject.toml`. Switching would require full type annotation completion first.
- **Do NOT raise coverage target above 50%** without first writing the missing tests — the threshold must reflect actual state.
- **Do NOT add `strict = true`** to mypy until all modules have complete type hints.
