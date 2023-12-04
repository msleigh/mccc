# -*- coding: utf-8 -*-


def handle_boundary_conditions(new_position, slab_thickness_cm, boundary_condition):
    """
    Function to handle boundary conditions for neutron position.

    Parameters:
    - new_position (float): Updated neutron position.
    - slab_thickness_cm (float): Thickness of the 1D slab in centimeters.
    - boundary_condition (str): Boundary condition for the left-hand side of the slab
                                ('reflective' or 'transmissive').

    Returns:
    - float: Updated neutron position considering boundary conditions.
    """

    if boundary_condition == "reflective":
        # Reflective boundary at x=0: neutron reflects back into the slab if it hits the
        # boundary
        return (
            abs(new_position) if abs(new_position) <= slab_thickness_cm else -1
        )  # Absorbed neutron flag
    elif boundary_condition == "transmissive":
        # Transmissive boundary: Neutron passes through the boundary and disappears
        return (
            new_position if 0 <= new_position <= slab_thickness_cm else -1
        )  # Absorbed neutron flag
    else:
        # Raise an error for unknown boundary conditions
        raise ValueError(f"Unknown boundary condition: {boundary_condition}")


def update_neutron_position(
    current_position,
    slab_thickness_cm,
    mu,
    left_boundary_condition,
    scatter_distance,
):
    """
    Function to update neutron position based on interaction type.

    Parameters:
    - current_position (float): Current neutron position in the slab.
    - slab_thickness_cm (float): Thickness of the 1D slab in centimeters.
    - mu (float): Direction cosine in x-direction.
    - left_boundary_condition (str): Boundary condition for the left-hand side of the
                                     slab ('reflective' or 'transmissive').

    Returns:
    - float: Updated neutron position.
    """

    # Compute new position after scattering
    new_position = current_position + scatter_distance * mu

    # Handle if the neutron crosses the slab boundaries
    return handle_boundary_conditions(
        new_position, slab_thickness_cm, left_boundary_condition
    )
