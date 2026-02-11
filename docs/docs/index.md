# mccc

`mccc` is a Monte Carlo criticality code for a 1D slab model.

## What this project does

- Simulates neutron histories across generations in a slab geometry.
- Estimates effective multiplication factor (`k_eff`) using two estimators.
- Generates plots for convergence, generation behavior, and fission-rate
  shape.

## Background

The implementation and modeling choices are documented in the original project
write-up:

- A toy Monte Carlo criticality code (December 21, 2023), copied in this repo
  as `monte_carlo_criticality_code.md`.

This docs site summarizes and updates that content around the current codebase.

## Documentation map

- [Getting Started](getting-started.md): prerequisites, installation, and first
  run.
- [Testing](testing.md): running and understanding the test suite.
- [Code Overview](code-overview.md): package architecture and execution flow.
- [Model and Results](model-and-results.md): transport assumptions,
  estimators, and convergence behavior.
- [CLI Usage](cli-usage.md): command-line interface and examples.

## Quick start

```bash
uv sync --extra docs --extra tests --extra dev
uv run pytest
uv run mccc -g 6 -p 128000 -t generations
```

Generated plots are written to the current working directory.
