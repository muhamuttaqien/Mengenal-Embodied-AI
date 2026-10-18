# Import NumPy untuk operasi numerik.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import animation untuk membuat GIF.
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

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

# Menentukan file hasil grafik.
IMAGE_OUTPUT_PATH = (
    RESULTS_DIR
    / "locomotion_result.png"
)

# Menentukan file hasil animasi.
GIF_OUTPUT_PATH = (
    RESULTS_DIR
    / "locomotion_animation.gif"
)


# Menentukan parameter simulasi.
DT = 0.05
DURATION = 8.0

# Membuat time steps.
time = np.arange(
    0,
    DURATION,
    DT,
)

# Menentukan kecepatan berjalan.
WALKING_SPEED = 0.35


# Menentukan panjang bagian kaki.
THIGH_LENGTH = 0.45
SHANK_LENGTH = 0.45

# Menentukan ukuran body.
BODY_HEIGHT = 0.55
HEAD_RADIUS = 0.10

# Menentukan tinggi pelvis.
PELVIS_HEIGHT = 1.0


# Menentukan parameter gait.
STEP_FREQUENCY = 0.8

HIP_AMPLITUDE = np.deg2rad(
    25
)

KNEE_BASE = np.deg2rad(
    10
)

KNEE_AMPLITUDE = np.deg2rad(
    40
)


# Membuat phase gait.
phase = (
    2
    * np.pi
    * STEP_FREQUENCY
    * time
)


# Membuat gerakan hip kiri.
left_hip = (
    HIP_AMPLITUDE
    * np.sin(
        phase
    )
)


# Membuat gerakan hip kanan.
right_hip = (
    HIP_AMPLITUDE
    * np.sin(
        phase
        + np.pi
    )
)


# Membuat gerakan knee kiri.
left_knee = (
    KNEE_BASE
    + KNEE_AMPLITUDE
    * (
        0.5
        * (
            1
            - np.cos(
                phase
            )
        )
    )
)


# Membuat gerakan knee kanan.
right_knee = (
    KNEE_BASE
    + KNEE_AMPLITUDE
    * (
        0.5
        * (
            1
            - np.cos(
                phase
                + np.pi
            )
        )
    )
)


# Membuat gerakan pelvis ke depan.
pelvis_x = (
    WALKING_SPEED
    * time
)


# Membuat gerakan pelvis naik dan turun.
pelvis_y = (
    PELVIS_HEIGHT
    + 0.03
    * np.sin(
        2
        * phase
    )
)


def leg_forward_kinematics(
    hip_position,
    hip_angle,
    knee_angle,
):
    # Membaca posisi hip.
    hip_x, hip_y = (
        hip_position
    )


    # Menghitung posisi knee.
    knee_x = (
        hip_x
        + THIGH_LENGTH
        * np.sin(
            hip_angle
        )
    )

    knee_y = (
        hip_y
        - THIGH_LENGTH
        * np.cos(
            hip_angle
        )
    )


    # Menghitung sudut lower leg.
    lower_leg_angle = (
        hip_angle
        - knee_angle
    )


    # Menghitung posisi foot.
    foot_x = (
        knee_x
        + SHANK_LENGTH
        * np.sin(
            lower_leg_angle
        )
    )

    foot_y = (
        knee_y
        - SHANK_LENGTH
        * np.cos(
            lower_leg_angle
        )
    )


    # Mengembalikan posisi knee dan foot.
    return (
        np.array(
            [
                knee_x,
                knee_y,
            ]
        ),
        np.array(
            [
                foot_x,
                foot_y,
            ]
        ),
    )


# Menyimpan posisi knee dan foot kiri.
left_knee_position = []
left_foot_position = []

# Menyimpan posisi knee dan foot kanan.
right_knee_position = []
right_foot_position = []


# Menghitung trajectory kedua kaki.
for i in range(
    len(time)
):
    # Menentukan posisi hip.
    hip_position = np.array(
        [
            pelvis_x[i],
            pelvis_y[i],
        ]
    )


    # Menghitung kaki kiri.
    knee, foot = (
        leg_forward_kinematics(
            hip_position,
            left_hip[i],
            left_knee[i],
        )
    )

    left_knee_position.append(
        knee
    )

    left_foot_position.append(
        foot
    )


    # Menghitung kaki kanan.
    knee, foot = (
        leg_forward_kinematics(
            hip_position,
            right_hip[i],
            right_knee[i],
        )
    )

    right_knee_position.append(
        knee
    )

    right_foot_position.append(
        foot
    )


# Mengubah trajectory menjadi NumPy array.
left_knee_position = np.array(
    left_knee_position
)

left_foot_position = np.array(
    left_foot_position
)

right_knee_position = np.array(
    right_knee_position
)

right_foot_position = np.array(
    right_foot_position
)


# Menghitung jarak yang ditempuh.
distance_travelled = (
    pelvis_x[-1]
    - pelvis_x[0]
)


# Menampilkan informasi simulasi.
print(
    "Walking simulation completed."
)

print(
    f"Duration: "
    f"{DURATION:.1f} seconds"
)

print(
    f"Walking speed: "
    f"{WALKING_SPEED:.2f} m/s"
)

print(
    f"Distance travelled: "
    f"{distance_travelled:.2f} m"
)


# Membuat visualisasi joint trajectory.
plt.figure(
    figsize=(
        9,
        6,
    )
)


# Menampilkan hip kiri.
plt.plot(
    time,
    np.rad2deg(
        left_hip
    ),
    label="Left Hip",
)


# Menampilkan hip kanan.
plt.plot(
    time,
    np.rad2deg(
        right_hip
    ),
    label="Right Hip",
)


# Menampilkan knee kiri.
plt.plot(
    time,
    np.rad2deg(
        left_knee
    ),
    "--",
    label="Left Knee",
)


# Menampilkan knee kanan.
plt.plot(
    time,
    np.rad2deg(
        right_knee
    ),
    "--",
    label="Right Knee",
)


# Mengatur plot.
plt.xlabel(
    "Time (s)"
)

plt.ylabel(
    "Joint Angle (degree)"
)

plt.title(
    "Biped Locomotion Joint Trajectories"
)

plt.grid(
    alpha=0.3
)

plt.legend()

plt.tight_layout()


# Menyimpan hasil visualisasi.
plt.savefig(
    IMAGE_OUTPUT_PATH,
    dpi=200,
)


print(
    "\nHasil visualisasi disimpan ke:",
    IMAGE_OUTPUT_PATH,
)


# Membuat figure untuk animasi.
fig, ax = plt.subplots(
    figsize=(
        9,
        6,
    )
)


# Mengatur batas plot.
ax.set_ylim(
    -0.1,
    1.8,
)

ax.set_xlim(
    -0.5,
    pelvis_x[-1] + 1.0,
)


# Mengatur rasio plot.
ax.set_aspect(
    "equal"
)


# Mengatur label plot.
ax.set_xlabel(
    "X Position (m)"
)

ax.set_ylabel(
    "Y Position (m)"
)

ax.set_title(
    "Simple Biped Locomotion"
)

ax.grid(
    alpha=0.3
)


# Menampilkan ground.
ax.axhline(
    y=0,
    linewidth=1,
)


# Membuat kaki kiri.
left_leg_line, = ax.plot(
    [],
    [],
    "-o",
    linewidth=3,
    label="Left Leg",
)


# Membuat kaki kanan.
right_leg_line, = ax.plot(
    [],
    [],
    "--o",
    linewidth=3,
    label="Right Leg",
)


# Membuat torso.
torso_line, = ax.plot(
    [],
    [],
    linewidth=5,
    label="Body",
)


# Membuat head.
head_marker, = ax.plot(
    [],
    [],
    "o",
    markersize=12,
)


# Membuat trajectory pelvis.
pelvis_path, = ax.plot(
    [],
    [],
    ":",
    linewidth=1,
    label="Pelvis Trajectory",
)


# Menampilkan legend.
ax.legend()


def update_animation(
    frame,
):
    # Membaca posisi hip.
    hip = np.array(
        [
            pelvis_x[frame],
            pelvis_y[frame],
        ]
    )


    # Memperbarui kaki kiri.
    left_leg_line.set_data(
        [
            hip[0],
            left_knee_position[
                frame,
                0,
            ],
            left_foot_position[
                frame,
                0,
            ],
        ],
        [
            hip[1],
            left_knee_position[
                frame,
                1,
            ],
            left_foot_position[
                frame,
                1,
            ],
        ],
    )


    # Memperbarui kaki kanan.
    right_leg_line.set_data(
        [
            hip[0],
            right_knee_position[
                frame,
                0,
            ],
            right_foot_position[
                frame,
                0,
            ],
        ],
        [
            hip[1],
            right_knee_position[
                frame,
                1,
            ],
            right_foot_position[
                frame,
                1,
            ],
        ],
    )


    # Menghitung posisi atas torso.
    torso_top = np.array(
        [
            hip[0],
            hip[1]
            + BODY_HEIGHT,
        ]
    )


    # Memperbarui torso.
    torso_line.set_data(
        [
            hip[0],
            torso_top[0],
        ],
        [
            hip[1],
            torso_top[1],
        ],
    )


    # Memperbarui head.
    head_marker.set_data(
        [
            torso_top[0]
        ],
        [
            torso_top[1]
            + HEAD_RADIUS
        ],
    )


    # Memperbarui trajectory pelvis.
    pelvis_path.set_data(
        pelvis_x[
            :frame + 1
        ],
        pelvis_y[
            :frame + 1
        ],
    )


    return (
        left_leg_line,
        right_leg_line,
        torso_line,
        head_marker,
        pelvis_path,
    )


# Membuat animasi.
animation = FuncAnimation(
    fig,
    update_animation,
    frames=len(
        time
    ),
    interval=50,
    blit=True,
)


# Menyimpan animasi sebagai GIF.
animation.save(
    GIF_OUTPUT_PATH,
    writer=PillowWriter(
        fps=20
    ),
)


print(
    "Animasi disimpan ke:",
    GIF_OUTPUT_PATH,
)


# Menampilkan hasil.
plt.show()
