# -*- coding: utf-8 -*-
from mccc.setup import initialise_tallies
from mccc.setup import setup_simulation
from mccc.setup import update_user_input


def test_setup_simulation():
    """
    Test the setup_simulation function.
    """
    # Test the default setup with no arguments (or None where arguments are
    # required)
    initial_data = setup_simulation()

    assert hasattr(initial_data, "num_generations")
    assert hasattr(initial_data, "num_particles")
    assert hasattr(initial_data, "slab_thickness_cm")
    assert hasattr(initial_data, "mean_free_path")
    assert hasattr(initial_data, "scatter_prob")
    assert hasattr(initial_data, "fission_prob")
    assert hasattr(initial_data, "nu")
    assert hasattr(initial_data, "left_boundary_condition")

    # Assuming the default values
    assert initial_data.num_generations == 4
    assert initial_data.num_particles == 128000
    assert initial_data.slab_thickness_cm == 1.853722
    assert initial_data.mean_free_path == 1 / 0.326400
    assert initial_data.scatter_prob == 0.225216 / 0.326400
    assert initial_data.fission_prob == 0.0816 / 0.326400
    assert initial_data.nu == 3.24
    assert initial_data.left_boundary_condition == "reflective"


def test_update_user_input():
    """
    Test the setup_simulation function.
    """
    # Test setup with custom parameters
    num_generations = 5
    num_particles = 500
    slab_thickness_cm = 15.0
    total_xs = 0.15
    scatter_xs = 0.07
    fission_xs = 0.03
    nu = 3.24
    left_boundary_condition = "transmissive"

    initial_data_custom = setup_simulation()
    user_input = {
        k: v
        for k, v in locals().items()
        if k in initial_data_custom.__annotations__ and v is not None
    }
    initial_data_custom = update_user_input(initial_data_custom, user_input)

    assert hasattr(initial_data_custom, "num_generations")
    assert hasattr(initial_data_custom, "num_particles")
    assert hasattr(initial_data_custom, "slab_thickness_cm")
    assert hasattr(initial_data_custom, "mean_free_path")
    assert hasattr(initial_data_custom, "scatter_prob")
    assert hasattr(initial_data_custom, "fission_prob")
    assert hasattr(initial_data_custom, "nu")
    assert hasattr(initial_data_custom, "left_boundary_condition")

    # Assuming the default values
    assert initial_data_custom.num_generations == num_generations
    assert initial_data_custom.num_particles == num_particles
    assert initial_data_custom.slab_thickness_cm == slab_thickness_cm
    assert initial_data_custom.mean_free_path == 1 / total_xs
    assert initial_data_custom.scatter_prob == scatter_xs / total_xs
    assert initial_data_custom.fission_prob == fission_xs / total_xs
    assert initial_data_custom.nu == nu
    assert initial_data_custom.left_boundary_condition == left_boundary_condition


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
