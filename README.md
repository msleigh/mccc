# mccc

[![PyPI](https://img.shields.io/pypi/v/mccc.svg)](https://pypi.org/project/mccc/)
[![Changelog](https://img.shields.io/github/v/release/msleigh/mccc?include_prereleases&label=changelog)](https://github.com/msleigh/mccc/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/msleigh/mccc/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Monte Carlo criticality code

---

## Requirements

mccc requires Python 3.10+. It is tested on macOS.

## Installation

mccc is published as a Python package and can be installed with `pip`,
ideally by using a virtual environment. Open up a terminal and install with:

    pip install mccc

## Configuration

Configuration instructions go here.

## Usage

To run with all defaults:

    mccc

See the `commands.txt` for some example commands. Full documentation is [here](https://msleigh.io).

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
