# =============================================================================
# Rankle - Web Infrastructure Reconnaissance Tool
# =============================================================================

PYTHON      := python
UV          := uv
RUFF        := uv run ruff
MYPY        := uv run mypy
PYTEST      := uv run pytest
BANDIT      := uv run bandit
INTERROGATE := uv run interrogate

PACKAGE     := rankle
MAIN        := main.py
DOMAIN      ?= example.com
OUTPUT_DIR  := output
REPORTS_DIR := htmlcov

DOCKER_IMAGE   := rankle
DOCKER_TAG     := latest
DOCKER_VOLUME  := $(PWD)/output

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
	@echo "  install        Install dependencies (uv sync)"
	@echo "  install-dev    Install with dev extras"
	@echo "  install-all    Install with dev + extended extras"
	@echo "  hooks          Install pre-commit hooks"
	@echo ""
	@echo "Build"
	@echo "  build          Build distribution packages"
	@echo "  build-docker   Build Docker image"
	@echo ""
	@echo "Run"
	@echo "  start          Run scan (DOMAIN=example.com)"
	@echo "  start-json     Run scan, save JSON output"
	@echo "  start-verbose  Run scan, verbose output"
	@echo "  start-docker   Run scan via Docker"
	@echo ""
	@echo "Quality"
	@echo "  lint           Run ruff linter"
	@echo "  format         Run ruff formatter"
	@echo "  lint-fix       Run ruff linter with auto-fix"
	@echo "  type-check     Run mypy type checker"
	@echo "  security       Run bandit security scan"
	@echo "  docstrings     Run interrogate docstring coverage"
	@echo "  check          Run lint + format + type-check + security"
	@echo ""
	@echo "Test"
	@echo "  test           Run test suite with coverage"
	@echo "  test-fast      Run tests (no coverage)"
	@echo "  test-parallel  Run tests in parallel"
	@echo "  test-unit      Run unit tests only (skip slow/integration)"
	@echo ""
	@echo "Pre-commit"
	@echo "  pre-commit     Run all pre-commit hooks"
	@echo ""
	@echo "Clean"
	@echo "  clean          Remove build artifacts and caches"
	@echo "  clean-output   Remove scan output files"
	@echo "  clean-all      Full clean including .venv"
	@echo ""
	@echo "Examples"
	@echo "  make start DOMAIN=github.com"
	@echo "  make start-json DOMAIN=github.com"
	@echo "  make start-docker DOMAIN=github.com"

# =============================================================================
# Setup
# =============================================================================

.PHONY: install
install:
	$(UV) sync

.PHONY: install-dev
install-dev:
	$(UV) sync --extra dev

.PHONY: install-all
install-all:
	$(UV) sync --extra dev --extra extended

.PHONY: hooks
hooks: install-dev
	$(UV) run pre-commit install
	$(UV) run pre-commit install --hook-type commit-msg

# =============================================================================
# Build
# =============================================================================

.PHONY: build
build: install
	$(UV) build

.PHONY: build-docker
build-docker:
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

# =============================================================================
# Run
# =============================================================================

.PHONY: start
start:
	$(UV) run $(PYTHON) $(MAIN) $(DOMAIN)

.PHONY: start-json
start-json:
	@mkdir -p $(OUTPUT_DIR)
	$(UV) run $(PYTHON) $(MAIN) $(DOMAIN) -o json

.PHONY: start-verbose
start-verbose:
	$(UV) run $(PYTHON) $(MAIN) $(DOMAIN) -v

.PHONY: start-docker
start-docker: build-docker
	@mkdir -p $(DOCKER_VOLUME)
	docker run --rm -v $(DOCKER_VOLUME):/output $(DOCKER_IMAGE):$(DOCKER_TAG) $(DOMAIN)

# =============================================================================
# Code Quality
# =============================================================================

.PHONY: lint
lint:
	$(RUFF) check $(PACKAGE)/ $(MAIN)

.PHONY: lint-fix
lint-fix:
	$(RUFF) check --fix $(PACKAGE)/ $(MAIN)

.PHONY: format
format:
	$(RUFF) format $(PACKAGE)/ $(MAIN)

.PHONY: type-check
type-check:
	$(MYPY) $(PACKAGE)/

.PHONY: security
security:
	$(BANDIT) -c pyproject.toml -r $(PACKAGE)/ $(MAIN)

.PHONY: docstrings
docstrings:
	$(INTERROGATE) -v $(PACKAGE)/

.PHONY: check
check: lint format type-check security
	@echo "All checks passed."

# =============================================================================
# Test
# =============================================================================

.PHONY: test
test:
	$(PYTEST) -v --cov=$(PACKAGE)

.PHONY: test-fast
test-fast:
	$(PYTEST) -v --no-cov

.PHONY: test-parallel
test-parallel:
	$(PYTEST) -v --cov=$(PACKAGE) -n auto

.PHONY: test-unit
test-unit:
	$(PYTEST) -v --cov=$(PACKAGE) -m "not slow and not integration"

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
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete 2>/dev/null || true
	rm -rf $(REPORTS_DIR) .mypy_cache .ruff_cache dist build *.egg-info

.PHONY: clean-output
clean-output:
	rm -rf $(OUTPUT_DIR) rankle_*.json rankle_*.txt

.PHONY: clean-all
clean-all: clean clean-output
	rm -rf .venv

# =============================================================================
# Sprint Automation - Type Hints & Test Coverage (Phase 3 & 4)
# =============================================================================

.PHONY: coverage-report
coverage-report:
	@echo "Coverage Report (Line-by-line missing):"
	$(PYTEST) --cov=$(PACKAGE) --cov-report=term-missing --cov-report=html:htmlcov

.PHONY: coverage-html
coverage-html: coverage-report
	@echo "Opening coverage report in browser..."
	@if command -v xdg-open > /dev/null; then xdg-open htmlcov/index.html; elif command -v open > /dev/null; then open htmlcov/index.html; else echo "Open htmlcov/index.html in your browser"; fi

.PHONY: type-check-verbose
type-check-verbose:
	$(MYPY) $(PACKAGE)/ --show-error-codes --show-column-numbers

.PHONY: type-check-strict
type-check-strict:
	$(MYPY) $(PACKAGE)/ --strict

.PHONY: audit-quality
audit-quality: lint type-check-verbose security docstrings
	@echo ""
	@echo "Quality Audit Complete"
	@echo "  ✓ Linting (ruff)"
	@echo "  ✓ Type hints (mypy)"
	@echo "  ✓ Security (bandit)"
	@echo "  ✓ Docstrings (interrogate)"

.PHONY: coverage-target
coverage-target:
	@echo "Current coverage target: 70%"
	@echo "Recommended: pytest --cov=rankle --cov-fail-under=70"

.PHONY: phase-1-complete
phase-1-complete: clean install-dev hooks
	@echo ""
	@echo "✅ PHASE 1 COMPLETE: Setup & Infrastructure"
	@echo "  - Tests structure created"
	@echo "  - conftest.py with 30+ fixtures"
	@echo "  - .coveragerc configured"
	@echo "  - pytest threshold: 70%"

.PHONY: phase-2-test
phase-2-test: test
	@echo ""
	@echo "Phase 2 Status: Test Suite Implementation"
	@coverage report --skip-covered

.PHONY: phase-3-types
phase-3-types: type-check-verbose
	@echo ""
	@echo "Phase 3 Status: Type Hints Migration"

.PHONY: phase-4-docs
phase-4-docs: docstrings
	@echo ""
	@echo "Phase 4 Status: API Docstrings"

.PHONY: sprint-report
sprint-report:
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║      RANKLE MODERNIZATION SPRINT REPORT                    ║"
	@echo "╠════════════════════════════════════════════════════════════╣"
	@echo "║ Phase 1: Infrastructure Setup              [✅ COMPLETE]   ║"
	@echo "║ Phase 2: Test Suite (70%+ coverage)        [IN PROGRESS]  ║"
	@echo "║ Phase 3: Type Hints (90%+ coverage)        [PENDING]      ║"
	@echo "║ Phase 4: Docstrings (80%+ coverage)        [PENDING]      ║"
	@echo "╠════════════════════════════════════════════════════════════╣"
	@echo "║ Target: 72/100 → 85+/100 (2026 Compliant)                ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@make audit-quality
