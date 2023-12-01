# -*- coding: utf-8 -*-
from mccc.monte_carlo import handle_boundary_conditions
from mccc.monte_carlo import initialise_tallies
from mccc.monte_carlo import main
from mccc.monte_carlo import sample_direction_cosine
from mccc.monte_carlo import sample_interaction_type
from mccc.monte_carlo import sample_scattering_distance
from mccc.monte_carlo import setup_simulation
from mccc.monte_carlo import simulate_single_history
from mccc.monte_carlo import update_neutron_position


def test_setup_simulation_default():
    """
    Test the setup_simulation function.
    """
    # Test the default setup with no arguments
    initial_data = setup_simulation()

    assert "num_particles" in initial_data
    assert "slab_thickness_cm" in initial_data
    assert "total_xs" in initial_data
    assert "scattering_xs" in initial_data
    assert "fission_xs" in initial_data
    assert "left_boundary_condition" in initial_data

    # Assuming the default values
    assert initial_data["num_particles"] == 10000
    assert initial_data["slab_thickness_cm"] == 1.853722
    assert initial_data["total_xs"] == 0.326400
    assert initial_data["scattering_xs"] == 0.225216
    assert initial_data["fission_xs"] == 0.0816
    assert initial_data["left_boundary_condition"] == "reflective"


def test_setup_simulation_custom():
    """
    Test the setup_simulation function.
    """
    # Test setup with custom parameters
    custom_num_particles = 500
    custom_slab_thickness_cm = 15.0
    custom_total_xs = 0.15
    custom_scattering_xs = 0.07
    custom_fission_xs = 0.03
    custom_boundary_condition = "transmissive"
    initial_data_custom = setup_simulation(
        num_particles=custom_num_particles,
        slab_thickness_cm=custom_slab_thickness_cm,
        total_xs=custom_total_xs,
        scattering_xs=custom_scattering_xs,
        fission_xs=custom_fission_xs,
        left_boundary_condition=custom_boundary_condition,
    )

    assert "num_particles" in initial_data_custom
    assert "slab_thickness_cm" in initial_data_custom
    assert "total_xs" in initial_data_custom
    assert "scattering_xs" in initial_data_custom
    assert "fission_xs" in initial_data_custom
    assert "left_boundary_condition" in initial_data_custom

    assert initial_data_custom["num_particles"] == custom_num_particles
    assert initial_data_custom["slab_thickness_cm"] == custom_slab_thickness_cm
    assert initial_data_custom["total_xs"] == custom_total_xs
    assert initial_data_custom["scattering_xs"] == custom_scattering_xs
    assert initial_data_custom["fission_xs"] == custom_fission_xs
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
    assert "absorption" in tallies

    assert tallies["collision"] == 0
    assert tallies["scatter"] == 0
    assert tallies["fission"] == 0
    assert tallies["leakage"] == 0
    assert tallies["history"] == 0
    assert tallies["absorption"] == 0


def test_sample_interaction_type():
    """
    Test the sample_interaction_type function.
    """
    total_xs = 0.1
    scattering_xs = 0.05
    fission_xs = 0.02

    # Ensure the function returns a valid interaction type
    interaction_type = sample_interaction_type(total_xs, scattering_xs, fission_xs)
    assert interaction_type in {"scatter", "fission", "absorption"}

    # Ensure the function returns 'scattering' within the scattering probability
    interaction_type = sample_interaction_type(
        total_xs, scattering_xs, fission_xs, rand_num=scattering_xs / total_xs - 1e-10
    )
    assert interaction_type == "scatter"

    # Ensure the function returns 'fission' within the fission probability
    interaction_type = sample_interaction_type(
        total_xs,
        scattering_xs,
        fission_xs,
        rand_num=(scattering_xs + fission_xs) / total_xs - 1e-10,
    )
    assert interaction_type == "fission"

    # Ensure the function returns 'absorption' for values close to or beyond 1.0
    interaction_type = sample_interaction_type(
        total_xs, scattering_xs, fission_xs, rand_num=1.0 - 1e-10
    )
    assert interaction_type == "absorption"


def test_sample_direction_cosine():
    """
    Test the sample_direction_cosine function.
    """
    # Ensure the function returns a valid direction cosine
    mu = sample_direction_cosine()
    assert -1 <= mu <= 1

    # Ensure the function returns different values for multiple calls
    mu1 = sample_direction_cosine()
    mu2 = sample_direction_cosine()
    assert mu1 != mu2

    # Ensure the function returns values within the specified range
    num_samples = 1000
    mu_values = [sample_direction_cosine() for _ in range(num_samples)]
    assert all(-1 <= mu <= 1 for mu in mu_values)


def test_sample_scattering_distance():
    """
    Test the sample_scattering_distance function.
    """
    total_xs = 0.1

    # Ensure the function returns a positive distance
    distance = sample_scattering_distance(total_xs)
    assert distance > 0

    # Ensure the function returns different values for multiple calls
    distance1 = sample_scattering_distance(total_xs)
    distance2 = sample_scattering_distance(total_xs)
    assert distance1 != distance2

    num_samples = 1000
    distance_values = [sample_scattering_distance(total_xs) for _ in range(num_samples)]
    assert all(distance > 0 for distance in distance_values)


def test_handle_reflective_boundary_conditions():
    """
    Test the handle_boundary_conditions function.
    """
    slab_thickness_cm = 10.0

    # Test reflective boundary condition
    boundary_condition = "reflective"

    # Neutron inside the slab
    new_position = handle_boundary_conditions(
        5.0, slab_thickness_cm, boundary_condition
    )
    assert 0 <= new_position <= slab_thickness_cm

    # Neutron at the left boundary
    new_position = handle_boundary_conditions(
        0.0, slab_thickness_cm, boundary_condition
    )
    assert 0 <= new_position <= slab_thickness_cm

    # Neutron beyond the left boundary
    new_position = handle_boundary_conditions(
        -2.0, slab_thickness_cm, boundary_condition
    )
    assert 0 <= new_position <= slab_thickness_cm

    # Neutron at the right boundary
    new_position = handle_boundary_conditions(
        10.0, slab_thickness_cm, boundary_condition
    )
    assert 0 <= new_position <= slab_thickness_cm

    # Neutron beyond the right boundary
    new_position = handle_boundary_conditions(
        11.0, slab_thickness_cm, boundary_condition
    )
    assert new_position < 0.0


def test_handle_transmissive_boundary_conditions():
    """
    Test the handle_boundary_conditions function.
    """
    slab_thickness_cm = 10.0

    # Test transmissive boundary condition
    boundary_condition = "transmissive"

    # Neutron inside the slab
    new_position = handle_boundary_conditions(
        5.0, slab_thickness_cm, boundary_condition
    )
    assert 0 <= new_position <= slab_thickness_cm

    # Neutron at the left boundary
    new_position = handle_boundary_conditions(
        0.0, slab_thickness_cm, boundary_condition
    )
    assert 0 <= new_position <= slab_thickness_cm

    # Neutron beyond the left boundary
    new_position = handle_boundary_conditions(
        -2.0, slab_thickness_cm, boundary_condition
    )
    assert new_position < 0.0

    # Neutron at the right boundary
    new_position = handle_boundary_conditions(
        10.0, slab_thickness_cm, boundary_condition
    )
    assert 0 <= new_position <= slab_thickness_cm

    # Neutron beyond the right boundary
    new_position = handle_boundary_conditions(
        11.0, slab_thickness_cm, boundary_condition
    )
    assert new_position < 0.0


def test_handle_unknown_boundary_conditions():
    """
    Test the handle_boundary_conditions function.
    """
    slab_thickness_cm = 10.0
    # Test unknown boundary condition (raises an error)
    boundary_condition = "unknown"
    try:
        handle_boundary_conditions(0.0, slab_thickness_cm, boundary_condition)
    except ValueError as e:
        assert str(e) == f"Unknown boundary condition: {boundary_condition}"
    else:
        assert False, "Expected a ValueError for unknown boundary condition"


def test_update_neutron_position():
    """
    Test the update_neutron_position function.
    """
    slab_thickness_cm = 10.0
    total_xs = 0.3
    direction_cosine = 0.5
    left_boundary_condition = "reflective"

    # Test absorption interaction
    current_position = 8.0
    interaction_type = "absorption"
    try:
        new_position = update_neutron_position(
            current_position,
            slab_thickness_cm,
            interaction_type,
            direction_cosine,
            left_boundary_condition,
            total_xs,
        )
    except ValueError as e:
        assert str(e) == f"Unknown interaction type: {interaction_type}"
    else:
        assert False, "Expected a ValueError for updating position after absorption"

    # Test fission interaction
    current_position = 2.0
    interaction_type = "fission"
    try:
        new_position = update_neutron_position(
            current_position,
            slab_thickness_cm,
            interaction_type,
            direction_cosine,
            left_boundary_condition,
            total_xs,
        )
    except ValueError as e:
        assert str(e) == f"Unknown interaction type: {interaction_type}"
    else:
        assert False, "Expected a ValueError for updating position after fission"

    # Test scattering interaction
    current_position = 1.0
    interaction_type = "scatter"
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        interaction_type,
        direction_cosine,
        left_boundary_condition,
        total_xs,
    )
    assert 0 <= new_position <= slab_thickness_cm or new_position == -1

    # Test boundary conditions (transmissive)
    left_boundary_condition = "transmissive"
    current_position = 0.5
    interaction_type = "scatter"
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        interaction_type,
        direction_cosine,
        left_boundary_condition,
        total_xs,
    )
    assert 0 <= new_position <= slab_thickness_cm or new_position == -1


def test_simulate_single_history():
    tallies = initialise_tallies()
    initial_data = setup_simulation()
    next_gen_start_locs = 0

    tallies = simulate_single_history(initial_data, tallies, next_gen_start_locs)


def test_main():
    main()
