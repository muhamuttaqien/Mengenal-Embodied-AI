# Import NumPy untuk operasi numerik.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import animation untuk membuat GIF.
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

# Import Circle untuk menggambar obstacle dan robot.
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
    / "dynamic_navigation_result.png"
)


# Menentukan file hasil animasi.
GIF_OUTPUT_PATH = (
    RESULTS_DIR
    / "dynamic_navigation.gif"
)


# Menentukan posisi awal dan goal.
START = np.array(
    [
        1.0,
        1.0,
    ]
)

GOAL = np.array(
    [
        9.0,
        8.0,
    ]
)


# Menentukan parameter gerakan.
STEP_SIZE = 0.08
GOAL_THRESHOLD = 0.20


# Menentukan radius robot.
ROBOT_RADIUS = 0.20


# Menentukan parameter navigation force.
ATTRACTIVE_GAIN = 1.0
REPULSIVE_GAIN = 1.0
INFLUENCE_DISTANCE = 1.6


# Menentukan jumlah langkah maksimum.
MAX_STEPS = 800


# Menentukan obstacle statis.
static_obstacles = [
    (
        np.array(
            [
                4.0,
                4.5,
            ]
        ),
        0.60,
    ),
    (
        np.array(
            [
                7.0,
                6.0,
            ]
        ),
        0.70,
    ),
]


# Menentukan obstacle dinamis.
dynamic_position = np.array(
    [
        5.0,
        1.5,
    ]
)

dynamic_velocity = np.array(
    [
        0.0,
        0.05,
    ]
)

DYNAMIC_RADIUS = 0.55


def update_dynamic_obstacle(
    position,
    velocity,
):
    # Menghitung posisi obstacle berikutnya.
    new_position = (
        position
        + velocity
    )


    # Membalik arah jika mencapai batas.
    if (
        new_position[1] < 1.2
        or new_position[1] > 7.8
    ):

        velocity = (
            velocity.copy()
        )

        velocity[1] *= -1

        new_position = (
            position
            + velocity
        )


    # Mengembalikan posisi dan velocity baru.
    return (
        new_position,
        velocity,
    )


def get_obstacles(
    dynamic_pos,
):
    # Menggabungkan obstacle statis dan dinamis.
    return (
        static_obstacles
        + [
            (
                dynamic_pos,
                DYNAMIC_RADIUS,
            )
        ]
    )


def is_collision(
    position,
    dynamic_pos,
):
    # Memeriksa collision dengan semua obstacle.
    for center, radius in get_obstacles(
        dynamic_pos
    ):

        # Menghitung jarak ke obstacle.
        distance = np.linalg.norm(
            position - center
        )


        # Memeriksa collision.
        if (
            distance
            <= radius + ROBOT_RADIUS
        ):

            return True


    return False


def attractive_force(
    position,
):
    # Menghitung vector menuju goal.
    vector = (
        GOAL - position
    )


    # Menghitung jarak menuju goal.
    distance = np.linalg.norm(
        vector
    )


    # Menghindari pembagian dengan nol.
    if distance < 1e-8:

        return np.zeros(
            2
        )


    # Menghasilkan attractive force.
    return (
        ATTRACTIVE_GAIN
        * vector
        / distance
    )


def repulsive_force(
    position,
    dynamic_pos,
):
    # Menyiapkan repulsive force.
    force = np.zeros(
        2
    )


    # Memeriksa semua obstacle.
    for center, radius in get_obstacles(
        dynamic_pos
    ):

        # Menghitung vector dari obstacle ke robot.
        vector = (
            position - center
        )


        # Menghitung jarak ke pusat obstacle.
        center_distance = np.linalg.norm(
            vector
        )


        # Menghindari pembagian dengan nol.
        if center_distance < 1e-8:

            continue


        # Menghitung jarak permukaan robot ke obstacle.
        distance = (
            center_distance
            - radius
            - ROBOT_RADIUS
        )


        # Mengaktifkan repulsive force di dekat obstacle.
        if distance < INFLUENCE_DISTANCE:

            # Menghindari nilai terlalu kecil.
            distance = max(
                distance,
                0.03,
            )


            # Menghitung arah menjauhi obstacle.
            direction = (
                vector
                / center_distance
            )


            # Menghitung besar repulsive force.
            magnitude = (
                REPULSIVE_GAIN
                * (
                    1 / distance
                    - 1 / INFLUENCE_DISTANCE
                )
                / (
                    distance ** 2
                )
            )


            # Menambahkan repulsive force.
            force += (
                magnitude
                * direction
            )


    return force


def find_safe_direction(
    position,
    direction,
    dynamic_pos,
):
    # Menghitung arah dasar robot.
    base_angle = np.arctan2(
        direction[1],
        direction[0],
    )


    # Menentukan alternatif arah.
    test_angles = [
        20,
        -20,
        40,
        -40,
        60,
        -60,
        90,
        -90,
        120,
        -120,
        160,
        -160,
        180,
    ]


    # Menyimpan kandidat gerakan.
    candidates = []


    # Memeriksa setiap arah alternatif.
    for angle_degree in test_angles:

        # Menghitung arah baru.
        angle = (
            base_angle
            + np.deg2rad(
                angle_degree
            )
        )


        # Membuat vector arah.
        test_direction = np.array(
            [
                np.cos(angle),
                np.sin(angle),
            ]
        )


        # Menghitung posisi kandidat.
        candidate = (
            position
            + STEP_SIZE
            * test_direction
        )


        # Memeriksa collision.
        if not is_collision(
            candidate,
            dynamic_pos,
        ):

            # Menghitung jarak kandidat ke goal.
            distance_to_goal = (
                np.linalg.norm(
                    GOAL
                    - candidate
                )
            )


            # Menyimpan kandidat.
            candidates.append(
                (
                    distance_to_goal,
                    candidate,
                )
            )


    # Tetap diam jika tidak ada arah aman.
    if len(candidates) == 0:

        return position


    # Mengurutkan kandidat berdasarkan jarak ke goal.
    candidates.sort(
        key=lambda item: item[0]
    )


    # Memilih kandidat terbaik.
    return candidates[0][1]


# Menentukan posisi awal robot.
robot_position = (
    START.copy()
)


# Menyimpan trajectory robot.
trajectory = [
    robot_position.copy()
]


# Menyimpan trajectory obstacle dinamis.
dynamic_trajectory = [
    dynamic_position.copy()
]


# Menyimpan posisi obstacle pada setiap step.
dynamic_positions_per_step = [
    dynamic_position.copy()
]


# Menyimpan status goal.
goal_reached = False


# Menjalankan reactive navigation.
for step in range(
    MAX_STEPS
):

    # Menggerakkan obstacle dinamis.
    dynamic_position, dynamic_velocity = (
        update_dynamic_obstacle(
            dynamic_position,
            dynamic_velocity,
        )
    )


    # Menyimpan trajectory obstacle.
    dynamic_trajectory.append(
        dynamic_position.copy()
    )


    # Menghitung jarak menuju goal.
    distance_to_goal = np.linalg.norm(
        GOAL - robot_position
    )


    # Menampilkan status navigation.
    print(
        f"Step {step + 1:03d} | "
        f"Robot: "
        f"({robot_position[0]:.2f}, "
        f"{robot_position[1]:.2f}) | "
        f"Dynamic obstacle: "
        f"({dynamic_position[0]:.2f}, "
        f"{dynamic_position[1]:.2f}) | "
        f"Goal distance: "
        f"{distance_to_goal:.2f} m"
    )


    # Memeriksa apakah goal sudah tercapai.
    if (
        distance_to_goal
        < GOAL_THRESHOLD
    ):

        print(
            "\nGoal reached!"
        )

        goal_reached = True

        break


    # Menghitung attractive force.
    attraction = attractive_force(
        robot_position
    )


    # Menghitung repulsive force.
    repulsion = repulsive_force(
        robot_position,
        dynamic_position,
    )


    # Menggabungkan navigation force.
    navigation_vector = (
        attraction
        + repulsion
    )


    # Menghitung magnitude vector.
    vector_norm = np.linalg.norm(
        navigation_vector
    )


    # Menggunakan attractive force jika vector terlalu kecil.
    if vector_norm < 1e-8:

        navigation_vector = (
            attraction
        )

        vector_norm = np.linalg.norm(
            navigation_vector
        )


    # Menormalisasi arah gerak.
    direction = (
        navigation_vector
        / vector_norm
    )


    # Menghitung posisi berikutnya.
    next_position = (
        robot_position
        + STEP_SIZE
        * direction
    )


    # Mencari arah lain jika collision terdeteksi.
    if is_collision(
        next_position,
        dynamic_position,
    ):

        next_position = (
            find_safe_direction(
                robot_position,
                direction,
                dynamic_position,
            )
        )


    # Memperbarui posisi robot.
    robot_position = (
        next_position
    )


    # Menyimpan trajectory robot.
    trajectory.append(
        robot_position.copy()
    )


    # Menyimpan posisi obstacle dinamis.
    dynamic_positions_per_step.append(
        dynamic_position.copy()
    )


# Menampilkan pesan jika goal belum tercapai.
if not goal_reached:

    print(
        "\nMaximum steps reached "
        "before reaching the goal."
    )


# Mengubah trajectory menjadi NumPy array.
trajectory = np.array(
    trajectory
)

dynamic_trajectory = np.array(
    dynamic_trajectory
)

dynamic_positions_per_step = np.array(
    dynamic_positions_per_step
)


# Membuat visualisasi hasil navigation.
fig, ax = plt.subplots(
    figsize=(
        8,
        7,
    )
)


# Menggambar obstacle statis.
for center, radius in static_obstacles:

    obstacle = Circle(
        center,
        radius,
        alpha=0.7,
    )

    ax.add_patch(
        obstacle
    )


# Menggambar trajectory obstacle dinamis.
ax.plot(
    dynamic_trajectory[:, 0],
    dynamic_trajectory[:, 1],
    "--",
    linewidth=1.5,
    label="Dynamic Obstacle Path",
)


# Menggambar trajectory robot.
ax.plot(
    trajectory[:, 0],
    trajectory[:, 1],
    "-",
    linewidth=2,
    label="Robot Trajectory",
)


# Menampilkan posisi awal.
ax.scatter(
    START[0],
    START[1],
    marker="s",
    s=100,
    label="Start",
)


# Menampilkan goal.
ax.scatter(
    GOAL[0],
    GOAL[1],
    marker="*",
    s=180,
    label="Goal",
)


# Mengatur plot.
ax.set_xlabel(
    "X Position (m)"
)

ax.set_ylabel(
    "Y Position (m)"
)

ax.set_title(
    "Reactive Navigation with Dynamic Obstacle"
)

ax.set_xlim(
    0,
    10,
)

ax.set_ylim(
    0,
    9,
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


# Menggambar obstacle statis.
for center, radius in static_obstacles:

    obstacle = Circle(
        center,
        radius,
        alpha=0.7,
    )

    ax_anim.add_patch(
        obstacle
    )


# Menampilkan posisi awal.
ax_anim.scatter(
    START[0],
    START[1],
    marker="s",
    s=100,
    label="Start",
)


# Menampilkan goal.
ax_anim.scatter(
    GOAL[0],
    GOAL[1],
    marker="*",
    s=180,
    label="Goal",
)


# Membuat robot.
robot_circle = Circle(
    START,
    ROBOT_RADIUS,
    fill=False,
    linewidth=2,
)


# Membuat obstacle dinamis.
dynamic_circle = Circle(
    dynamic_positions_per_step[0],
    DYNAMIC_RADIUS,
    alpha=0.7,
)


# Menambahkan robot dan obstacle.
ax_anim.add_patch(
    robot_circle
)

ax_anim.add_patch(
    dynamic_circle
)


# Membuat garis trajectory robot.
robot_path_line, = ax_anim.plot(
    [],
    [],
    "-",
    linewidth=2,
    label="Robot Trajectory",
)


# Mengatur plot animasi.
ax_anim.set_xlabel(
    "X Position (m)"
)

ax_anim.set_ylabel(
    "Y Position (m)"
)

ax_anim.set_title(
    "Reactive Navigation with Dynamic Obstacle"
)

ax_anim.set_xlim(
    0,
    10,
)

ax_anim.set_ylim(
    0,
    9,
)

ax_anim.set_aspect(
    "equal"
)

ax_anim.grid(
    alpha=0.3
)

ax_anim.legend()


def update_animation(
    frame,
):
    # Membaca posisi robot.
    robot_position = (
        trajectory[frame]
    )


    # Menentukan index obstacle.
    dynamic_index = min(
        frame,
        len(
            dynamic_positions_per_step
        )
        - 1,
    )


    # Membaca posisi obstacle.
    obstacle_position = (
        dynamic_positions_per_step[
            dynamic_index
        ]
    )


    # Memperbarui posisi robot.
    robot_circle.center = (
        robot_position
    )


    # Memperbarui posisi obstacle.
    dynamic_circle.center = (
        obstacle_position
    )


    # Memperbarui trajectory robot.
    robot_path_line.set_data(
        trajectory[
            :frame + 1,
            0,
        ],
        trajectory[
            :frame + 1,
            1,
        ],
    )


    return (
        robot_circle,
        dynamic_circle,
        robot_path_line,
    )


# Membuat animasi.
animation = FuncAnimation(
    fig_anim,
    update_animation,
    frames=len(
        trajectory
    ),
    interval=60,
    blit=True,
)


# Menyimpan animasi sebagai GIF.
animation.save(
    GIF_OUTPUT_PATH,
    writer=PillowWriter(
        fps=15
    ),
)


print(
    "Animasi disimpan ke:",
    GIF_OUTPUT_PATH,
)


# Menampilkan hasil.
plt.show()
