# Claude Code Configuration

This directory contains Claude Code configuration files following 2026 best practices.

## Files

### `settings.json` (Tracked in Git)
Shared team configuration for Claude Code:
- Project metadata
- Permissions for common development tasks
- Context optimization strategies
- Development tooling preferences

### `settings.local.json` (Not Tracked)
Local overrides for individual developers:
- Personal API keys
- Local paths
- Machine-specific permissions
- Experimental features

Settings are merged with local overrides taking precedence.

## Token Optimization

The project uses several strategies to optimize Claude Code's token consumption:

1. **`.claudeignore`** - Excludes high-token-cost files:
   - Build artifacts and caches
   - Virtual environments
   - Test coverage reports
   - JSON scan results
   - IDE files

2. **Context Prioritization** - `settings.json` specifies:
   - Primary files: CLAUDE.md, README.md, pyproject.toml
   - Important directories: rankle/core, rankle/detectors, etc.

3. **Targeted Operations**:
   - Use specific file reads instead of full directory scans
   - Focus on changed files in git operations
   - Summarize large dependency files

## Best Practices (2026)

1. **Version Control**:
   - ✅ Track `settings.json` (shared config)
   - ❌ Don't track `settings.local.json` (personal config)
   - ❌ Don't track `cache/` or `logs/` directories

2. **Permissions**:
   - Allow development tools (python, pip, git, ruff, mypy)
   - Allow research sources (portswigger.net, owasp.org, github.com)
   - Restrict dangerous operations (unless explicitly needed)

3. **Context Management**:
   - Use `.claudeignore` to reduce noise
   - Specify primary documentation files
   - Identify critical code directories

4. **Token Budget**:
   - Conservative mode for large codebases
   - Aggressive mode for small focused work
   - Balance between context and cost

## Usage

Claude Code automatically reads configuration from this directory.

To override settings locally:
```bash
cp settings.json settings.local.json
# Edit settings.local.json with your overrides
```

## Documentation

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Configuration Reference](https://docs.anthropic.com/claude-code/configuration)
- [Token Optimization Guide](https://docs.anthropic.com/claude-code/optimization)

---

**Last Updated:** 2026-01-20
**Maintained By:** Claude Code + Human collaboration
