# -*- coding: utf-8 -*-
from mccc.monte_carlo import run
from mccc.monte_carlo import simulate_single_history
from mccc.setup import initialise_tallies
from mccc.setup import setup_simulation


def test_simulate_single_history():
    tallies = initialise_tallies()
    initial_data = setup_simulation()
    start_positions = [0.0]

    tallies, new_start_positions = simulate_single_history(
        initial_data, tallies, start_positions
    )


def test_run():
    run(1, 1000, plot=False)
