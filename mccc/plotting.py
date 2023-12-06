# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


def plot_starting_positions(num_generations, gen, starting_positions=None):
    """
    Function to create a histogram and plot starting positions.

    Parameters:
    - starting_positions (list): List of starting positions (x-values).
    """
    if starting_positions is None:
        plt.savefig("fission_rate.png")
        return

    # Calculate the histogram data
    hist, edges = np.histogram(starting_positions, bins=30)

    # Calculate the bin centers
    bin_centers = (edges[:-1] + edges[1:]) / 2

    # Normalise
    hist = hist / len(starting_positions)

    colors = plt.cm.jet(np.linspace(0, 1, num_generations))

    # Create a line plot for frequencies
    plt.plot(bin_centers, hist, color=colors[gen], linestyle="-")

    # Set plot labels and title
    plt.xlabel("Starting position (cm)")
    plt.ylabel("Frequency")
    plt.title("Histogram of starting positions by generation")
    return


def plot_particle_convergence(df):
    """
    Function to plot k1 and k2 as a function of particle number.
    """
    df.plot(
        y=["k1", "k2"],
        logx=True,
        grid=True,
        yerr=[df["k1_std"], df["k2_std"]],
        xlim=(500, 2000000),
        ylim=(0.9, 1.1),
        xlabel="No. of particles",
        ylabel="$k_{\mathrm{eff}}$",
        title="Convergence of $k_{\mathrm{eff}}$ with no. of particles.",
    )
    plt.savefig("particle_convergence.png")
    return


def plot_generations(df):
    """
    Function to plot k1 and k2 as a function of generation number.
    """
    df.plot(
        y=["k1", "k2"],
        grid=True,
        yerr=[df["k1_std"], df["k2_std"]],
        xticks=df.index,
        ylim=(0.97, 1.03),
        xlabel="Generation number",
        ylabel="$k_{\mathrm{eff}}$",
        title="Convergence of $k_{\mathrm{eff}}$ with generation",
    )
    plt.savefig("generations.png")
    return
