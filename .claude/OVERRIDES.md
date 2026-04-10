# Claude Code Configuration Overrides

**Policy:** Rankle only overrides global rules (`~/.claude/rules/`) when project architecture requires it.

---

## Overrides in Effect

### Python Version: 3.11+ (vs global 3.13+)

**Global rule says:** Python 3.13+ exclusively (3.10-3.12 are legacy).

**Rankle uses:** Python 3.11+ minimum (`pyproject.toml requires-python = ">=3.11"`).

**Why:** Rankle targets broader ecosystem compatibility. Python 3.11 and 3.12 are active LTS releases with strong security support.

**Decision:** Accept 3.11+ baseline. Plan migration to 3.13+ for 2026 Q3 when LTS dominance shifts.

---

### Type Checker: mypy gradual (vs global pyright strict)

**Global rule says:** pyright in strict mode.

**Rankle uses:** mypy with gradual adoption (`disallow_untyped_defs = false` in pyproject.toml).

**Why:** Type coverage is 65% and growing. Gradual migration allows incremental enforcement:
- `rankle/core/` — target strict
- `rankle/utils/` — target strict
- `rankle/detectors/` — currently gradual (complex logic)

Pyright strict mode is too aggressive for mid-migration projects.

**Decision:** Maintain gradual strategy. Target 90%+ type coverage by 2026 Q3, then evaluate strict mode.

**See:** `.claude/rules/architecture.md` section "What NOT to Change"

---

### Type Syntax: TypeAlias (vs global PEP 695 `type`)

**Global rule says:** PEP 695 `type` keyword syntax (Python 3.13+).

**Rankle uses:** `TypeAlias` from `typing` module (Python 3.11+ compatible).

Example from `rankle/types.py`:
```python
ScanResults: TypeAlias = dict[str, Any]
```

vs PEP 695:
```python
type ScanResults = dict[str, Any]
```

**Why:** TypeAlias is compatible with 3.11+. PEP 695 requires 3.13+.

**Decision:** Migrate to PEP 695 `type` syntax once minimum version reaches 3.13+. TypeAlias is transitional.

---

### Project Layout: Flat (vs global src-layout)

**Global rule says:** Use `src-layout` pattern (src/my_package/...).

**Rankle uses:** Flat layout (rankle/ at root).

**Why:** Rankle is a distributed CLI application, not a library.
Per setuptools best practices (guide.python-packaging.org), CLI applications use flat layout:
- Simpler entry point configuration
- Direct `python main.py` execution
- Cleaner namespace for single-domain tools

**Decision:** Keep flat layout. This is appropriate for CLI/application tools.

---

### Test Coverage Threshold: 70% floor (vs global 85%+)

**Global rule says:** 80% minimum, 85%+ target.

**Rankle uses:** `pytest --cov-fail-under=70`.

**Why:** Reconnaissance modules (detectors/) have high logic complexity and variability. 70% is sustainable baseline.

**Plan:** Incremental increase to 75% (Q2 2026) → 80% (Q3 2026).

**Details by module:**
- `rankle/core/` — 85%+ (target)
- `rankle/utils/` — 85%+ (validators, confidence, rate_limiter)
- `rankle/modules/` — 75%+ (DNS, SSL, subdomains have high variance)
- `rankle/detectors/` — 70%+ baseline (complex fingerprinting logic)

---

### Lazy-Init Architecture Pattern

**Global rules:** No mention (general Python patterns only).

**Rankle uses:** `@property` lazy initialization on `RankleScanner`.

```python
@property
def dns(self) -> DNSAnalyzer:
    if self._dns is None:
        self._dns = DNSAnalyzer(self.domain, self.session)
    return self._dns
```

**Why:** Modules only instantiate when accessed. Reduces startup time, memory footprint, and initialization errors.

**Details:** See `.claude/rules/architecture.md` section "Architecture: Core Design Pattern".

---

## Global Rules Applied

All other standards follow global rules in `~/.claude/rules/`:

| Rule | File | Scope |
|------|------|-------|
| English-only, concise, no emojis | `universal/communication.rule.md` | All text, commits, docs |
| DRY/KISS, 80%+ testing, type safety | `universal/code-quality.rule.md` | Python code patterns |
| Conventional Commits, no force-push | `universal/git-workflow.rule.md` | Git commits and pushes |
| Non-destructive, research-first | `universal/safety.rule.md` | All operations |
| Markdown formatting, inverted pyramid | `stacks/markdown.rule.md` | Markdown documentation |
| Mermaid diagram standards | `stacks/diagrams.rule.md` | Diagrams in .mmd and .md |

---

## When to Reference

**As a contributor:** Start with global rules (`~/.claude/rules/`). If they conflict with project reality (Python 3.11, mypy, flat layout), refer to this file and `.claude/rules/architecture.md`.

**As Claude Code:** Load `.claude/` files when editing rankle/ or config/ directories. Otherwise, global rules apply automatically.

---

**Last Updated:** 2026-04-10
**Authority:** Architecture decisions, not preferences
