.PHONY: help all build develop test fmt lint typing clean clean-cargo check test-cargo format unit
UV ?= uv

all: develop ## Build and install the package in development mode (default target)

help: ## Show help for all available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

fmt: ## Format Rust code (cargo fmt)
	cargo fmt

test-cargo: ## Check and test Rust code (fmt --check, clippy, build, test)
	cargo fmt --all -- --check
	cargo clippy -- -D warnings
	cargo build --release
	cargo test --release

format: ## Auto-fix and format Python code (ruff)
	$(UV) run ruff check --fix
	$(UV) run ruff format

lint: ## Lint Python code (ruff + flake8)
	$(UV) run ruff check --exit-non-zero-on-fix
	$(UV) run ruff format --check --diff
	$(UV) run flake8 tests fast_collections benchmarks

typing: ## Type-check with mypy --strict
	$(UV) run mypy --strict fast_collections tests

build: ## Build the wheel package (maturin build --release)
	$(UV) run maturin build --release

develop: ## Install the package in development mode (maturin develop --release)
	$(UV) run maturin develop --release

unit: ## Run Python tests (pytest)
	$(UV) run pytest

clean-cargo: ## Clean Cargo artifacts (cargo clean)
	cargo clean

clean: clean-cargo ## Full clean: Cargo artifacts + built wheels
	rm -rf target/wheels

check: ## Run all code quality checks (fmt, lint, typing)
	$(MAKE) fmt
	$(MAKE) lint
	$(MAKE) typing

test: build unit check ## Full cycle: build, unit tests, and checks