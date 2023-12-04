# -*- coding: utf-8 -*-
from mccc.geometry import handle_boundary_conditions
from mccc.geometry import update_neutron_position


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
    current_position = 8.0
    left_boundary_condition = "reflective"

    # Move right
    mu = 1.0

    ### Stay in slab
    scatter_distance = 1.0
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        mu,
        left_boundary_condition,
        scatter_distance,
    )
    assert 0 <= new_position <= slab_thickness_cm

    ### Leave slab
    scatter_distance = 3.0
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        mu,
        left_boundary_condition,
        scatter_distance,
    )
    assert new_position == -1

    # Move left
    mu = -1.0

    ## Reflective boundary

    ### Stay in slab
    scatter_distance = 1.0
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        mu,
        left_boundary_condition,
        scatter_distance,
    )
    assert 0 <= new_position <= slab_thickness_cm

    ### Cross boundary
    scatter_distance = 9.0
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        mu,
        left_boundary_condition,
        scatter_distance,
    )
    assert 0 <= new_position <= slab_thickness_cm

    ### Leave slab
    scatter_distance = 20.0
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        mu,
        left_boundary_condition,
        scatter_distance,
    )
    assert new_position == -1

    ## Transmissive boundary
    left_boundary_condition = "transmissive"

    ### Stay in slab
    scatter_distance = 1.0
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        mu,
        left_boundary_condition,
        scatter_distance,
    )
    assert 0 <= new_position <= slab_thickness_cm

    ### Leave slab
    scatter_distance = 9.0
    new_position = update_neutron_position(
        current_position,
        slab_thickness_cm,
        mu,
        left_boundary_condition,
        scatter_distance,
    )
    assert new_position == -1
