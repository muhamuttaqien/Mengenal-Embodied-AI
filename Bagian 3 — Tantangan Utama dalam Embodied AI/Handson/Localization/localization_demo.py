# Import NumPy untuk operasi numerik.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import Path untuk mengatur path file.
from pathlib import Path


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent


# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"


# Membuat folder results jika belum ada.
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# Menentukan file hasil.
OUTPUT_PATH = (
    RESULTS_DIR
    / "localization_result.png"
)


# Pose robot: [x, y, yaw].
true_pose = np.array(
    [
        0.0,
        0.0,
        0.0,
    ]
)

estimated_pose = np.array(
    [
        0.0,
        0.0,
        0.0,
    ]
)


# Menyimpan trajectory awal.
true_trajectory = [
    true_pose.copy()
]

estimated_trajectory = [
    estimated_pose.copy()
]


# Menentukan parameter gerakan.
distance_per_step = 0.5

rotation_per_step = np.deg2rad(
    30
)


# Menentukan noise odometry.
position_noise_std = 0.03

rotation_noise_std = np.deg2rad(
    2
)


def move_forward(
    pose,
    distance,
):
    # Membaca pose robot.
    x, y, yaw = pose


    # Mengubah posisi robot.
    x += (
        distance
        * np.cos(yaw)
    )

    y += (
        distance
        * np.sin(yaw)
    )


    # Mengembalikan pose baru.
    return np.array(
        [
            x,
            y,
            yaw,
        ]
    )


def rotate(
    pose,
    angle,
):
    # Membaca pose robot.
    x, y, yaw = pose


    # Mengubah orientasi robot.
    yaw += angle


    # Mengembalikan pose baru.
    return np.array(
        [
            x,
            y,
            yaw,
        ]
    )


# Menentukan urutan aksi robot.
actions = [
    "forward",
    "forward",
    "rotate_left",
    "forward",
    "forward",
    "rotate_left",
    "forward",
    "forward",
    "rotate_right",
    "forward",
]


# Menjalankan simulasi.
for action in actions:

    # Menjalankan gerakan maju.
    if action == "forward":

        # Mengubah ground truth.
        true_pose = move_forward(
            true_pose,
            distance_per_step,
        )


        # Menambahkan noise pada odometry.
        noisy_distance = (
            distance_per_step
            + np.random.normal(
                0,
                position_noise_std,
            )
        )


        # Mengubah estimated pose.
        estimated_pose = move_forward(
            estimated_pose,
            noisy_distance,
        )


    # Menjalankan rotasi ke kiri.
    elif action == "rotate_left":

        # Mengubah ground truth.
        true_pose = rotate(
            true_pose,
            rotation_per_step,
        )


        # Menambahkan noise pada rotasi.
        noisy_rotation = (
            rotation_per_step
            + np.random.normal(
                0,
                rotation_noise_std,
            )
        )


        # Mengubah estimated pose.
        estimated_pose = rotate(
            estimated_pose,
            noisy_rotation,
        )


    # Menjalankan rotasi ke kanan.
    elif action == "rotate_right":

        # Mengubah ground truth.
        true_pose = rotate(
            true_pose,
            -rotation_per_step,
        )


        # Menambahkan noise pada rotasi.
        noisy_rotation = (
            -rotation_per_step
            + np.random.normal(
                0,
                rotation_noise_std,
            )
        )


        # Mengubah estimated pose.
        estimated_pose = rotate(
            estimated_pose,
            noisy_rotation,
        )


    # Menyimpan trajectory.
    true_trajectory.append(
        true_pose.copy()
    )

    estimated_trajectory.append(
        estimated_pose.copy()
    )


# Mengubah trajectory menjadi NumPy array.
true_trajectory = np.array(
    true_trajectory
)

estimated_trajectory = np.array(
    estimated_trajectory
)


# Menampilkan ground truth pose.
print(
    "Ground Truth Pose"
)

print(
    f"x   : {true_pose[0]:.2f} m\n"
    f"y   : {true_pose[1]:.2f} m\n"
    f"yaw : "
    f"{np.rad2deg(true_pose[2]):.2f} degree"
)


print()


# Menampilkan estimated pose.
print(
    "Estimated Pose"
)

print(
    f"x   : {estimated_pose[0]:.2f} m\n"
    f"y   : {estimated_pose[1]:.2f} m\n"
    f"yaw : "
    f"{np.rad2deg(estimated_pose[2]):.2f} degree"
)


# Membuat visualisasi.
plt.figure(
    figsize=(
        8,
        6,
    )
)


# Menampilkan ground truth trajectory.
plt.plot(
    true_trajectory[:, 0],
    true_trajectory[:, 1],
    "o-",
    label="Ground Truth",
)


# Menampilkan estimated trajectory.
plt.plot(
    estimated_trajectory[:, 0],
    estimated_trajectory[:, 1],
    "x--",
    label="Estimated Position",
)


# Menentukan panjang panah orientasi.
arrow_length = 0.3


# Menampilkan orientasi ground truth.
plt.arrow(
    true_pose[0],
    true_pose[1],
    arrow_length
    * np.cos(
        true_pose[2]
    ),
    arrow_length
    * np.sin(
        true_pose[2]
    ),
    head_width=0.08,
)


# Menampilkan orientasi estimated pose.
plt.arrow(
    estimated_pose[0],
    estimated_pose[1],
    arrow_length
    * np.cos(
        estimated_pose[2]
    ),
    arrow_length
    * np.sin(
        estimated_pose[2]
    ),
    head_width=0.08,
)


# Mengatur plot.
plt.xlabel(
    "X Position (m)"
)

plt.ylabel(
    "Y Position (m)"
)

plt.title(
    "Robot Localization"
)

plt.axis(
    "equal"
)

plt.grid()

plt.legend()

plt.tight_layout()


# Menyimpan hasil.
plt.savefig(
    OUTPUT_PATH,
    dpi=200,
)


print(
    "\nHasil visualisasi disimpan ke:",
    OUTPUT_PATH,
)


# Menampilkan hasil.
plt.show()
