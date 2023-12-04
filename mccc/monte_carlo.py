# -*- coding: utf-8 -*-
from mccc.geometry import update_neutron_position
from mccc.plotting import plot_starting_positions
from mccc.sampling import sample_direction_cosine
from mccc.sampling import sample_interaction_type
from mccc.sampling import sample_neutrons_emitted
from mccc.sampling import sample_position
from mccc.sampling import sample_scattering_distance
from mccc.setup import initialise_tallies
from mccc.setup import setup_simulation


def simulate_single_history(initial_data, tallies, start_positions):
    """
    Function to simulate a single neutron history in a 1D slab.

    Parameters:

    Returns:
    """

    (
        num_generations,
        num_particles,
        slab_thickness_cm,
        mean_free_path,
        scatter_prob,
        fission_prob,
        nu,
        left_boundary_condition,
    ) = initial_data.values()

    tallies["history"] += 1

    current_position = start_positions.pop()

    new_positions = []

    while True:
        # Free flight to next reaction/collision
        direction_cosine = sample_direction_cosine()
        scatter_distance = sample_scattering_distance(mean_free_path)
        current_position = update_neutron_position(
            current_position,
            slab_thickness_cm,
            direction_cosine,
            left_boundary_condition,
            scatter_distance,
        )

        # Leakage
        if current_position < 0:
            tallies["leakage"] += 1
            return tallies, new_positions

        # Collisions
        tallies["collision"] += 1

        interaction_type = sample_interaction_type(scatter_prob, fission_prob)

        tallies[interaction_type] += 1

        # Capture
        if interaction_type == "capture":
            return tallies, new_positions

        # Fission
        if interaction_type == "fission":
            num_secondaries = sample_neutrons_emitted(nu)
            tallies["secondary"] += num_secondaries
            for fission_neutron in range(num_secondaries):
                new_positions.append(current_position)
            return tallies, new_positions

        tallies["secondary"] += 1


def trial(plot=True):
    """
    A single independent run with a fixed number of generations and particles.
    """
    initial_data = setup_simulation()

    num_generations = initial_data["num_generations"]
    num_particles = initial_data["num_particles"]
    slab_thickness_cm = initial_data["slab_thickness_cm"]
    fission_prob = initial_data["fission_prob"]
    scatter_prob = initial_data["scatter_prob"]
    nu = initial_data["nu"]

    num_particles_in_generation = num_particles

    # Get a uniformly distributed set of starting positions for the initial
    # generation of particles
    start_positions = [
        sample_position(slab_thickness_cm) for _ in range(num_particles_in_generation)
    ]

    for gen in range(num_generations):
        if gen >= 2 and plot:
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

        print("Fission", tallies["fission"] / tallies["collision"], fission_prob)
        print(
            "Scatter",
            tallies["scatter"] / tallies["collision"],
            scatter_prob,
        )
        print(
            "Absorbs",
            tallies["capture"] / tallies["collision"],
            1 - fission_prob - scatter_prob,
        )
        c = tallies["secondary"] / tallies["collision"]
        print("c", c)
        print(nu * fission_prob / (c - scatter_prob))

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
        k1 = (
            nu
            * tallies["fission"]
            / (tallies["capture"] + tallies["leakage"] + tallies["fission"])
        )
        print(f"k1 = {k1}")

        k2 = len(next_start_positions) / num_particles_in_generation
        print(f"k2 = {k2}")

        num_particles_in_generation = len(next_start_positions)
        start_positions = next_start_positions

    if plot:
        plot_starting_positions()

    return k1, k2


def main():
    print("k =", trial(plot=False))
