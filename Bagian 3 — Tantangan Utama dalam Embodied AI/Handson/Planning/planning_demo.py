# Import heapq untuk priority queue.
import heapq

# Import NumPy untuk operasi numerik.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import ListedColormap untuk warna map.
from matplotlib.colors import ListedColormap

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
    / "planning_result.png"
)


# Menentukan ukuran map.
MAP_WIDTH = 20
MAP_HEIGHT = 15


# Menentukan nilai cell.
FREE = 0
OCCUPIED = 1


# Menentukan posisi awal.
START = (
    1,
    1,
)


# Menentukan posisi goal.
GOAL = (
    18,
    13,
)


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


# Membuat obstacle.
grid[
    3:11,
    5,
] = OCCUPIED

grid[
    4,
    5:11,
] = OCCUPIED


grid[
    8:13,
    10,
] = OCCUPIED

grid[
    8,
    10:16,
] = OCCUPIED


grid[
    3:8,
    15,
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
):
    # Membaca posisi node.
    x, y = node


    # Menentukan gerakan yang mungkin.
    possible_moves = [
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
    for dx, dy in possible_moves:

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
            grid[
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


    # Menjalankan A* selama queue belum kosong.
    while open_set:

        # Mengambil node dengan prioritas terbaik.
        _, current = heapq.heappop(
            open_set
        )


        # Menyimpan node yang dieksplorasi.
        visited.append(
            current
        )


        # Memeriksa apakah goal tercapai.
        if current == goal:

            # Membentuk final path.
            path = reconstruct_path(
                came_from,
                current,
            )


            return (
                path,
                visited,
            )


        # Memeriksa setiap neighbor.
        for neighbor in get_neighbors(
            current
        ):

            # Menghitung cost menuju neighbor.
            tentative_g_score = (
                g_score[
                    current
                ]
                + 1
            )


            # Memperbarui jika path lebih baik.
            if (
                neighbor not in g_score
                or tentative_g_score
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
                ] = tentative_g_score


                # Menghitung heuristic.
                h_score = heuristic(
                    neighbor,
                    goal,
                )


                # Menghitung f score.
                f_score = (
                    tentative_g_score
                    + h_score
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


# Menjalankan A* planning.
path, visited = a_star(
    START,
    GOAL,
)


# Menampilkan hasil planning.
if path is None:

    print(
        "No path found."
    )

else:

    print(
        "Path found!"
    )


    print(
        "Path length:",
        len(
            path
        ),
    )


    print(
        "Visited nodes:",
        len(
            visited
        ),
    )


    print(
        "Planned path:"
    )


    # Menampilkan setiap node pada path.
    for node in path:

        print(
            node
        )


# Menentukan warna map.
cmap = ListedColormap(
    [
        "white",
        "black",
    ]
)


# Membuat visualisasi.
fig, ax = plt.subplots(
    figsize=(
        9,
        7,
    )
)


# Menampilkan occupancy grid.
ax.imshow(
    grid,
    cmap=cmap,
    origin="lower",
    vmin=0,
    vmax=1,
)


# Mengubah visited nodes menjadi array.
visited_array = np.array(
    visited
)


# Menampilkan node yang dieksplorasi.
if len(
    visited_array
) > 0:

    ax.scatter(
        visited_array[:, 0],
        visited_array[:, 1],
        s=12,
        alpha=0.25,
        label="Explored Nodes",
    )


# Menampilkan planned path.
if path is not None:

    path_array = np.array(
        path
    )


    ax.plot(
        path_array[:, 0],
        path_array[:, 1],
        "-o",
        linewidth=2,
        markersize=4,
        label="Planned Path",
    )


# Menampilkan posisi awal.
ax.scatter(
    START[0],
    START[1],
    marker="s",
    s=120,
    label="Start",
)


# Menampilkan goal.
ax.scatter(
    GOAL[0],
    GOAL[1],
    marker="*",
    s=200,
    label="Goal",
)


# Mengatur plot.
ax.set_xlabel(
    "X Position"
)

ax.set_ylabel(
    "Y Position"
)

ax.set_title(
    "A* Path Planning"
)


# Menampilkan grid pada sumbu X.
ax.set_xticks(
    np.arange(
        0,
        MAP_WIDTH,
        1,
    )
)


# Menampilkan grid pada sumbu Y.
ax.set_yticks(
    np.arange(
        0,
        MAP_HEIGHT,
        1,
    )
)


# Menampilkan grid.
ax.grid(
    linewidth=0.4,
    alpha=0.4,
)


# Menampilkan legend.
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


# Menampilkan visualisasi.
plt.show()
