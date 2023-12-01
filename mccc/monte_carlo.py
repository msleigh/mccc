# -*- coding: utf-8 -*-
import math
import random

import matplotlib.pyplot as plt
import numpy as np


def setup_simulation(
    num_particles=1000000,
    slab_thickness_cm=1.853722,
    total_xs=0.326400,
    scatter_xs=0.225216,
    fission_xs=0.081600,
    left_boundary_condition="reflective",
):
    """
    Function to perform the initial setup for the Monte Carlo simulation.

    Parameters:
    - num_particles (int): Number of particles for the simulation.
    - slab_thickness_cm (float): Thickness of the 1D slab in centimeters.
    - total_xs (float): Total macroscopic cross-section in cm^-1.
    - scatter_xs (float): Scattering macroscopic cross-section in cm^-1.
    - fission_xs (float): Fission macroscopic cross-section in cm^-1.
    - left_boundary_condition (str): Boundary condition for the left-hand side of the
                                     slab ('reflective' or 'transmissive').

    Returns:
    - dict: A dictionary containing initial data and parameters.
    """

    print(fission_xs)
    print(total_xs - scatter_xs - fission_xs)
    print(total_xs * slab_thickness_cm)
    print((scatter_xs + 3.24 * fission_xs) / total_xs)

    initial_data = {
        "num_particles": num_particles,
        "slab_thickness_cm": slab_thickness_cm,
        "total_xs": total_xs,
        "scatter_xs": scatter_xs,
        "fission_xs": fission_xs,
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
        "leakage": 0,  # Include leakage tally
        "history": 0,
        "capture": 0,
        "secondary": 0,
    }

    return tally_data


def sample_position(slab_thickness_cm):
    """
    Function to sample the initial position of a neutron within the slab.

    Parameters:
    - slab_thickness_cm (float): Thickness of the 1D slab in centimeters.

    Returns:
    - float: Initial position of the neutron within the slab.
    """
    # Sample a random initial position within the slab
    return random.uniform(0, slab_thickness_cm)


def sample_interaction_type(total_xs, scatter_xs, fission_xs, rand_num=None):
    """
    Function to sample an interaction type based on cross-sections.

    Parameters:
    - total_xs (float): Total macroscopic cross-section in cm^-1.
    - scatter_xs (float): Scattering macroscopic cross-section in cm^-1.
    - fission_xs (float): Fission macroscopic cross-section in cm^-1.

    Returns:
    - str: Interaction type ('scatter', 'fission', 'capture').
    """

    scatter_prob = scatter_xs / total_xs
    fission_prob = fission_xs / total_xs

    # Sample a random number between 0 and 1
    if rand_num is None:
        rand_num = random.uniform(0, 1)

    if rand_num < scatter_prob:
        return "scatter"
    elif rand_num < scatter_prob + fission_prob:
        return "fission"
    else:
        return "capture"


def sample_direction_cosine():
    """
    Function to sample direction cosine for the neutron in x-direction.

    Returns:
    - float: Sampled direction cosine (mu).
    """

    return random.uniform(-1, 1)  # Sample mu between -1 and 1


def sample_scattering_distance(total_xs):
    """
    Function to sample a distance for scattering.

    Parameters:
    - total_xs (float): Total macroscopic cross-section in cm^-1.

    Returns:
    - float: Sampled distance for scattering.
    """
    # Calculate the mean free path (inverse of total cross-section) adjusted by the
    # direction cosine
    mean_free_path = 1 / (total_xs)

    # Calculate the distance using the inverse transform sampling method
    return -mean_free_path * math.log(random.uniform(0, 1))


def sample_neutrons_emitted(nu):
    """
    Function to sample the number of neutrons emitted in a fission event.

    Parameters:
    - nu (float): Average number of neutrons emitted per fission.

    Returns:
    - int: Number of neutrons emitted in the fission event.
    """
    return np.random.poisson(nu)


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
    total_xs,
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

    # Sample a new position after scattering
    scatter_distance = sample_scattering_distance(total_xs)
    new_position = current_position + scatter_distance * mu

    # Handle if the neutron crosses the slab boundaries
    return handle_boundary_conditions(
        new_position, slab_thickness_cm, left_boundary_condition
    )


def simulate_single_history(initial_data, tallies, start_positions):
    """
    Function to simulate a single neutron history in a 1D slab.

    Parameters:
    - slab_thickness_cm (float): Thickness of the 1D slab in centimeters.
    - total_xs (float): Total macroscopic cross-section in cm^-1.
    - left_boundary_condition (str): Boundary condition for the left-hand side of the
                                     slab ('reflective' or 'transmissive').

    Returns:
    - float: Final position of the neutron or -1.0 if the neutron is absorbed.
    """

    (
        num_particles,
        slab_thickness_cm,
        total_xs,
        scatter_xs,
        fission_xs,
        left_boundary_condition,
    ) = initial_data.values()

    tallies["history"] += 1

    current_position = start_positions.pop()

    new_positions = []

    while True:
        # Free flight to next reaction/collision
        direction_cosine = sample_direction_cosine()
        current_position = update_neutron_position(
            current_position,
            slab_thickness_cm,
            direction_cosine,
            left_boundary_condition,
            total_xs,
        )

        # Leakage
        if current_position < 0:
            tallies["leakage"] += 1
            return tallies, new_positions

        # Collisions
        tallies["collision"] += 1

        interaction_type = sample_interaction_type(total_xs, scatter_xs, fission_xs)

        tallies[interaction_type] += 1

        # Capture
        if interaction_type == "capture":
            return tallies, new_positions

        # Fission
        if interaction_type == "fission":
            num_secondaries = sample_neutrons_emitted(3.24)
            tallies["secondary"] += num_secondaries
            for fission_neutron in range(num_secondaries):
                new_positions.append(current_position)
            return tallies, new_positions

        tallies["secondary"] += 1


def plot_starting_positions(starting_positions):
    """
    Function to create a histogram and plot starting positions.

    Parameters:
    - starting_positions (list): List of starting positions (x-values).
    """
    # Create a histogram
    # plt.hist(starting_positions, bins=30, edgecolor='black')

    # Calculate the histogram data
    hist, edges = np.histogram(starting_positions, bins=30)

    # Calculate the bin centers
    bin_centers = (edges[:-1] + edges[1:]) / 2

    # Normalise
    hist = hist / len(starting_positions)

    # Create a line plot for frequencies
    plt.plot(bin_centers, hist, color="blue", marker="o", linestyle="-")

    # Set plot labels and title
    plt.xlabel("Starting position (cm)")
    plt.ylabel("Frequency")
    plt.title("Histogram of Starting positions")


def main():
    initial_data = setup_simulation()

    num_generations = 10
    num_particles = initial_data["num_particles"]
    slab_thickness_cm = initial_data["slab_thickness_cm"]
    fission_xs = initial_data["fission_xs"]
    scatter_xs = initial_data["scatter_xs"]
    total_xs = initial_data["total_xs"]
    nu = 3.24

    num_particles_in_generation = num_particles

    # Get a uniformly distributed set of starting positions for the initial
    # generation of particles
    start_positions = [
        sample_position(slab_thickness_cm) for _ in range(num_particles_in_generation)
    ]

    for gen in range(num_generations):
        if gen >= 2:
            plot_starting_positions(start_positions)

        # Reset all the tallies to zero for this generation
        tallies = initialise_tallies()

        # Initialise a list for the start positions of the next generation,
        # arising from fission in this generation
        next_start_positions = []

        # Main loop over particles in this generation
        for _ in range(num_particles_in_generation):
            # Particle history
            tallies, new_start_positions = simulate_single_history(
                initial_data, tallies, start_positions
            )

            # Add the new start positions from this history to the global list
            # of start positions for the next generation
            next_start_positions += new_start_positions

        print(tallies)

        print(
            "Fission", tallies["fission"] / tallies["collision"], fission_xs / total_xs
        )
        print(
            "Scatter",
            tallies["scatter"] / tallies["collision"],
            scatter_xs / total_xs,
        )
        print(
            "Absorbs",
            tallies["capture"] / tallies["collision"],
            (total_xs - fission_xs - scatter_xs) / total_xs,
        )
        c = tallies["secondary"] / tallies["collision"]
        print("c", c)
        print(nu * fission_xs / (c * total_xs - scatter_xs))

        # Sanity checks
        assert tallies["history"] == num_particles_in_generation
        assert (
            tallies["capture"] + tallies["leakage"] + tallies["fission"]
            == num_particles_in_generation
        )
        assert (
            tallies["scatter"] + tallies["fission"] + tallies["capture"]
            == tallies["collision"]
        )

        # Estimate k_eff
        k = (
            nu
            * tallies["fission"]
            / (tallies["capture"] + tallies["leakage"] + tallies["fission"])
        )
        print(f"k = {k}")

        k = len(next_start_positions) / num_particles_in_generation
        # print(f"k = {k}")

        num_particles_in_generation = len(next_start_positions)
        start_positions = next_start_positions

    # plt.show()
    print("Done")
