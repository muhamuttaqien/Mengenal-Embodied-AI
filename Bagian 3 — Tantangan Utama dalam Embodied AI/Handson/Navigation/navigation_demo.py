# Import NumPy untuk operasi numerik.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

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


# Menentukan file hasil.
OUTPUT_PATH = (
    RESULTS_DIR
    / "navigation_result.png"
)


# Menentukan posisi awal dan tujuan.
START = np.array(
    [
        2.0,
        2.0,
    ]
)

GOAL = np.array(
    [
        18.0,
        13.0,
    ]
)


# Menentukan parameter gerakan.
STEP_SIZE = 0.18
GOAL_THRESHOLD = 0.35


# Menentukan radius robot.
ROBOT_RADIUS = 0.25


# Menentukan parameter navigation force.
ATTRACTIVE_GAIN = 1.0
REPULSIVE_GAIN = 1.2
INFLUENCE_DISTANCE = 3.0


# Menentukan jumlah langkah maksimum.
MAX_STEPS = 1000


# Menentukan obstacle.
obstacles = [
    (
        np.array(
            [
                7.0,
                5.5,
            ]
        ),
        1.4,
    ),
    (
        np.array(
            [
                10.0,
                8.0,
            ]
        ),
        1.6,
    ),
    (
        np.array(
            [
                13.0,
                10.0,
            ]
        ),
        1.3,
    ),
]


def is_collision(
    position,
):
    # Memeriksa collision dengan setiap obstacle.
    for center, radius in obstacles:

        # Menghitung jarak ke pusat obstacle.
        distance = np.linalg.norm(
            position - center
        )


        # Memeriksa apakah robot menyentuh obstacle.
        if (
            distance
            <= radius + ROBOT_RADIUS
        ):

            return True


    return False


def attractive_force(
    position,
):
    # Menghitung arah menuju goal.
    direction = (
        GOAL - position
    )


    # Menghitung jarak menuju goal.
    distance = np.linalg.norm(
        direction
    )


    # Menghindari pembagian dengan nol.
    if distance == 0:

        return np.zeros(
            2
        )


    # Menghasilkan attractive force.
    return (
        ATTRACTIVE_GAIN
        * direction
        / distance
    )


def repulsive_force(
    position,
):
    # Menyiapkan repulsive force.
    force = np.zeros(
        2
    )


    # Memeriksa setiap obstacle.
    for center, radius in obstacles:

        # Menghitung vector dari obstacle ke robot.
        vector = (
            position - center
        )


        # Menghitung jarak ke pusat obstacle.
        center_distance = np.linalg.norm(
            vector
        )


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
                0.05,
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
):
    # Menentukan alternatif arah gerak.
    test_angles = [
        30,
        -30,
        60,
        -60,
        90,
        -90,
        120,
        -120,
        180,
    ]


    # Menyimpan kandidat gerakan.
    candidates = []


    # Memeriksa setiap arah alternatif.
    for angle_degree in test_angles:

        # Mengubah sudut menjadi radian.
        angle = np.deg2rad(
            angle_degree
        )


        # Membuat rotation matrix.
        rotation = np.array(
            [
                [
                    np.cos(angle),
                    -np.sin(angle),
                ],
                [
                    np.sin(angle),
                    np.cos(angle),
                ],
            ]
        )


        # Memutar arah gerak.
        new_direction = (
            rotation
            @ direction
        )


        # Menghitung posisi kandidat.
        candidate_position = (
            position
            + STEP_SIZE
            * new_direction
        )


        # Memeriksa collision.
        if not is_collision(
            candidate_position
        ):

            # Menghitung jarak kandidat ke goal.
            distance_to_goal = (
                np.linalg.norm(
                    GOAL
                    - candidate_position
                )
            )


            # Menyimpan kandidat.
            candidates.append(
                (
                    distance_to_goal,
                    candidate_position,
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
position = START.copy()


# Menyimpan trajectory robot.
trajectory = [
    position.copy()
]


# Menyimpan status goal.
goal_reached = False


# Menjalankan proses navigation.
for step in range(
    MAX_STEPS
):

    # Menghitung jarak menuju goal.
    distance_to_goal = np.linalg.norm(
        GOAL - position
    )


    # Menampilkan status robot.
    print(
        f"Step {step + 1:03d} | "
        f"Position: "
        f"({position[0]:.2f}, "
        f"{position[1]:.2f}) | "
        f"Distance to goal: "
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
        position
    )


    # Menghitung repulsive force.
    repulsion = repulsive_force(
        position
    )


    # Menggabungkan kedua force.
    navigation_vector = (
        attraction
        + repulsion
    )


    # Menghitung magnitude vector.
    vector_norm = np.linalg.norm(
        navigation_vector
    )


    # Menggunakan attractive force jika vector terlalu kecil.
    if vector_norm < 1e-6:

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
        position
        + STEP_SIZE
        * direction
    )


    # Mencari arah lain jika collision terdeteksi.
    if is_collision(
        next_position
    ):

        next_position = (
            find_safe_direction(
                position,
                direction,
            )
        )


    # Memperbarui posisi robot.
    position = (
        next_position
    )


    # Menyimpan trajectory.
    trajectory.append(
        position.copy()
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


# Membuat visualisasi.
fig, ax = plt.subplots(
    figsize=(
        9,
        7,
    )
)


# Menggambar obstacle.
for center, radius in obstacles:

    obstacle = Circle(
        center,
        radius,
        color="gray",
        alpha=0.8,
    )


    ax.add_patch(
        obstacle
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


# Menampilkan posisi akhir robot.
robot = Circle(
    position,
    ROBOT_RADIUS,
    fill=False,
    linewidth=2,
)


ax.add_patch(
    robot
)


# Mengatur plot.
ax.set_xlabel(
    "X Position (m)"
)

ax.set_ylabel(
    "Y Position (m)"
)

ax.set_title(
    "Robot Navigation with Obstacle Avoidance"
)

ax.set_xlim(
    0,
    20,
)

ax.set_ylim(
    0,
    15,
)

ax.set_aspect(
    "equal"
)

ax.grid(
    alpha=0.3
)

ax.legend()

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
