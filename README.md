# mccc

[PyPI](https://pypi.org/project/mccc/) |
[Changelog](https://github.com/msleigh/mccc/releases) |
[License](https://github.com/msleigh/mccc/blob/main/LICENSE) |
[Black](https://github.com/python/black)

Monte Carlo criticality code

---

## Requirements

mccc requires Python 3.10+. It is tested on macOS.

## Installation

mccc is published as a Python package and can be installed with `pip`,
ideally by using a virtual environment. Open up a terminal and install with:

    pip install mccc

## Configuration

Use `--seed` to make Monte Carlo sampling reproducible:

    mccc -g 4 -p 128000 --seed 12345

## Usage

To run with all defaults:

    mccc

To run reproducibly:

    mccc -g 4 -p 128000 --seed 12345

See the `commands.txt` for some example commands.
Full documentation is available at <https://msleigh.io>.

## Development

To contribute to this library, first checkout the code. Then create a new
virtual environment:

    cd mccc
    uv sync --extra docs --extra tests --extra dev

Run commands via `uv run`:

To run the tests:

    uv run pytest

To build the documentation:

    uv run mkdocs build -f docs/mkdocs.yml

To launch a server to build, auto-update and serve the documentation:

    uv run mkdocs serve -f docs/mkdocs.yml
