# -*- coding: utf-8 -*-
from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace


@dataclass
class Config:
    """
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
    - random_seed (int | None): Optional RNG seed for reproducible runs.
    """

    # Independent parameters
    num_generations: int = 4
    num_particles: int = 128000
    slab_thickness_cm: float = 1.853722
    total_xs: float = 0.326400
    scatter_xs: float = 0.225216
    fission_xs: float = 0.081600
    nu: float = 3.24
    left_boundary_condition: str = "reflective"
    random_seed: int | None = None

    # Derived parameters
    mean_free_path: float = field(init=False)
    scatter_prob: float = field(init=False)
    fission_prob: float = field(init=False)

    # Calculate derived parameters so they're updated automatically if the
    # independent paramer(s) they depend on are changed
    def __post_init__(self):
        self.mean_free_path = 1 / self.total_xs
        self.scatter_prob = self.scatter_xs / self.total_xs
        self.fission_prob = self.fission_xs / self.total_xs


def setup_simulation():
    """
    Function to perform the initial setup for the Monte Carlo simulation.

    Returns:
    - dict: A dictionary containing initial data and parameters.
    """

    return Config()


def update_user_input(initial_data, user_input):
    """
    Function to perform the initial setup for the Monte Carlo simulation.

    Returns:
    - dict: A dictionary containing initial data and parameters.
    """

    return replace(initial_data, **user_input)


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
