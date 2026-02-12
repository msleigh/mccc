# Getting Started

## Prerequisites

- Python 3.10 or newer.
- [`uv`](https://docs.astral.sh/uv/) for environment and dependency management.
- A checkout of this repository.

Check versions:

```bash
python --version
uv --version
```

## Installation

From the repository root:

```bash
uv sync
```

For development (tests, docs, and tooling):

```bash
uv sync --extra docs --extra tests --extra dev
```

This creates and manages `.venv` automatically.

## Running the code

Run a default simulation:

```bash
uv run mccc -g 4 -p 128000
```

Run a reproducible simulation:

```bash
uv run mccc -g 4 -p 128000 --seed 12345
```

Run a convergence study:

```bash
uv run mccc -t convergence -g 1 -p 1000 -p 2000 -p 4000 -p 8000
```

Run a generation study:

```bash
uv run mccc -t generations -g 6 -p 128000
```

Run a fission-rate plot:

```bash
uv run mccc -t fission_rate -g 12 -p 1024000
```

## Default physical setup

The defaults in `mccc/setup.py` correspond to a homogeneous 1D slab transport
toy problem:

- `num_generations = 4`
- `num_particles = 128000`
- `slab_thickness_cm = 1.853722`
- `total_xs = 0.326400`
- `scatter_xs = 0.225216`
- `fission_xs = 0.081600`
- `nu = 3.24`
- `left_boundary_condition = "reflective"`
- `random_seed = None`

Derived values such as mean free path and reaction probabilities are computed
from those inputs.

## Building docs

```bash
uv run mkdocs build -f docs/mkdocs.yml
uv run mkdocs serve -f docs/mkdocs.yml
```
