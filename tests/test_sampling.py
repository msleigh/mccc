# -*- coding: utf-8 -*-
from mccc.sampling import sample_direction_cosine
from mccc.sampling import sample_interaction_type
from mccc.sampling import sample_neutrons_emitted
from mccc.sampling import sample_position
from mccc.sampling import sample_scattering_distance


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


def test_sample_interaction_type():
    """
    Test the sample_interaction_type function.
    """
    scatter_prob = 0.5
    fission_prob = 0.2

    # Ensure the function returns a valid interaction type
    interaction_type = sample_interaction_type(scatter_prob, fission_prob)
    assert interaction_type in {"scatter", "fission", "capture"}

    # Ensure the function returns 'scattering' within the scattering probability
    interaction_type = sample_interaction_type(
        scatter_prob, fission_prob, rand_num=scatter_prob - 1e-10
    )
    assert interaction_type == "scatter"

    # Ensure the function returns 'fission' within the fission probability
    interaction_type = sample_interaction_type(
        scatter_prob,
        fission_prob,
        rand_num=scatter_prob + fission_prob - 1e-10,
    )
    assert interaction_type == "fission"

    # Ensure the function returns 'absorption' for values close to or beyond 1.0
    interaction_type = sample_interaction_type(
        scatter_prob, fission_prob, rand_num=1.0 - 1e-10
    )
    assert interaction_type == "capture"

    # Ensure the function returns values within the specified range
    num_samples = 1000
    values = [
        sample_interaction_type(scatter_prob, fission_prob) for _ in range(num_samples)
    ]
    assert all(
        interaction_type in {"scatter", "fission", "capture"}
        for interaction_type in values
    )


def test_sample_neutrons_emitted():
    """
    Test the sample_neutrons_emitted function.
    """
    nu = 0
    neutrons_emitted = sample_neutrons_emitted(nu)
    assert neutrons_emitted == 0

    num_samples = 1000
    values = [sample_neutrons_emitted(nu) for _ in range(num_samples)]
    assert all(neutrons_emitted >= 0 for neutrons_emitted in values)


def test_sample_position():
    """
    Test the sample_position function.
    """
    slab_thickness_cm = 0
    start_position = sample_position(slab_thickness_cm)
    assert start_position == 0

    slab_thickness_cm = 10.0
    num_samples = 1000
    values = [sample_position(slab_thickness_cm) for _ in range(num_samples)]
    assert all(0 <= start_position <= slab_thickness_cm for start_position in values)


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
