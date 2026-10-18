# Import heapq untuk priority queue.
import heapq

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
    / "dynamic_replanning_result.png"
)

# Menentukan file hasil animasi.
GIF_OUTPUT_PATH = (
    RESULTS_DIR
    / "dynamic_replanning.gif"
)


# Menentukan ukuran map.
MAP_WIDTH = 22
MAP_HEIGHT = 16

# Menentukan nilai cell.
FREE = 0
OCCUPIED = 1

# Menentukan posisi awal dan goal.
START = (
    1,
    1,
)

GOAL = (
    20,
    14,
)

# Menentukan kapan obstacle baru muncul.
REPLAN_AFTER_MOVES = 8


# Membuat map kosong.
grid = np.zeros(
    (
        MAP_HEIGHT,
        MAP_WIDTH,
    ),
    dtype=int,
)


# Membuat dinding luar.
grid[0, :] = OCCUPIED
grid[-1, :] = OCCUPIED
grid[:, 0] = OCCUPIED
grid[:, -1] = OCCUPIED


# Membuat obstacle statis.
grid[
    3:12,
    6,
] = OCCUPIED

grid[
    3,
    6:12,
] = OCCUPIED

grid[
    8:14,
    12,
] = OCCUPIED

grid[
    8,
    12:18,
] = OCCUPIED

grid[
    4:9,
    17,
] = OCCUPIED


# Memastikan posisi start bebas.
grid[
    START[1],
    START[0],
] = FREE

# Memastikan posisi goal bebas.
grid[
    GOAL[1],
    GOAL[0],
] = FREE


def heuristic(
    a,
    b,
):
    # Menghitung Manhattan distance.
    return (
        abs(
            a[0] - b[0]
        )
        + abs(
            a[1] - b[1]
        )
    )


def get_neighbors(
    node,
    current_grid,
):
    # Membaca posisi node.
    x, y = node

    # Menentukan gerakan yang mungkin.
    moves = [
        (
            1,
            0,
        ),
        (
            -1,
            0,
        ),
        (
            0,
            1,
        ),
        (
            0,
            -1,
        ),
    ]

    # Menyimpan neighbor yang valid.
    neighbors = []

    # Memeriksa setiap gerakan.
    for dx, dy in moves:

        # Menghitung posisi neighbor.
        nx = (
            x + dx
        )

        ny = (
            y + dy
        )

        # Memeriksa batas map.
        if (
            nx < 0
            or nx >= MAP_WIDTH
            or ny < 0
            or ny >= MAP_HEIGHT
        ):
            continue

        # Memeriksa obstacle.
        if (
            current_grid[
                ny,
                nx,
            ]
            == OCCUPIED
        ):
            continue

        # Menyimpan neighbor.
        neighbors.append(
            (
                nx,
                ny,
            )
        )

    return neighbors


def reconstruct_path(
    came_from,
    current,
):
    # Menyimpan goal sebagai titik awal rekonstruksi.
    path = [
        current
    ]

    # Menelusuri kembali parent setiap node.
    while current in came_from:

        current = (
            came_from[
                current
            ]
        )

        path.append(
            current
        )

    # Membalik path menjadi start ke goal.
    path.reverse()

    return path


def a_star(
    start,
    goal,
    current_grid,
):
    # Membuat priority queue.
    open_set = []

    # Memasukkan start ke queue.
    heapq.heappush(
        open_set,
        (
            0,
            start,
        ),
    )

    # Menyimpan asal setiap node.
    came_from = {}

    # Menyimpan cost dari start.
    g_score = {
        start: 0
    }

    # Menyimpan node yang sudah dieksplorasi.
    visited = []

    # Menyimpan node yang sudah selesai diproses.
    closed = set()

    # Menjalankan A* selama queue belum kosong.
    while open_set:

        # Mengambil node dengan prioritas terbaik.
        _, current = heapq.heappop(
            open_set
        )

        # Mengabaikan node yang sudah diproses.
        if current in closed:
            continue

        # Menandai node sebagai selesai diproses.
        closed.add(
            current
        )

        # Menyimpan node yang dieksplorasi.
        visited.append(
            current
        )

        # Memeriksa apakah goal tercapai.
        if current == goal:

            # Membentuk final path.
            return (
                reconstruct_path(
                    came_from,
                    current,
                ),
                visited,
            )

        # Memeriksa setiap neighbor.
        for neighbor in get_neighbors(
            current,
            current_grid,
        ):

            # Menghitung cost menuju neighbor.
            tentative_g = (
                g_score[
                    current
                ]
                + 1
            )

            # Memperbarui jika path lebih baik.
            if (
                neighbor not in g_score
                or tentative_g
                < g_score[
                    neighbor
                ]
            ):

                # Menyimpan asal node.
                came_from[
                    neighbor
                ] = current

                # Memperbarui g score.
                g_score[
                    neighbor
                ] = tentative_g

                # Menghitung f score.
                f_score = (
                    tentative_g
                    + heuristic(
                        neighbor,
                        goal,
                    )
                )

                # Memasukkan neighbor ke queue.
                heapq.heappush(
                    open_set,
                    (
                        f_score,
                        neighbor,
                    ),
                )

    # Mengembalikan None jika path tidak ditemukan.
    return (
        None,
        visited,
    )


# Membuat initial plan.
initial_path, initial_visited = a_star(
    START,
    GOAL,
    grid,
)


# Memastikan initial path ditemukan.
if initial_path is None:

    raise RuntimeError(
        "Initial path could not be found."
    )


# Menampilkan hasil initial planning.
print(
    "Initial plan found."
)

print(
    "Initial path length:",
    len(
        initial_path
    ),
)


# Menyimpan trajectory robot.
robot_history = [
    START
]


# Menentukan posisi awal robot.
current_position = (
    START
)


# Menentukan jumlah gerakan sebelum replanning.
moves_before_replan = min(
    REPLAN_AFTER_MOVES,
    len(
        initial_path
    )
    - 3,
)


# Menjalankan sebagian initial path.
for i in range(
    1,
    moves_before_replan + 1,
):

    # Memperbarui posisi robot.
    current_position = (
        initial_path[
            i
        ]
    )

    # Menyimpan trajectory robot.
    robot_history.append(
        current_position
    )


# Menampilkan posisi robot sebelum replanning.
print(
    "Robot reached:",
    current_position,
)


# Memilih node pada original path untuk obstacle baru.
future_index = min(
    moves_before_replan + 4,
    len(
        initial_path
    )
    - 2,
)

new_obstacle = (
    initial_path[
        future_index
    ]
)


# Membuat map baru.
grid_after_change = (
    grid.copy()
)


# Menambahkan obstacle baru.
grid_after_change[
    new_obstacle[1],
    new_obstacle[0],
] = OCCUPIED


# Menampilkan posisi obstacle baru.
print(
    "New obstacle detected at:",
    new_obstacle,
)


# Membuat plan baru dari posisi robot saat ini.
new_path, replan_visited = a_star(
    current_position,
    GOAL,
    grid_after_change,
)


# Memastikan alternative path ditemukan.
if new_path is None:

    raise RuntimeError(
        "No alternative path found after "
        "the new obstacle appeared."
    )


# Menampilkan hasil replanning.
print(
    "Replanning successful."
)

print(
    "New path length:",
    len(
        new_path
    ),
)


# Menjalankan replanned path.
for position in new_path[
    1:
]:

    # Menyimpan trajectory robot.
    robot_history.append(
        position
    )


# Mengubah data menjadi NumPy array.
robot_history = np.array(
    robot_history
)

initial_path_array = np.array(
    initial_path
)

new_path_array = np.array(
    new_path
)

initial_visited_array = np.array(
    initial_visited
)

replan_visited_array = np.array(
    replan_visited
)


# Membuat visualisasi statis.
fig, ax = plt.subplots(
    figsize=(
        10,
        7,
    )
)


# Menampilkan map setelah perubahan.
ax.imshow(
    grid_after_change,
    origin="lower",
)


# Menampilkan node initial planning.
if len(
    initial_visited_array
) > 0:

    ax.scatter(
        initial_visited_array[:, 0],
        initial_visited_array[:, 1],
        s=12,
        alpha=0.20,
        label="Initial Explored Nodes",
    )


# Menampilkan node replanning.
if len(
    replan_visited_array
) > 0:

    ax.scatter(
        replan_visited_array[:, 0],
        replan_visited_array[:, 1],
        s=18,
        alpha=0.35,
        marker="x",
        label="Replanning Explored Nodes",
    )


# Menampilkan original plan.
ax.plot(
    initial_path_array[:, 0],
    initial_path_array[:, 1],
    "--",
    linewidth=1.5,
    label="Original Plan",
)


# Menampilkan replanned path.
ax.plot(
    new_path_array[:, 0],
    new_path_array[:, 1],
    "-o",
    linewidth=2,
    markersize=3,
    label="Replanned Path",
)


# Menampilkan trajectory robot.
ax.plot(
    robot_history[:, 0],
    robot_history[:, 1],
    linewidth=2.5,
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


# Menampilkan obstacle baru.
ax.scatter(
    new_obstacle[0],
    new_obstacle[1],
    marker="X",
    s=140,
    label="New Obstacle",
)


# Mengatur plot.
ax.set_xlabel(
    "X Position"
)

ax.set_ylabel(
    "Y Position"
)

ax.set_title(
    "Dynamic Replanning with A*"
)

ax.set_xticks(
    np.arange(
        0,
        MAP_WIDTH,
        1,
    )
)

ax.set_yticks(
    np.arange(
        0,
        MAP_HEIGHT,
        1,
    )
)

ax.grid(
    linewidth=0.4,
    alpha=0.4,
)

ax.legend(
    loc="upper left",
    fontsize=8,
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
        10,
        7,
    )
)


# Menampilkan map awal.
image = ax_anim.imshow(
    grid,
    origin="lower",
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


# Menampilkan original plan sejak awal.
ax_anim.plot(
    initial_path_array[:, 0],
    initial_path_array[:, 1],
    "--",
    linewidth=1.5,
    label="Original Plan",
)


# Membuat marker robot.
robot_marker, = ax_anim.plot(
    [],
    [],
    "o",
    markersize=8,
    label="Robot",
)


# Membuat garis trajectory robot.
robot_line, = ax_anim.plot(
    [],
    [],
    linewidth=2,
    label="Robot Trajectory",
)


# Membuat garis replanned path.
new_path_line, = ax_anim.plot(
    [],
    [],
    "-o",
    linewidth=2,
    markersize=3,
    label="Replanned Path",
)


# Membuat marker obstacle baru.
new_obstacle_marker, = ax_anim.plot(
    [],
    [],
    "X",
    markersize=10,
    label="New Obstacle",
)


# Mengatur plot animasi.
ax_anim.set_xlabel(
    "X Position"
)

ax_anim.set_ylabel(
    "Y Position"
)

ax_anim.set_title(
    "Dynamic Replanning with A*"
)

ax_anim.set_xticks(
    np.arange(
        0,
        MAP_WIDTH,
        1,
    )
)

ax_anim.set_yticks(
    np.arange(
        0,
        MAP_HEIGHT,
        1,
    )
)

ax_anim.grid(
    linewidth=0.4,
    alpha=0.4,
)

ax_anim.legend(
    loc="upper left",
    fontsize=8,
)


# Menentukan frame saat replanning dimulai.
replan_frame = (
    moves_before_replan
)


def update_animation(
    frame,
):
    # Memperbarui trajectory robot.
    robot_line.set_data(
        robot_history[
            :frame + 1,
            0,
        ],
        robot_history[
            :frame + 1,
            1,
        ],
    )

    # Memperbarui posisi robot.
    robot_marker.set_data(
        [
            robot_history[
                frame,
                0,
            ]
        ],
        [
            robot_history[
                frame,
                1,
            ]
        ],
    )

    # Menampilkan perubahan map saat replanning dimulai.
    if frame >= replan_frame:

        # Menampilkan map dengan obstacle baru.
        image.set_data(
            grid_after_change
        )

        # Menampilkan obstacle baru.
        new_obstacle_marker.set_data(
            [
                new_obstacle[
                    0
                ]
            ],
            [
                new_obstacle[
                    1
                ]
            ],
        )

        # Menampilkan replanned path.
        new_path_line.set_data(
            new_path_array[:, 0],
            new_path_array[:, 1],
        )

    else:

        # Menyembunyikan obstacle baru.
        new_obstacle_marker.set_data(
            [],
            [],
        )

        # Menyembunyikan replanned path.
        new_path_line.set_data(
            [],
            [],
        )

    return (
        robot_marker,
        robot_line,
        new_path_line,
        new_obstacle_marker,
    )


# Membuat animasi.
animation = FuncAnimation(
    fig_anim,
    update_animation,
    frames=len(
        robot_history
    ),
    interval=180,
    blit=False,
)


# Menyimpan animasi sebagai GIF.
animation.save(
    GIF_OUTPUT_PATH,
    writer=PillowWriter(
        fps=5
    ),
)


print(
    "Animasi disimpan ke:",
    GIF_OUTPUT_PATH,
)


# Menampilkan hasil.
plt.show()
