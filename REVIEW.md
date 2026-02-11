# Repository Review: mccc

## Summary

**mccc** is a Monte Carlo criticality code that simulates neutron transport
in a 1D slab geometry to estimate the effective multiplication factor
(k\_eff). The codebase is small (~570 lines of Python across 5 modules),
well-structured, and at an early stage (v0.0.1).

All 14 tests pass. The project has a functional CI pipeline and is published
on PyPI.

---

## Strengths

- **Clean modular design.** Simulation logic, geometry, sampling, plotting,
  and configuration are separated into focused modules with clear
  responsibilities.
- **Good use of dataclasses.** The `Config` class in `setup.py` uses
  `__post_init__` to derive dependent parameters automatically, which keeps
  the configuration consistent.
- **Comprehensive pre-commit setup.** Trailing whitespace, import ordering,
  YAML linting, Black, Ruff, and more are all enforced.
- **CI/CD pipeline.** Tests run on push/PR across Python 3.9-3.11, and
  publishing to PyPI is automated on release.
- **Reasonable test coverage.** Geometry, sampling, and setup modules have
  good unit test coverage.

---

## Issues

### Bugs

1. **`start_positions` list mutation via `pop()` in `simulate_single_history`**
   (`monte_carlo.py:37`). The function pops from the shared `start_positions`
   list, which is a side effect. If the list runs out of elements before all
   particles are processed (e.g. due to a logic error or configuration
   mismatch), this will raise an `IndexError` with no informative message.

1. **Reflective boundary logic is incomplete** (`geometry.py:21-23`). The
   current reflective boundary does `abs(new_position)`, which correctly
   handles a single reflection at `x=0`. However, if `abs(new_position) >
   slab_thickness_cm`, the neutron is flagged as leaked (`-1`). In reality, a
   reflective boundary should bounce the neutron back regardless of how far
   past `x=0` it goes - only leakage at the right boundary
   (`x=slab_thickness`) should cause loss. A neutron at position `-12` in a
   10 cm slab with a reflective left boundary would reflect to `+12`, which
   exceeds the slab and gets flagged as leaked, when physically it should
   undergo multiple reflections.

### Code Quality

1. **Mixed RNG usage.** `sampling.py` uses both `random` (stdlib) and
   `numpy.random`. This means reproducibility via seed-setting requires
   seeding both RNGs. Consolidating on one RNG (preferably `numpy`) would
   simplify reproducibility.

1. **No seed control.** There is no mechanism to set a random seed for
   reproducible runs. For a Monte Carlo code, this is important for
   debugging, validation, and regression testing.

1. **Hardcoded `verbose = False`** (`monte_carlo.py:153`). The verbose
   debug block and sanity checks are dead code that can never execute.
   This should either be a CLI flag or removed.

1. **Hardcoded `n = 10` in `trial()`** (`monte_carlo.py:200`). The number
   of independent runs per trial is not configurable, making it difficult
   to adjust for faster testing or more thorough averaging.

1. **`sys.exit()` for error handling** (`monte_carlo.py:142,187`). Using
    `sys.exit()` makes the code untestable and unfriendly as a library.
    Raising exceptions would be more appropriate.

1. **`run()` uses `locals()` for parameter passing** (`monte_carlo.py:92-96`).
    This is fragile - adding any local variable before that line (e.g. a
    comment typo fix that becomes an assignment) would silently inject it into
    the config update. Explicit parameter passing would be safer.

1. **Unused variable `c`** (`monte_carlo.py:151`). The variable `c` is
    computed but only used inside the `verbose` block, which is unreachable.

1. **Invalid escape sequences in `plotting.py`** (lines 50-51, 68-69).
    Strings like `"$k_{\mathrm{eff}}$"` contain `\m`, which Python warns
    about as an invalid escape sequence. These should use raw strings
    (`r"$k_{\mathrm{eff}}$"`).

1. **`plot_starting_positions` dual purpose** (`plotting.py:6-15`). When
    called with `starting_positions=None`, it saves the figure instead of
    plotting. This conflates "save the accumulated plot" with "plot data",
    making the function hard to understand.

### Testing

1. **Tests have no assertions on return values** (`test_monte_carlo.py:8-19`).
    `test_simulate_single_history` doesn't assert anything about the returned
    tallies or positions. `test_run` doesn't check the returned `k1, k2`
    values at all. These tests only verify the code doesn't crash.

1. **Non-deterministic test for randomness** (`test_sampling.py:20`).
    `assert mu1 != mu2` could theoretically fail (two random floats
    could be equal). While extremely unlikely, it's not a sound assertion.
    A better test would verify statistical properties over many samples.

1. **Missing test for `secondary` tally** (`test_setup.py:90-97`).
    `initialise_tallies()` returns 7 keys including `"secondary"`, but the
    test only checks 6 of them.

1. **No tests for `plotting.py`.** The plotting module is untested.

1. **No tests for `trial()`, `study_convergence()`, `study_generations()`,
    or `main()`.**

### Configuration & Packaging

1. **`pyproject.toml` has both `[tool.poetry]` and `[project]` sections.**
    The `[project]` section is incomplete (missing `name`, `version`, etc.)
    which is what causes the `pip install -e .` failure with newer Poetry
    versions. The `[project]` section should either be completed per PEP 621
    or removed if relying solely on Poetry metadata.

1. **`pip install -e '.[tests]'` fails.** Due to the `[project]` section
    issue above, the editable install fails with: *"project must contain
    ['name'] properties"*. This affects local development workflows.

1. **GitHub Actions uses outdated action versions.** `actions/checkout@v3`
    and `actions/setup-python@v4` are behind current versions (`v4` and `v5`
    respectively).

1. **No `pip cache` in test workflow** (`test.yml:20-21`). The test workflow
    specifies `cache-dependency-path` but doesn't enable `cache: pip` (unlike
    the publish workflow), resulting in slower CI runs.

### Documentation

1. **Incomplete docstrings.** `simulate_single_history` has empty
    `Parameters:` and `Returns:` sections. `update_user_input` has a
    copy-pasted docstring from `setup_simulation`.

1. **`docs/docs/index.md` is minimal.** The MkDocs documentation site has
    only a placeholder homepage.

---

## Recommended Priority

**High priority** (likely to cause failures):
- Fix `pyproject.toml` `[project]` section (#20, #21)
- Fix publish workflow (Python version matrix #4, `make` command #5)
- Fix `math.log(0)` potential crash (#1)
- Fix plotting escape sequences (#13) - these are deprecation warnings that
  will become errors in a future Python version

**Medium priority** (improve correctness and usability):
- Add seed control for reproducibility (#7)
- Consolidate RNG usage (#6)
- Replace `sys.exit` with exceptions (#10)
- Review reflective boundary multi-bounce logic (#3)
- Add meaningful assertions to MC tests (#15)

**Low priority** (cleanup):
- Remove or wire up `verbose` mode (#8)
- Make trial count configurable (#9)
- Improve test coverage (#17, #18, #19)
- Update GitHub Actions versions (#22)
