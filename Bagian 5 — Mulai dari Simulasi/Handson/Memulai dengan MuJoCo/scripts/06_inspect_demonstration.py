# Import argparse untuk menerima path file demonstration.
import argparse

# Import NumPy untuk membaca dataset NPZ.
import numpy as np


# Membuat command-line parser.
parser = argparse.ArgumentParser(
    description="Inspect one saved demonstration."
)


# Menambahkan argument untuk file demonstration.
parser.add_argument(
    "demo_file",
    help="Path to a demonstration .npz file.",
)


# Membaca argument dari terminal.
args = parser.parse_args()


# Membuka file demonstration.
data = np.load(
    args.demo_file,
    allow_pickle=False,
)


# Membaca observation.
observations = data["observations"]


# Membaca action.
actions = data["actions"]


# Membaca reward.
rewards = data["rewards"]


# Membaca status keberhasilan.
success = bool(
    data["success"][0]
)


# Membaca nama observation key.
observation_keys = data[
    "observation_keys"
].tolist()


# Menampilkan nama file.
print(
    "File               :",
    args.demo_file
)


# Menampilkan jumlah timestep.
print(
    "Timesteps          :",
    observations.shape[0]
)


# Menampilkan shape observation.
print(
    "Observation shape  :",
    observations.shape
)


# Menampilkan shape action.
print(
    "Action shape       :",
    actions.shape
)


# Menampilkan shape reward.
print(
    "Reward shape       :",
    rewards.shape
)


# Menampilkan status keberhasilan.
print(
    "Success            :",
    success
)


# Menampilkan total reward.
print(
    "Total reward       :",
    float(
        rewards.sum()
    )
)


# Menampilkan observation key.
print(
    "Observation keys   :"
)


# Membaca setiap observation key.
for key in observation_keys:

    print(
        "-",
        key
    )


# Menampilkan observation pertama.
print(
    "\nFirst observation:"
)


print(
    observations[0]
)


# Menampilkan action pertama.
print(
    "\nFirst action:"
)


print(
    actions[0]
)
