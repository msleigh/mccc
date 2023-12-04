# -*- coding: utf-8 -*-
from mccc.setup import initialise_tallies
from mccc.setup import setup_simulation


def test_setup_simulation_default():
    """
    Test the setup_simulation function.
    """
    # Test the default setup with no arguments
    initial_data = setup_simulation()

    assert "num_generations" in initial_data
    assert "num_particles" in initial_data
    assert "slab_thickness_cm" in initial_data
    assert "mean_free_path" in initial_data
    assert "scatter_prob" in initial_data
    assert "fission_prob" in initial_data
    assert "nu" in initial_data
    assert "left_boundary_condition" in initial_data

    # Assuming the default values
    assert initial_data["num_generations"] == 10
    assert initial_data["num_particles"] == 200000
    assert initial_data["slab_thickness_cm"] == 1.853722
    assert initial_data["mean_free_path"] == 1 / 0.326400
    assert initial_data["scatter_prob"] == 0.225216 / 0.326400
    assert initial_data["fission_prob"] == 0.0816 / 0.326400
    assert initial_data["nu"] == 3.24
    assert initial_data["left_boundary_condition"] == "reflective"


def test_setup_simulation_custom():
    """
    Test the setup_simulation function.
    """
    # Test setup with custom parameters
    custom_num_generations = 5
    custom_num_particles = 500
    custom_slab_thickness_cm = 15.0
    custom_total_xs = 0.15
    custom_scatter_xs = 0.07
    custom_fission_xs = 0.03
    custom_nu = 3.24
    custom_boundary_condition = "transmissive"
    initial_data_custom = setup_simulation(
        num_generations=custom_num_generations,
        num_particles=custom_num_particles,
        slab_thickness_cm=custom_slab_thickness_cm,
        total_xs=custom_total_xs,
        scatter_xs=custom_scatter_xs,
        fission_xs=custom_fission_xs,
        nu=custom_nu,
        left_boundary_condition=custom_boundary_condition,
    )

    assert "num_generations" in initial_data_custom
    assert "num_particles" in initial_data_custom
    assert "slab_thickness_cm" in initial_data_custom
    assert "mean_free_path" in initial_data_custom
    assert "scatter_prob" in initial_data_custom
    assert "fission_prob" in initial_data_custom
    assert "nu" in initial_data_custom
    assert "left_boundary_condition" in initial_data_custom

    assert initial_data_custom["num_generations"] == custom_num_generations
    assert initial_data_custom["num_particles"] == custom_num_particles
    assert initial_data_custom["slab_thickness_cm"] == custom_slab_thickness_cm
    assert initial_data_custom["mean_free_path"] == 1.0 / custom_total_xs
    assert initial_data_custom["scatter_prob"] == custom_scatter_xs / custom_total_xs
    assert initial_data_custom["fission_prob"] == custom_fission_xs / custom_total_xs
    assert initial_data_custom["nu"] == custom_nu
    assert initial_data_custom["left_boundary_condition"] == custom_boundary_condition


def test_initialise_tallies():
    """
    Test the initialise_tallies function.
    """
    # Initialise tallies
    tallies = initialise_tallies()

    # Check that all expected tallies are present and initialised to zero
    assert "collision" in tallies
    assert "scatter" in tallies
    assert "fission" in tallies
    assert "leakage" in tallies
    assert "history" in tallies
    assert "capture" in tallies

    assert tallies["collision"] == 0
    assert tallies["scatter"] == 0
    assert tallies["fission"] == 0
    assert tallies["leakage"] == 0
    assert tallies["history"] == 0
    assert tallies["capture"] == 0
