# -*- coding: utf-8 -*-
import sys

import click
import numpy as np
import pandas as pd

from mccc.geometry import update_neutron_position
from mccc.plotting import plot_generations
from mccc.plotting import plot_particle_convergence
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


def run(generations, particles, plot=True):
    """
    A single independent run with a fixed number of generations and particles.
    """
    initial_data = setup_simulation(
        num_particles=particles, num_generations=generations
    )

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

    k1 = []
    k2 = []

    for gen in range(num_generations):
        if gen >= 0 and plot:
            plot_starting_positions(num_generations, gen, start_positions)

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

        if tallies["collision"] == 0:
            sys.exit("Zero collisions")

        # Estimate k_eff
        k1.append(
            nu
            * tallies["fission"]
            / (tallies["capture"] + tallies["leakage"] + tallies["fission"])
        )
        k2.append(len(next_start_positions) / num_particles_in_generation)
        c = tallies["secondary"] / tallies["collision"]

        verbose = False
        if verbose:
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
            print("c", c)
            print(nu * fission_prob / (c - scatter_prob))
            print(f"k1 = {k1}")
            print(f"k2 = {k2}")

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

        num_particles_in_generation = len(next_start_positions)
        if num_particles_in_generation == 0:
            sys.exit("Zero particles")
        start_positions = next_start_positions

    if plot:
        plot_starting_positions(num_generations, gen)

    return k1, k2


def trial(generations, particles):
    """
    Run a trial; a set of n independent but identical runs, averaged over.
    """
    n = 10
    k1, k2 = zip(*[run(generations, particles) for _ in range(n)])
    k1m = np.mean(np.array(k1), axis=0)
    k1s = np.std(np.array(k1), axis=0)
    k2m = np.mean(np.array(k2), axis=0)
    k2s = np.std(np.array(k2), axis=0)
    return (k1m, k1s, k2m, k2s)


def study_convergence(generations, particles_list):
    data = []
    for particles in particles_list:
        data.append([series[-1] for series in trial(generations, particles)])
    df = pd.DataFrame(
        data, index=particles_list, columns=["k1", "k1_std", "k2", "k2_std"]
    )
    plot_particle_convergence(df)


def study_generations(generations, particles):
    data = trial(generations, particles)
    print(data)
    df = pd.DataFrame(
        np.transpose(data),
        index=range(generations),
        columns=["k1", "k1_std", "k2", "k2_std"],
    )
    print(df)
    plot_generations(df)


def study_fission_rate(generations, particles):
    run(generations, particles, plot=True)


@click.command()
@click.option("-g", "--generations", default=1, help="Number of generations.")
@click.option(
    "particles_list",
    "-p",
    "--particles",
    default=[200000],
    multiple=True,
    help="Number of particles.",
)
@click.option(
    "plot_type", "-t", "--type", default="convergence", help="Type of plot to create."
)
def main(generations, particles_list, plot_type):
    if plot_type == "convergence":
        if len(particles_list) < 2:
            sys.exit("Not enough -p values")
        study_convergence(generations, particles_list)
    elif plot_type == "generations":
        if len(particles_list) != 1:
            sys.exit("Too many -p values")
        study_generations(generations, particles_list[0])
    elif plot_type == "fission_rate":
        if len(particles_list) != 1:
            sys.exit("Too many -p values")
        study_fission_rate(generations, particles_list[0])
