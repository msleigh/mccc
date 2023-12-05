# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


def plot_starting_positions(starting_positions=None):
    """
    Function to create a histogram and plot starting positions.

    Parameters:
    - starting_positions (list): List of starting positions (x-values).
    """
    if starting_positions is None:
        plt.show()
        return

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
