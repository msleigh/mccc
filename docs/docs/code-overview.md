# Code Overview

## Package structure

- `mccc/monte_carlo.py`: top-level simulation logic and CLI entrypoint.
- `mccc/setup.py`: dataclass-based configuration and tallies.
- `mccc/sampling.py`: random sampling routines for directions, reactions, and
  distances.
- `mccc/geometry.py`: neutron transport and boundary-condition handling.
- `mccc/plotting.py`: plotting helpers for study outputs.

## Execution flow

A typical run (`run`) performs the following:

1. Builds a `Config` object using defaults and user overrides.
2. Samples initial neutron starting positions in the slab.
3. Loops over generations.
4. For each particle history, repeatedly samples direction and collision
   distance.
5. Applies geometry and boundary updates.
6. Samples interaction type (`scatter`, `fission`, `capture`).
7. Tallies events and collects next-generation source positions.
8. Computes `k_eff` estimators (`k1`, `k2`) per generation.

At the particle-history level (`simulate_single_history`), each neutron is
tracked until one terminating event occurs:

- leakage from the slab
- capture
- fission

Scatter events continue the same history and increment the collision/secondary
tallies.

## Key data models

`Config` in `mccc/setup.py` contains:

- Independent inputs: number of generations/particles, slab thickness, cross
  sections, `nu`, and boundary condition.
- Derived values: `mean_free_path`, `scatter_prob`, and `fission_prob`
  (computed in `__post_init__`).

Tallies are stored as a dict with counters such as `collision`, `scatter`,
`fission`, `capture`, `leakage`, `history`, and `secondary`.

## Estimators

The code tracks two generation-wise estimators:

1. Collision/loss-based estimator:
   `k1 = nu * N_fission / (N_capture + N_leakage + N_fission)`
2. Population-ratio estimator:
   `k2 = N_(g+1) / N_g`

Using multiple generations is important because a single generation started
from a uniform source does not represent the steady fission source shape.

## CLI entrypoint

The `mccc` command maps to `mccc.monte_carlo:main` and supports:

- default run
- convergence study (`-t convergence`)
- generations study (`-t generations`)
- fission-rate study (`-t fission_rate`)
