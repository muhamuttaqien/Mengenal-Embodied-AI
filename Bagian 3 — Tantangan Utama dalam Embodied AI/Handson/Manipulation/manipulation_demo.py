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

# Menentukan file hasil gambar.
IMAGE_OUTPUT_PATH = (
    RESULTS_DIR
    / "manipulation_result.png"
)

# Menentukan file hasil animasi.
GIF_OUTPUT_PATH = (
    RESULTS_DIR
    / "manipulation_animation.gif"
)


# Menentukan panjang link robot.
LINK_1 = 2.0
LINK_2 = 1.5

# Menentukan posisi base robot.
BASE = np.array(
    [
        0.0,
        0.0,
    ]
)


# Menentukan posisi penting.
HOME = np.array(
    [
        2.4,
        2.0,
    ]
)

OBJECT_START = np.array(
    [
        2.2,
        1.0,
    ]
)

OBJECT_APPROACH = np.array(
    [
        2.2,
        1.4,
    ]
)

PLACE_POSITION = np.array(
    [
        -1.3,
        2.0,
    ]
)

PLACE_APPROACH = np.array(
    [
        -1.3,
        2.4,
    ]
)


def inverse_kinematics(
    x,
    y,
):
    # Menghitung sudut joint kedua.
    cos_q2 = (
        x ** 2
        + y ** 2
        - LINK_1 ** 2
        - LINK_2 ** 2
    ) / (
        2
        * LINK_1
        * LINK_2
    )

    # Membatasi nilai agar tetap valid.
    cos_q2 = np.clip(
        cos_q2,
        -1.0,
        1.0,
    )

    # Menghitung q2.
    q2 = np.arccos(
        cos_q2
    )

    # Menghitung q1.
    q1 = (
        np.arctan2(
            y,
            x,
        )
        - np.arctan2(
            LINK_2
            * np.sin(q2),
            LINK_1
            + LINK_2
            * np.cos(q2),
        )
    )

    return (
        q1,
        q2,
    )


def forward_kinematics(
    q1,
    q2,
):
    # Menentukan posisi base.
    joint_1 = BASE

    # Menghitung posisi joint kedua.
    joint_2 = np.array(
        [
            LINK_1
            * np.cos(q1),

            LINK_1
            * np.sin(q1),
        ]
    )

    # Menghitung posisi end-effector.
    end_effector = np.array(
        [
            joint_2[0]
            + LINK_2
            * np.cos(
                q1 + q2
            ),

            joint_2[1]
            + LINK_2
            * np.sin(
                q1 + q2
            ),
        ]
    )

    return (
        joint_1,
        joint_2,
        end_effector,
    )


def interpolate(
    start,
    end,
    steps=30,
):
    # Membuat trajectory linear.
    return np.linspace(
        start,
        end,
        steps,
    )


# Menyiapkan trajectory end-effector.
trajectory = []


# Bergerak dari home ke atas object.
trajectory.extend(
    interpolate(
        HOME,
        OBJECT_APPROACH,
    )
)


# Bergerak turun menuju object.
trajectory.extend(
    interpolate(
        OBJECT_APPROACH,
        OBJECT_START,
    )
)


# Menentukan waktu grasp.
grasp_index = (
    len(trajectory)
    - 1
)


# Mengangkat object.
trajectory.extend(
    interpolate(
        OBJECT_START,
        OBJECT_APPROACH,
    )
)


# Bergerak menuju area place.
trajectory.extend(
    interpolate(
        OBJECT_APPROACH,
        PLACE_APPROACH,
        steps=50,
    )
)


# Bergerak turun menuju posisi place.
trajectory.extend(
    interpolate(
        PLACE_APPROACH,
        PLACE_POSITION,
    )
)


# Menentukan waktu release.
release_index = (
    len(trajectory)
    - 1
)


# Bergerak naik setelah release.
trajectory.extend(
    interpolate(
        PLACE_POSITION,
        PLACE_APPROACH,
    )
)


# Kembali ke home.
trajectory.extend(
    interpolate(
        PLACE_APPROACH,
        HOME,
        steps=50,
    )
)


# Mengubah trajectory menjadi NumPy array.
trajectory = np.array(
    trajectory
)


# Menyimpan joint history.
joint_history = []

# Menyimpan end-effector history.
end_effector_history = []

# Menentukan posisi awal object.
object_position = (
    OBJECT_START.copy()
)

# Menyimpan object history.
object_history = []

# Menentukan status grasp.
holding_object = False


# Menjalankan trajectory.
for step, target in enumerate(
    trajectory
):

    # Membaca target end-effector.
    x, y = target

    # Menghitung inverse kinematics.
    q1, q2 = inverse_kinematics(
        x,
        y,
    )

    # Menghitung forward kinematics.
    joint_1, joint_2, end_effector = (
        forward_kinematics(
            q1,
            q2,
        )
    )

    # Menyimpan joint state.
    joint_history.append(
        (
            q1,
            q2,
            joint_2.copy(),
        )
    )

    # Menyimpan posisi end-effector.
    end_effector_history.append(
        end_effector.copy()
    )

    # Melakukan grasp.
    if step == grasp_index:

        holding_object = True

        print(
            "Object grasped."
        )

    # Membawa object bersama end-effector.
    if holding_object:

        object_position = (
            end_effector.copy()
        )

    # Melakukan release.
    if step == release_index:

        holding_object = False

        object_position = (
            PLACE_POSITION.copy()
        )

        print(
            "Object released."
        )

    # Menyimpan posisi object.
    object_history.append(
        object_position.copy()
    )


# Mengubah joint history menjadi NumPy array.
joint_history = np.array(
    [
        [
            q1,
            q2,
            joint_2[0],
            joint_2[1],
        ]
        for q1, q2, joint_2
        in joint_history
    ]
)


# Mengubah history menjadi NumPy array.
end_effector_history = np.array(
    end_effector_history
)

object_history = np.array(
    object_history
)


# Menampilkan status akhir.
print(
    "Manipulation task completed."
)


# Membuat visualisasi statis.
fig, ax = plt.subplots(
    figsize=(
        8,
        7,
    )
)


# Menampilkan trajectory end-effector.
ax.plot(
    end_effector_history[:, 0],
    end_effector_history[:, 1],
    "--",
    linewidth=1.5,
    label="End-Effector Trajectory",
)


# Menampilkan posisi awal object.
ax.scatter(
    OBJECT_START[0],
    OBJECT_START[1],
    marker="s",
    s=100,
    label="Object Start",
)


# Menampilkan target place.
ax.scatter(
    PLACE_POSITION[0],
    PLACE_POSITION[1],
    marker="*",
    s=180,
    label="Place Target",
)


# Membaca konfigurasi robot terakhir.
q1 = joint_history[
    -1,
    0,
]

q2 = joint_history[
    -1,
    1,
]


# Menghitung posisi robot terakhir.
_, joint_2, end_effector = (
    forward_kinematics(
        q1,
        q2,
    )
)


# Menggambar robot arm.
ax.plot(
    [
        BASE[0],
        joint_2[0],
        end_effector[0],
    ],
    [
        BASE[1],
        joint_2[1],
        end_effector[1],
    ],
    "-o",
    linewidth=4,
    label="Robot Arm",
)


# Menampilkan posisi akhir object.
ax.scatter(
    object_history[
        -1,
        0,
    ],
    object_history[
        -1,
        1,
    ],
    marker="s",
    s=120,
    label="Placed Object",
)


# Mengatur plot.
ax.set_xlabel(
    "X Position (m)"
)

ax.set_ylabel(
    "Y Position (m)"
)

ax.set_title(
    "Robot Manipulation: Pick and Place"
)

ax.set_xlim(
    -4,
    4,
)

ax.set_ylim(
    -0.5,
    4,
)

ax.set_aspect(
    "equal"
)

ax.grid(
    alpha=0.3
)

ax.legend()

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
fig_anim, ax_anim = plt.subplots(
    figsize=(
        8,
        7,
    )
)


# Mengatur plot animasi.
ax_anim.set_xlim(
    -4,
    4,
)

ax_anim.set_ylim(
    -0.5,
    4,
)

ax_anim.set_aspect(
    "equal"
)

ax_anim.set_xlabel(
    "X Position (m)"
)

ax_anim.set_ylabel(
    "Y Position (m)"
)

ax_anim.set_title(
    "Pick-and-Place Manipulation"
)

ax_anim.grid(
    alpha=0.3
)


# Menampilkan garis workspace.
ax_anim.axhline(
    y=0.7,
    linewidth=1,
)


# Menampilkan target place.
ax_anim.scatter(
    PLACE_POSITION[0],
    PLACE_POSITION[1],
    marker="*",
    s=150,
    label="Place Target",
)


# Membuat robot arm.
robot_line, = ax_anim.plot(
    [],
    [],
    "-o",
    linewidth=4,
    markersize=8,
    label="Robot Arm",
)


# Membuat end-effector path.
ee_path, = ax_anim.plot(
    [],
    [],
    "--",
    linewidth=1,
    label="End-Effector Path",
)


# Membuat marker object.
object_marker, = ax_anim.plot(
    [],
    [],
    "s",
    markersize=10,
    label="Object",
)


# Menampilkan legend.
ax_anim.legend()


def update_animation(
    frame,
):
    # Membaca joint angle.
    q1 = joint_history[
        frame,
        0,
    ]

    q2 = joint_history[
        frame,
        1,
    ]

    # Menghitung posisi robot.
    joint_1, joint_2, end_effector = (
        forward_kinematics(
            q1,
            q2,
        )
    )

    # Memperbarui robot arm.
    robot_line.set_data(
        [
            joint_1[0],
            joint_2[0],
            end_effector[0],
        ],
        [
            joint_1[1],
            joint_2[1],
            end_effector[1],
        ],
    )

    # Memperbarui trajectory end-effector.
    ee_path.set_data(
        end_effector_history[
            :frame + 1,
            0,
        ],
        end_effector_history[
            :frame + 1,
            1,
        ],
    )

    # Memperbarui posisi object.
    object_marker.set_data(
        [
            object_history[
                frame,
                0,
            ]
        ],
        [
            object_history[
                frame,
                1,
            ]
        ],
    )

    return (
        robot_line,
        ee_path,
        object_marker,
    )


# Membuat animasi.
animation = FuncAnimation(
    fig_anim,
    update_animation,
    frames=len(
        trajectory
    ),
    interval=40,
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
