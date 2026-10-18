# Import argparse for standalone plotting.
import argparse

# Import csv to read the training log.
import csv

# Import Path for input and output paths.
from pathlib import Path

# Import Matplotlib.
import matplotlib.pyplot as plt

# Import NumPy for moving averages.
import numpy as np


# Compute a simple moving average.
def moving_average(
    values,
    window=20,
):
    # Convert values into a float array.
    values = np.asarray(
        values,
        dtype=np.float32,
    )

    # Return unchanged values when the sequence is shorter than the window.
    if len(values) < window:
        # Return the original sequence.
        return values

    # Build a uniform averaging kernel.
    kernel = np.ones(
        window,
        dtype=np.float32,
    ) / float(window)

    # Compute the valid moving average.
    averaged = np.convolve(
        values,
        kernel,
        mode="valid",
    )

    # Pad the beginning so output length matches input length.
    prefix = np.full(
        window - 1,
        np.nan,
        dtype=np.float32,
    )

    # Return the padded moving average.
    return np.concatenate(
        [prefix, averaged]
    )


# Read and plot one training CSV.
def plot_training_log(
    log_path,
):
    # Convert input into a Path.
    log_path = Path(
        log_path
    )

    # Create empty episode storage.
    episodes = []

    # Create empty reward storage.
    rewards = []

    # Create empty success storage.
    successes = []

    # Open the training log.
    with log_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        # Create a dictionary CSV reader.
        reader = csv.DictReader(
            file
        )

        # Iterate through rows.
        for row in reader:
            # Store episode number.
            episodes.append(
                int(row["episode"])
            )

            # Store reward.
            rewards.append(
                float(row["reward"])
            )

            # Store success.
            successes.append(
                int(row["success"])
            )

    # Create a new reward figure.
    plt.figure(
        figsize=(8, 4.5)
    )

    # Plot raw episode reward.
    plt.plot(
        episodes,
        rewards,
        alpha=0.35,
        label="Episode reward",
    )

    # Plot the smoothed reward.
    plt.plot(
        episodes,
        moving_average(
            rewards,
            window=20,
        ),
        label="20-episode moving average",
    )

    # Label the horizontal axis.
    plt.xlabel(
        "Episode"
    )

    # Label the vertical axis.
    plt.ylabel(
        "Reward"
    )

    # Add the plot title.
    plt.title(
        "CNN + DQN Training Reward"
    )

    # Add a legend.
    plt.legend()

    # Use a compact layout.
    plt.tight_layout()

    # Save the reward curve.
    plt.savefig(
        "results/reward_curve.png",
        dpi=180,
    )

    # Close the reward figure.
    plt.close()

    # Create a separate success-rate figure.
    plt.figure(
        figsize=(8, 4.5)
    )

    # Plot the moving success rate.
    plt.plot(
        episodes,
        moving_average(
            successes,
            window=20,
        ),
    )

    # Label the horizontal axis.
    plt.xlabel(
        "Episode"
    )

    # Label the vertical axis.
    plt.ylabel(
        "Success rate"
    )

    # Limit the success axis to probabilities.
    plt.ylim(
        0.0,
        1.0,
    )

    # Add a title.
    plt.title(
        "20-Episode Moving Success Rate"
    )

    # Use a compact layout.
    plt.tight_layout()

    # Save the success plot.
    plt.savefig(
        "results/success_curve.png",
        dpi=180,
    )

    # Close the success figure.
    plt.close()


# Run as a standalone script when requested.
if __name__ == "__main__":
    # Create command-line options.
    parser = argparse.ArgumentParser()

    # Add the training-log path.
    parser.add_argument(
        "--log",
        default="results/training_log.csv",
    )

    # Parse arguments.
    args = parser.parse_args()

    # Plot the requested log.
    plot_training_log(
        args.log
    )
