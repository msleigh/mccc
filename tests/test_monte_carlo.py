# -*- coding: utf-8 -*-
from mccc.monte_carlo import run
from mccc.monte_carlo import simulate_single_history
from mccc.setup import initialise_tallies
from mccc.setup import setup_simulation


def test_simulate_single_history():
    tallies = initialise_tallies()
    cfg = setup_simulation()
    start_positions = [0.0]

    tallies, new_start_positions = simulate_single_history(
        cfg, tallies, start_positions[0]
    )
    assert tallies["history"] == 1
    assert isinstance(new_start_positions, list)
    assert start_positions == [0.0]


def test_run():
    run(1, 1000, plot=False)


def test_run_reproducible_with_seed():
    k1_a, k2_a = run(2, 1000, plot=False, random_seed=12345)
    k1_b, k2_b = run(2, 1000, plot=False, random_seed=12345)
    assert k1_a == k1_b
    assert k2_a == k2_b
