# =============================================================================
# Rankle - Web Infrastructure Reconnaissance Tool
# =============================================================================

UV      := uv
RUFF    := uv run ruff
PYRIGHT := uv run pyright
PYTEST  := uv run pytest

SRC     := src/rankle
MAIN    := main.py
DOMAIN  ?= example.com

.DEFAULT_GOAL := help

# =============================================================================
# Help
# =============================================================================

.PHONY: help
help:
	@echo "Rankle - Web Infrastructure Reconnaissance Tool"
	@echo ""
	@echo "Usage: make [target] [DOMAIN=<domain>]"
	@echo ""
	@echo "Setup"
	@echo "  install      Install dependencies (uv sync)"
	@echo "  hooks        Install pre-commit hooks"
	@echo ""
	@echo "Run"
	@echo "  start        Scan domain, print to terminal (DOMAIN=example.com)"
	@echo "  start-json   Scan domain, save JSON to reports/"
	@echo "  start-v      Scan domain, verbose output"
	@echo ""
	@echo "Quality"
	@echo "  lint         Run ruff linter (no auto-fix)"
	@echo "  lint-fix     Run ruff linter with auto-fix"
	@echo "  format       Run ruff formatter"
	@echo "  type-check   Run pyright type checker (strict)"
	@echo "  check        lint-fix + format + type-check"
	@echo ""
	@echo "Test"
	@echo "  test         Run full test suite with coverage"
	@echo "  test-fast    Run tests without coverage"
	@echo "  test-unit    Run unit tests only (skip slow/integration)"
	@echo "  coverage     Show coverage report (term + html)"
	@echo ""
	@echo "Clean"
	@echo "  clean        Remove all build artifacts, caches, temp files"
	@echo "  clean-all    Full clean including .venv"
	@echo ""
	@echo "Examples"
	@echo "  make start DOMAIN=github.com"
	@echo "  make start-json DOMAIN=github.com"

# =============================================================================
# Setup
# =============================================================================

.PHONY: install
install:
	$(UV) sync

.PHONY: hooks
hooks: install
	$(UV) run pre-commit install
	$(UV) run pre-commit install --hook-type commit-msg

# =============================================================================
# Run
# =============================================================================

.PHONY: start
start:
	$(UV) run python $(MAIN) $(DOMAIN)

.PHONY: start-json
start-json:
	$(UV) run python $(MAIN) $(DOMAIN) -o

.PHONY: start-v
start-v:
	$(UV) run python $(MAIN) $(DOMAIN) -v

# =============================================================================
# Code Quality
# =============================================================================

.PHONY: lint
lint:
	$(RUFF) check $(SRC)/ $(MAIN)

.PHONY: lint-fix
lint-fix:
	$(RUFF) check --fix $(SRC)/ $(MAIN)

.PHONY: format
format:
	$(RUFF) format $(SRC)/ $(MAIN)

.PHONY: type-check
type-check:
	$(PYRIGHT) $(SRC)/

.PHONY: check
check: lint-fix format type-check
	@echo "All checks passed."

# =============================================================================
# Test
# =============================================================================

.PHONY: test
test:
	$(PYTEST) -v --cov=$(SRC)

.PHONY: test-fast
test-fast:
	$(PYTEST) -v --no-cov

.PHONY: test-unit
test-unit:
	$(PYTEST) -v --cov=$(SRC) -m "not slow and not integration"

.PHONY: coverage
coverage:
	$(PYTEST) --cov=$(SRC) --cov-report=term-missing --cov-report=html:htmlcov
	@echo "HTML report: htmlcov/index.html"

# =============================================================================
# Pre-commit
# =============================================================================

.PHONY: pre-commit
pre-commit:
	$(UV) run pre-commit run --all-files

# =============================================================================
# Clean
# =============================================================================

.PHONY: clean
clean:
	find . -path ./.venv -prune -o -type d -name "__pycache__" -print -exec rm -rf {} + 2>/dev/null || true
	find . -path ./.venv -prune -o -type f -name "*.pyc" -print -delete 2>/dev/null || true
	find . -path ./.venv -prune -o -type f -name "*.pyo" -print -delete 2>/dev/null || true
	find . -path ./.venv -prune -o -name "*.egg-info" -print -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov dist build
	rm -f .coverage coverage.xml

.PHONY: clean-reports
clean-reports:
	rm -f reports/rankle_*.json

.PHONY: clean-all
clean-all: clean clean-reports
	rm -rf .venv
