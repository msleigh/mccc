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
from mccc.setup import update_user_input


def simulate_single_history(
    cfg,
    tallies,
    start_positions,
):
    """
    Function to simulate a single neutron history in a 1D slab.

    Parameters:

    Returns:
    """

    tallies["history"] += 1

    current_position = start_positions.pop()

    new_positions = []

    while True:
        # Free flight to next reaction/collision
        direction_cosine = sample_direction_cosine()
        scatter_distance = sample_scattering_distance(cfg.mean_free_path)
        current_position = update_neutron_position(
            current_position,
            cfg.slab_thickness_cm,
            direction_cosine,
            cfg.left_boundary_condition,
            scatter_distance,
        )

        # Leakage
        if current_position < 0:
            tallies["leakage"] += 1
            return tallies, new_positions

        # Collisions
        tallies["collision"] += 1

        interaction_type = sample_interaction_type(cfg.scatter_prob, cfg.fission_prob)

        tallies[interaction_type] += 1

        # Capture
        if interaction_type == "capture":
            return tallies, new_positions

        # Fission
        if interaction_type == "fission":
            num_secondaries = sample_neutrons_emitted(cfg.nu)
            tallies["secondary"] += num_secondaries
            for fission_neutron in range(num_secondaries):
                new_positions.append(current_position)
            return tallies, new_positions

        # Scattering
        tallies["secondary"] += 1


def run(num_generations, num_particles, plot=True):
    """
    A single independent run with a fixed number of generations and particles.
    """

    # Sensible defaults
    defaults = setup_simulation()

    # Over-ride with any user input
    # Create a dictionary from provided arguments that correspond to fields in
    # the `defaults` object
    user_input = {
        k: v
        for k, v in locals().items()
        if k in defaults.__annotations__ and v is not None
    }

    # Replace defaults with user input
    cfg = update_user_input(defaults, user_input)

    # Initialise the per-generation number of particles
    num_particles_in_generation = cfg.num_particles

    # Get a uniformly distributed set of starting positions for the initial
    # generation of particles
    start_positions = [
        sample_position(cfg.slab_thickness_cm)
        for _ in range(num_particles_in_generation)
    ]

    # Lists for storing the estimates of k_effective across generations
    # k1 and k2 are two different estimators for k_effective
    k1 = []
    k2 = []

    for gen in range(cfg.num_generations):
        if plot:
            plot_starting_positions(cfg.num_generations, gen, start_positions)

        # Reset all the tallies to zero for this generation
        tallies = initialise_tallies()

        # Initialise a list for the start positions of the next generation,
        # arising from fission in this generation
        next_start_positions = []

        # Main loop over particles in this generation
        for _ in range(num_particles_in_generation):
            # Particle history
            tallies, new_start_positions = simulate_single_history(
                cfg,
                tallies,
                start_positions,
            )

            # Add the new start positions from this history to the global list
            # of start positions for the next generation
            next_start_positions += new_start_positions

        if tallies["collision"] == 0:
            sys.exit("Zero collisions")

        # Estimate k_eff
        k1.append(
            cfg.nu
            * tallies["fission"]
            / (tallies["capture"] + tallies["leakage"] + tallies["fission"])
        )
        k2.append(len(next_start_positions) / num_particles_in_generation)
        c = tallies["secondary"] / tallies["collision"]

        verbose = False
        if verbose:
            print(tallies)
            print(
                "Fission", tallies["fission"] / tallies["collision"], cfg.fission_prob
            )
            print(
                "Scatter",
                tallies["scatter"] / tallies["collision"],
                cfg.scatter_prob,
            )
            print(
                "Absorbs",
                tallies["capture"] / tallies["collision"],
                1 - cfg.fission_prob - cfg.scatter_prob,
            )
            print("c", c)
            print(cfg.nu * cfg.fission_prob / (c - cfg.scatter_prob))
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
        plot_starting_positions(cfg.num_generations, gen)

    return k1, k2


def trial(num_generations, num_particles):
    """
    Run a trial; a set of n independent but identical runs, averaged over.
    """
    n = 10
    k1, k2 = zip(*[run(num_generations, num_particles) for _ in range(n)])
    k1m = np.mean(np.array(k1), axis=0)
    k1s = np.std(np.array(k1), axis=0)
    k2m = np.mean(np.array(k2), axis=0)
    k2s = np.std(np.array(k2), axis=0)
    return (k1m, k1s, k2m, k2s)


def study_convergence(num_generations, particles_list):
    data = []
    for num_particles in particles_list:
        data.append([series[-1] for series in trial(num_generations, num_particles)])
    df = pd.DataFrame(
        data, index=particles_list, columns=["k1", "k1_std", "k2", "k2_std"]
    )
    plot_particle_convergence(df)


def study_generations(num_generations, num_particles):
    data = trial(num_generations, num_particles)
    df = pd.DataFrame(
        np.transpose(data),
        index=range(num_generations),
        columns=["k1", "k1_std", "k2", "k2_std"],
    )
    plot_generations(df)


def study_fission_rate(num_generations, num_particles):
    run(num_generations, num_particles, plot=True)


@click.command()
@click.option(
    "num_generations", "-g", "--generations", type=int, help="Number of generations."
)
@click.option(
    "particles_list",
    "-p",
    "--particles",
    default=[None],
    type=int,
    multiple=True,
    help="Number of particles.",
)
@click.option("plot_type", "-t", "--type", help="Type of plot to create.")
def main(num_generations, particles_list, plot_type):
    if plot_type == "convergence":
        if len(particles_list) < 2:
            sys.exit("Not enough -p values")
        study_convergence(num_generations, particles_list)
    elif plot_type == "generations":
        if len(particles_list) > 1:
            sys.exit("Too many -p values")
        study_generations(num_generations, particles_list[0])
    elif plot_type == "fission_rate":
        if len(particles_list) > 1:
            sys.exit("Too many -p values")
        study_fission_rate(num_generations, particles_list[0])
    else:
        if len(particles_list) > 1:
            sys.exit("Too many -p values")
        run(num_generations, particles_list[0], plot=False)
