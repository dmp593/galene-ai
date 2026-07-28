# galene-ai — developer commands. Run `make` (or `make help`) to list them.
# Everything runs through `uv`. First time: `make dev`.

.DEFAULT_GOAL := help
.PHONY: help dev test test-live cov lint format format-check type check drift models registry build publish publish-test clean

PY ?= 3.13   # dev interpreter (3.12+ supported); 3.14 may lack prebuilt wheels

# Publish tokens. PyPI and TestPyPI disabled username/password uploads — you
# MUST use an API token (sent as username `__token__`, which `uv publish
# --token` handles for you). They are DIFFERENT accounts, so you need one token
# each. Read from the environment, falling back to `.env` (gitignored). Get them:
#   PyPI:     https://pypi.org/manage/account/token/
#   TestPyPI: https://test.pypi.org/manage/account/token/
PYPI_TOKEN      ?= $(shell grep -E '^PYPI_TOKEN=' .env 2>/dev/null | cut -d= -f2-)
TEST_PYPI_TOKEN ?= $(shell grep -E '^TEST_PYPI_TOKEN=' .env 2>/dev/null | cut -d= -f2-)

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

dev:  ## Create the dev venv (Python $(PY)) and install the package + dev tools
	uv venv --python $(PY)
	uv pip install -e ".[dev]"

test:  ## Run the unit test suite (live tests excluded)
	uv run pytest -q

test-live:  ## Run the LIVE integration tests against a real backend (needs GALENE_AI_API_KEY + GALENE_AI_BASE_URL)
	uv run pytest -m live -q

cov:  ## Run tests with a coverage report
	uv run pytest --cov=galene_ai --cov-report=term-missing -q

lint:  ## Lint with ruff
	uv run ruff check .

format:  ## Auto-format with ruff
	uv run ruff format .

format-check:  ## Check formatting without changing files
	uv run ruff format --check .

type:  ## Type-check with mypy (strict)
	uv run mypy

check: lint format-check type test  ## Run the full gate: lint + format-check + type + test

drift:  ## Verify the SDK still covers every spec operation (regenerate registry + run drift test)
	uv run python scripts/build_registry.py
	@git diff --quiet spec/operations.json || (echo "spec/operations.json changed — the API drifted; review + commit" && exit 1)
	uv run pytest tests/test_drift.py -q

models:  ## Regenerate the committed msgspec models from the vendored spec
	uv run python scripts/generate_models.py

registry:  ## Regenerate spec/operations.json (namespace registry) from the spec
	uv run python scripts/build_registry.py

build: clean  ## Build the wheel + sdist into dist/
	uv build

publish: build  ## Upload dist/* to PyPI (needs PYPI_TOKEN in .env or the environment)
	@test -n "$(PYPI_TOKEN)" || { echo "PYPI_TOKEN not set. Add it to .env — get one at https://pypi.org/manage/account/token/"; exit 1; }
	@uv publish --token "$(PYPI_TOKEN)"  # @ so make doesn't echo the token

publish-test: build  ## Upload dist/* to TestPyPI (needs TEST_PYPI_TOKEN in .env or the environment)
	@test -n "$(TEST_PYPI_TOKEN)" || { echo "TEST_PYPI_TOKEN not set. Add it to .env — get one at https://test.pypi.org/manage/account/token/"; exit 1; }
	@uv publish --publish-url https://test.pypi.org/legacy/ --token "$(TEST_PYPI_TOKEN)"  # @ so make doesn't echo the token

clean:  ## Remove build artifacts and tool caches
	rm -rf dist build ./*.egg-info src/*.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -not -path './.venv/*' -prune -exec rm -rf {} + 2>/dev/null || true
