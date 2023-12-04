# -*- coding: utf-8 -*-
import math
import random

import numpy as np


def sample_direction_cosine():
    """
    Function to sample direction cosine for the neutron in x-direction.

    Returns:
    - float: Sampled direction cosine (mu).
    """

    return random.uniform(-1, 1)  # Sample mu between -1 and 1


def sample_interaction_type(scatter_prob, fission_prob, rand_num=None):
    """
    Function to sample an interaction type based on cross-sections.

    Parameters:
    - scatter_prob (float): Scattering probability
    - fission_prob (float): Fission probability

    Returns:
    - str: Interaction type ('scatter', 'fission', 'capture').
    """

    # Sample a random number between 0 and 1
    if rand_num is None:
        rand_num = random.uniform(0, 1)

    if rand_num < scatter_prob:
        return "scatter"
    elif rand_num < scatter_prob + fission_prob:
        return "fission"
    else:
        return "capture"


def sample_neutrons_emitted(nu):
    """
    Function to sample the number of neutrons emitted in a fission event.

    Parameters:
    - nu (float): Average number of neutrons emitted per fission.

    Returns:
    - int: Number of neutrons emitted in the fission event.
    """
    return np.random.poisson(nu)


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


def sample_scattering_distance(mean_free_path):
    """
    Function to sample a distance for scattering.

    Parameters:
    - mean_free_path (float): inverse of total macroscopic cross-section, in cm.

    Returns:
    - float: Sampled distance for scattering.
    """

    # Calculate the distance using the inverse transform sampling method
    return -mean_free_path * math.log(random.uniform(0, 1))
