---
description: Rankle-specific architecture — lazy-init pattern, module flow, integration guide
paths: rankle/**/*.py, config/**/*.py
---

<!-- Loaded when editing Python files in rankle/ or config/ -->

## Architecture: Core Design Pattern

**Lazy initialization** via `@property` — modules instantiate only when accessed:

```python
@property
def module_name(self) -> ModuleClass:
    if self._module_name is None:
        self._module_name = ModuleClass(self.domain)
    return self._module_name
```

`RankleScanner` (`rankle/core/scanner.py`) orchestrates via this pattern.

## Request Flow

1. `main.py` → `RankleScanner(domain)`
2. `run_full_scan()` coordinates all modules
3. `SessionManager` (`rankle/core/session.py`) — retry + connection pooling + timeouts
4. Each module in `rankle/modules/` and `rankle/detectors/` returns `dict[str, Any]`
5. Reports via `rankle/reports/`

## Module Categories

| Layer | Path | Purpose |
|-------|------|---------|
| Core | `rankle/core/scanner.py` | Orchestrator (lazy init) |
| Core | `rankle/core/session.py` | HTTP client |
| Modules | `rankle/modules/` | DNS, SSL, WHOIS, subdomains, HTTP fingerprint |
| Detectors | `rankle/detectors/` | Technology, CDN, WAF, origin discovery |
| Utils | `rankle/utils/` | Validators, confidence scoring, rate limiting |
| Config | `config/settings.py` | Timeouts, DNS servers, User-Agent, rate limits |
| Config | `config/patterns.py` | Cloud/CDN/WAF ASN patterns |
| Config | `config/tech_signatures.json` | Technology detection signatures (loaded at runtime) |

**Key principle:** All configuration is file-based — no hardcoded values in detection logic.

## Adding New Detection Modules

1. Create in `rankle/modules/` or `rankle/detectors/` with `analyze() -> dict[str, Any]`
2. Add lazy `@property` to `RankleScanner`
3. Call in `run_full_scan()`

Example signature locations: `config/tech_signatures.json`, `rankle/detectors/technology.py:42-646`

**Updated:** 2026-04-10
