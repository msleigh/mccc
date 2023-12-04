# -*- coding: utf-8 -*-
def setup_simulation(
    num_generations=10,
    num_particles=200000,
    slab_thickness_cm=1.853722,
    total_xs=0.326400,
    scatter_xs=0.225216,
    fission_xs=0.081600,
    nu=3.24,
    left_boundary_condition="reflective",
):
    """
    Function to perform the initial setup for the Monte Carlo simulation.

    Parameters:
    - num_generations (int): Number of generations of neutrons for the simulation.
    - num_particles (int): Number of particles for the simulation.
    - slab_thickness_cm (float): Thickness of the 1D slab in centimeters.
    - total_xs (float): Total macroscopic cross-section in cm^-1.
    - scatter_xs (float): Scattering macroscopic cross-section in cm^-1.
    - fission_xs (float): Fission macroscopic cross-section in cm^-1.
    - nu (float): Mean number of neutrons per fission.
    - left_boundary_condition (str): Boundary condition for the left-hand side of the
                                     slab ('reflective' or 'transmissive').

    Returns:
    - dict: A dictionary containing initial data and parameters.
    """

    # Calculate the mean free path (inverse of total cross-section) adjusted by the
    # direction cosine
    mean_free_path = 1 / total_xs
    scatter_prob = scatter_xs * mean_free_path
    fission_prob = fission_xs * mean_free_path

    initial_data = {
        "num_generations": num_generations,
        "num_particles": num_particles,
        "slab_thickness_cm": slab_thickness_cm,
        "mean_free_path": mean_free_path,
        "scatter_prob": scatter_prob,
        "fission_prob": fission_prob,
        "nu": nu,
        "left_boundary_condition": left_boundary_condition,
    }

    return initial_data


def initialise_tallies():
    """
    Function to initialise tallies for the Monte Carlo simulation.

    Returns:
    - dict: A dictionary containing initialised tally variables.
    """

    tally_data = {
        "collision": 0,
        "scatter": 0,
        "fission": 0,
        "leakage": 0,
        "history": 0,
        "capture": 0,
        "secondary": 0,
    }

    return tally_data
