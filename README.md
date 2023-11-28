# mccc

[![PyPI](https://img.shields.io/pypi/v/mccc.svg)](https://pypi.org/project/mccc/)
[![Changelog](https://img.shields.io/github/v/release/msleigh/mccc?include_prereleases&label=changelog)](https://github.com/msleigh/mccc/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/msleigh/mccc/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Monte Carlo criticality code

---

## Requirements

mccc requires Python 3.7+. It is tested on Linux and macOS.

## Installation

mccc is published as a Python package and can be installed with `pip`,
ideally by using a virtual environment. Open up a terminal and install with:

    pip install mccc

## Configuration

Configuration instructions go here.

## Usage

Usage instructions go here.

## Development

To contribute to this library, first checkout the code. Then create a new
virtual environment:

    cd mccc
    python -m venv .venv
    source .venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
