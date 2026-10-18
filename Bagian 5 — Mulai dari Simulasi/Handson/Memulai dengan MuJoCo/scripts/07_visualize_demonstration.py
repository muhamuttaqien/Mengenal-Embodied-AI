# Import argparse untuk menerima path file demonstration.
import argparse

# Import Path untuk mengatur output file.
from pathlib import Path

# Import NumPy untuk membaca dataset.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt


# Menentukan dimensi setiap observation.
OBSERVATION_DIMS = {
    "robot0_joint_pos": 7,
    "robot0_joint_vel": 7,
    "robot0_eef_pos": 3,
    "robot0_eef_quat": 4,
    "robot0_gripper_qpos": 2,
    "Can_pos": 3,
    "Can_quat": 4,
}


# Membuat command-line parser.
parser = argparse.ArgumentParser(
    description="Visualize one saved demonstration."
)


# Menambahkan argument file demonstration.
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
observations = data[
    "observations"
]


# Membaca reward.
rewards = data[
    "rewards"
]


# Membaca observation key.
observation_keys = data[
    "observation_keys"
].tolist()


# Membuat mapping posisi setiap observation
# di dalam flattened observation vector.
observation_slices = {}


# Posisi awal pada vector.
start = 0


# Membaca setiap observation key.
for key in observation_keys:

    # Membaca jumlah dimensinya.
    dimension = OBSERVATION_DIMS.get(
        key
    )


    # Lewati key yang tidak dikenal.
    if dimension is None:

        print(
            f"Unknown observation key: {key}"
        )

        continue


    # Menentukan bagian vector untuk key ini.
    observation_slices[key] = slice(
        start,
        start + dimension
    )


    # Memperbarui posisi berikutnya.
    start += dimension


# Memastikan posisi end-effector tersedia.
if "robot0_eef_pos" not in observation_slices:

    raise RuntimeError(
        "robot0_eef_pos was not found "
        "in the demonstration."
    )


# Memastikan posisi Can tersedia.
if "Can_pos" not in observation_slices:

    raise RuntimeError(
        "Can_pos was not found "
        "in the demonstration."
    )


# Mengambil trajectory end-effector.
eef_positions = observations[
    :,
    observation_slices[
        "robot0_eef_pos"
    ]
]


# Mengambil trajectory Can.
can_positions = observations[
    :,
    observation_slices[
        "Can_pos"
    ]
]


# Membuat array timestep.
timesteps = np.arange(
    len(observations)
)


# Membuat figure.
fig = plt.figure(
    figsize=(10, 8)
)


# Membuat plot trajectory dari atas.
ax1 = fig.add_subplot(
    2,
    2,
    1
)


# Menampilkan trajectory end-effector.
ax1.plot(
    eef_positions[:, 0],
    eef_positions[:, 1],
    label="End-Effector"
)


# Menampilkan trajectory Can.
ax1.plot(
    can_positions[:, 0],
    can_positions[:, 1],
    label="Can"
)


# Menandai posisi awal end-effector.
ax1.scatter(
    eef_positions[0, 0],
    eef_positions[0, 1],
    marker="o"
)


# Menandai posisi akhir end-effector.
ax1.scatter(
    eef_positions[-1, 0],
    eef_positions[-1, 1],
    marker="x"
)


# Memberikan label axis.
ax1.set_xlabel(
    "X Position"
)

ax1.set_ylabel(
    "Y Position"
)


# Memberikan judul.
ax1.set_title(
    "Top-Down Trajectory"
)


# Menampilkan legend.
ax1.legend()


# Membuat plot ketinggian end-effector.
ax2 = fig.add_subplot(
    2,
    2,
    2
)


# Menampilkan posisi Z end-effector.
ax2.plot(
    timesteps,
    eef_positions[:, 2],
    label="End-Effector"
)


# Menampilkan posisi Z Can.
ax2.plot(
    timesteps,
    can_positions[:, 2],
    label="Can"
)


# Memberikan label.
ax2.set_xlabel(
    "Timestep"
)

ax2.set_ylabel(
    "Z Position"
)


# Memberikan judul.
ax2.set_title(
    "Object Height"
)


# Menampilkan legend.
ax2.legend()


# Membuat plot reward.
ax3 = fig.add_subplot(
    2,
    1,
    2
)


# Menampilkan reward sepanjang episode.
ax3.plot(
    timesteps,
    rewards
)


# Memberikan label.
ax3.set_xlabel(
    "Timestep"
)

ax3.set_ylabel(
    "Reward"
)


# Memberikan judul.
ax3.set_title(
    "Reward During Demonstration"
)


# Merapikan layout.
plt.tight_layout()


# Membuat folder results jika belum tersedia.
RESULT_DIR = Path(
    "results"
)

RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Membuat nama file output.
demo_name = Path(
    args.demo_file
).stem


output_path = (
    RESULT_DIR
    / f"{demo_name}_visualization.png"
)


# Menyimpan visualisasi.
plt.savefig(
    output_path,
    dpi=180
)


# Menampilkan figure.
plt.show()


# Menampilkan lokasi hasil.
print(
    "Saved:",
    output_path
)
