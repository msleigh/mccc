# Testing

## Test prerequisites

Install with test dependencies:

```bash
uv sync --extra tests
```

If you also want docs checks and lint tooling:

```bash
uv sync --extra docs --extra tests --extra dev
```

## Run tests

```bash
uv run pytest
```

Run a specific test module:

```bash
uv run pytest tests/test_sampling.py
```

## Notes on stochastic behavior

This project is Monte Carlo based, but the current tests are written as
property/behavior checks (ranges, invariants, and error handling), not strict
numerical regression tests. That keeps the suite robust across platforms and
Python versions.

## What is covered

Current tests validate core behavior in:

- `mccc/sampling.py`: random sampling helpers.
- `mccc/geometry.py`: boundary handling and position updates.
- `mccc/setup.py`: configuration defaults and tally initialization.
- `mccc/monte_carlo.py`: basic simulation execution paths.

## CI behavior

GitHub Actions runs tests on Python 3.10, 3.11, and 3.12, and also performs a
docs build.
