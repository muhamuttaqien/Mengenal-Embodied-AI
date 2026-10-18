# Import NumPy untuk operasi numerik.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import animation untuk membuat GIF.
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

# Import Circle untuk menggambar obstacle.
from matplotlib.patches import Circle

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
    / "manipulation_obstacle_result.png"
)

# Menentukan file hasil animasi.
GIF_OUTPUT_PATH = (
    RESULTS_DIR
    / "manipulation_obstacle_animation.gif"
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


# Menentukan posisi home.
HOME = np.array(
    [
        2.4,
        2.2,
    ]
)


# Menentukan posisi awal object.
OBJECT_START = np.array(
    [
        2.2,
        0.9,
    ]
)


# Menentukan posisi approach object.
OBJECT_APPROACH = np.array(
    [
        2.2,
        1.4,
    ]
)


# Menentukan posisi place.
PLACE_POSITION = np.array(
    [
        -1.5,
        1.1,
    ]
)


# Menentukan posisi approach place.
PLACE_APPROACH = np.array(
    [
        -1.5,
        1.6,
    ]
)


# Menentukan waypoint aman.
SAFE_WAYPOINT = np.array(
    [
        0.2,
        3.0,
    ]
)


# Menentukan obstacle.
OBSTACLE_CENTER = np.array(
    [
        0.3,
        1.7,
    ]
)

OBSTACLE_RADIUS = 0.55


# Menentukan safety margin.
SAFETY_MARGIN = 0.15


def inverse_kinematics(
    x,
    y,
):
    # Menghitung nilai cos q2.
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


    # Memeriksa apakah target dapat dijangkau.
    if (
        cos_q2 < -1.0
        or cos_q2 > 1.0
    ):

        raise ValueError(
            f"Target ({x:.2f}, {y:.2f}) "
            "is outside the robot workspace."
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
    joint_1 = (
        BASE.copy()
    )


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


def point_to_segment_distance(
    point,
    segment_start,
    segment_end,
):
    # Menghitung vector segment.
    segment = (
        segment_end
        - segment_start
    )


    # Menghitung panjang segment.
    length_squared = np.dot(
        segment,
        segment,
    )


    # Menangani segment dengan panjang nol.
    if length_squared == 0:

        return np.linalg.norm(
            point
            - segment_start
        )


    # Menghitung posisi projection.
    t = np.dot(
        point
        - segment_start,
        segment,
    ) / length_squared


    # Membatasi projection pada segment.
    t = np.clip(
        t,
        0.0,
        1.0,
    )


    # Menghitung titik projection.
    projection = (
        segment_start
        + t
        * segment
    )


    # Menghitung jarak point ke segment.
    return np.linalg.norm(
        point
        - projection
    )


def robot_in_collision(
    joint_1,
    joint_2,
    end_effector,
):
    # Menentukan batas aman obstacle.
    threshold = (
        OBSTACLE_RADIUS
        + SAFETY_MARGIN
    )


    # Menghitung jarak obstacle ke link pertama.
    link_1_distance = (
        point_to_segment_distance(
            OBSTACLE_CENTER,
            joint_1,
            joint_2,
        )
    )


    # Menghitung jarak obstacle ke link kedua.
    link_2_distance = (
        point_to_segment_distance(
            OBSTACLE_CENTER,
            joint_2,
            end_effector,
        )
    )


    # Memeriksa collision.
    return (
        link_1_distance
        < threshold
        or link_2_distance
        < threshold
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


# Menyiapkan trajectory.
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


# Bergerak menuju safe waypoint.
trajectory.extend(
    interpolate(
        OBJECT_APPROACH,
        SAFE_WAYPOINT,
        steps=45,
    )
)


# Bergerak dari safe waypoint menuju place.
trajectory.extend(
    interpolate(
        SAFE_WAYPOINT,
        PLACE_APPROACH,
        steps=45,
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


# Kembali menuju safe waypoint.
trajectory.extend(
    interpolate(
        PLACE_APPROACH,
        SAFE_WAYPOINT,
        steps=45,
    )
)


# Kembali ke home.
trajectory.extend(
    interpolate(
        SAFE_WAYPOINT,
        HOME,
        steps=45,
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

# Menyimpan object history.
object_history = []


# Menentukan status grasp.
holding_object = False


# Menentukan posisi awal object.
object_position = (
    OBJECT_START.copy()
)


# Menentukan status collision.
collision_detected = False


# Menjalankan trajectory.
for step, target in enumerate(
    trajectory
):

    # Menghitung inverse kinematics.
    q1, q2 = inverse_kinematics(
        target[0],
        target[1],
    )


    # Menghitung forward kinematics.
    (
        joint_1,
        joint_2,
        end_effector,
    ) = forward_kinematics(
        q1,
        q2,
    )


    # Memeriksa collision.
    if robot_in_collision(
        joint_1,
        joint_2,
        end_effector,
    ):

        collision_detected = True

        print(
            f"Warning: collision risk "
            f"at step {step}."
        )


    # Menyimpan joint state.
    joint_history.append(
        [
            q1,
            q2,
            joint_2[0],
            joint_2[1],
        ]
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


# Mengubah history menjadi NumPy array.
joint_history = np.array(
    joint_history
)

end_effector_history = np.array(
    end_effector_history
)

object_history = np.array(
    object_history
)


# Menampilkan status task.
print(
    "Manipulation task completed."
)


# Menampilkan status collision.
if not collision_detected:

    print(
        "Trajectory completed without "
        "detected link-obstacle collision."
    )


# Membuat visualisasi statis.
fig, ax = plt.subplots(
    figsize=(
        8,
        7,
    )
)


# Membuat obstacle.
obstacle = Circle(
    OBSTACLE_CENTER,
    OBSTACLE_RADIUS,
    alpha=0.7,
    label="Obstacle",
)


# Menampilkan obstacle.
ax.add_patch(
    obstacle
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


# Menampilkan safe waypoint.
ax.scatter(
    SAFE_WAYPOINT[0],
    SAFE_WAYPOINT[1],
    marker="^",
    s=100,
    label="Safe Waypoint",
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
(
    joint_1,
    joint_2,
    end_effector,
) = forward_kinematics(
    q1,
    q2,
)


# Menampilkan robot arm.
ax.plot(
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
    "Pick-and-Place with Obstacle Avoidance"
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

ax.legend(
    fontsize=8
)

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
    "Pick-and-Place with Obstacle Avoidance"
)

ax_anim.grid(
    alpha=0.3
)


# Membuat obstacle pada animasi.
obstacle_anim = Circle(
    OBSTACLE_CENTER,
    OBSTACLE_RADIUS,
    alpha=0.7,
    label="Obstacle",
)


# Menampilkan obstacle.
ax_anim.add_patch(
    obstacle_anim
)


# Menampilkan target place.
ax_anim.scatter(
    PLACE_POSITION[0],
    PLACE_POSITION[1],
    marker="*",
    s=150,
    label="Place Target",
)


# Menampilkan safe waypoint.
ax_anim.scatter(
    SAFE_WAYPOINT[0],
    SAFE_WAYPOINT[1],
    marker="^",
    s=80,
    label="Safe Waypoint",
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
ax_anim.legend(
    fontsize=8
)


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
    (
        joint_1,
        joint_2,
        end_effector,
    ) = forward_kinematics(
        q1,
        q2,
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


    # Memperbarui end-effector path.
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
