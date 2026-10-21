# Benchmarks

Performance comparison of `fast_collections` implementations (Rust)
against pure-Python reference implementations with the same API.
Measurements are made with `pytest-benchmark`; each data structure
lives in its own subdirectory (`trie/`, more to come).

## How we test

Each operation (`insert` / `search` / `delete`) is benchmarked
separately on fresh data, so benchmark rounds never interfere with
each other. Implementations are compared head-to-head:
`fast_collections` vs a pure-Python reference exposing the same API.

Datasets are deterministic and committed to the repository. Each
structure generates its own data; for example:

```bash
uv run python benchmarks/trie/data/generate.py
```

## What we use

- `pytest-benchmark` — measurements and reports;
- `uv` — virtual environment and running commands;
- `maturin` — building the Rust extension.

## Running

```bash
uv sync --group bench
uv run maturin develop --release   # build the Rust extension
uv run pytest benchmarks/trie --benchmark-only -o "python_files=test_*.py bench_*.py"
```

The `-o "python_files=test_*.py bench_*.py"` override makes pytest collect
the `bench_*.py` files. It is not set globally so that regular unit-test
runs (`make test`) do not pick up benchmarks.

Useful pytest-benchmark flags:

- `--benchmark-group-by=group` — group the report by operation;
- `--benchmark-save=<name>` — save the results for later comparison;
- `--benchmark-compare=<name>` — compare against a saved run;
- `--benchmark-histogram` — render histograms.

## Results

Latest numbers and analysis are documented per structure under
[`docs/data-structures/`](../docs/data-structures/).