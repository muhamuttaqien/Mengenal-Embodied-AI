# Import NumPy untuk operasi numerik.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import colormap untuk occupancy grid.
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
    / "mapping_result.png"
)


# Menentukan ukuran map.
MAP_WIDTH = 30
MAP_HEIGHT = 25


# Menentukan nilai occupancy.
UNKNOWN = -1
FREE = 0
OCCUPIED = 1


# Membuat ground truth environment.
world = np.zeros(
    (
        MAP_HEIGHT,
        MAP_WIDTH,
    ),
    dtype=int,
)


# Membuat dinding luar.
world[0, :] = OCCUPIED
world[-1, :] = OCCUPIED
world[:, 0] = OCCUPIED
world[:, -1] = OCCUPIED


# Menambahkan obstacle.
world[
    8:12,
    9:12,
] = OCCUPIED

world[
    6:9,
    17:21,
] = OCCUPIED

world[
    15:18,
    14:18,
] = OCCUPIED

world[
    11:15,
    22:24,
] = OCCUPIED


# Membuat occupancy map robot.
occupancy_map = np.full(
    (
        MAP_HEIGHT,
        MAP_WIDTH,
    ),
    UNKNOWN,
    dtype=int,
)


# Menentukan trajectory robot.
trajectory = [
    (3, 3),
    (5, 3),
    (7, 3),
    (9, 3),
    (11, 3),
    (13, 3),
    (15, 3),
    (17, 3),
    (19, 3),
    (21, 3),
    (23, 3),
    (25, 3),

    (25, 5),
    (25, 7),
    (25, 9),
    (25, 11),
    (25, 13),
    (25, 15),
    (25, 17),
    (25, 19),
    (25, 21),

    (23, 21),
    (21, 21),
    (19, 21),
    (17, 21),
    (15, 21),
    (13, 21),
    (11, 21),
    (9, 21),
    (7, 21),
    (5, 21),
]


# Menentukan parameter LiDAR.
NUM_RAYS = 72
MAX_RANGE = 10.0
RAY_STEP = 0.2


def simulate_lidar(
    robot_x,
    robot_y,
):
    # Menyimpan hasil pengamatan sensor.
    observations = []


    # Membuat arah sinar LiDAR.
    angles = np.linspace(
        0,
        2 * np.pi,
        NUM_RAYS,
        endpoint=False,
    )


    # Menjalankan setiap sinar LiDAR.
    for angle in angles:

        ray_cells = []

        hit_obstacle = False

        hit_cell = None

        distance = 0.0


        # Menjalankan ray casting.
        while distance <= MAX_RANGE:

            x = (
                robot_x
                + distance
                * np.cos(angle)
            )

            y = (
                robot_y
                + distance
                * np.sin(angle)
            )


            # Mengubah koordinat ke grid.
            grid_x = int(
                round(x)
            )

            grid_y = int(
                round(y)
            )


            # Menghentikan ray jika keluar map.
            if (
                grid_x < 0
                or grid_x >= MAP_WIDTH
                or grid_y < 0
                or grid_y >= MAP_HEIGHT
            ):

                break


            cell = (
                grid_x,
                grid_y,
            )


            # Menghindari cell duplikat.
            if (
                not ray_cells
                or ray_cells[-1] != cell
            ):

                ray_cells.append(
                    cell
                )


            # Memeriksa obstacle.
            if (
                world[
                    grid_y,
                    grid_x,
                ]
                == OCCUPIED
            ):

                hit_obstacle = True

                hit_cell = cell

                break


            # Menambah jarak ray.
            distance += RAY_STEP


        # Menyimpan hasil ray.
        observations.append(
            (
                ray_cells,
                hit_obstacle,
                hit_cell,
            )
        )


    # Mengembalikan hasil pengamatan.
    return observations


def update_map(
    occupancy_map,
    observations,
):

    # Membaca setiap hasil LiDAR.
    for (
        ray_cells,
        hit_obstacle,
        hit_cell,
    ) in observations:

        # Menandai free space.
        for x, y in ray_cells:

            if (
                hit_obstacle
                and (
                    x,
                    y,
                )
                == hit_cell
            ):

                break


            occupancy_map[
                y,
                x,
            ] = FREE


        # Menandai obstacle.
        if (
            hit_obstacle
            and hit_cell is not None
        ):

            x, y = hit_cell

            occupancy_map[
                y,
                x,
            ] = OCCUPIED


# Menjalankan proses mapping.
for step, (
    robot_x,
    robot_y,
) in enumerate(
    trajectory
):

    # Menampilkan posisi robot.
    print(
        f"Step {step + 1:02d} | "
        f"Robot position: "
        f"({robot_x}, {robot_y})"
    )


    # Menandai posisi robot sebagai free space.
    occupancy_map[
        robot_y,
        robot_x,
    ] = FREE


    # Mengambil pengamatan LiDAR.
    observations = simulate_lidar(
        robot_x,
        robot_y,
    )


    # Memperbarui occupancy map.
    update_map(
        occupancy_map,
        observations,
    )


# Mengubah trajectory menjadi NumPy array.
trajectory_array = np.array(
    trajectory
)


# Membuat colormap occupancy.
cmap = ListedColormap(
    [
        "gray",
        "white",
        "black",
    ]
)


# Membuat visualisasi.
plt.figure(
    figsize=(
        9,
        7,
    )
)


# Menampilkan occupancy map.
plt.imshow(
    occupancy_map,
    cmap=cmap,
    origin="lower",
    vmin=-1,
    vmax=1,
)


# Menampilkan trajectory robot.
plt.plot(
    trajectory_array[:, 0],
    trajectory_array[:, 1],
    "o-",
    label="Robot Trajectory",
    markersize=3,
)


# Menampilkan posisi awal.
plt.scatter(
    trajectory_array[0, 0],
    trajectory_array[0, 1],
    s=100,
    marker="s",
    label="Start",
)


# Menampilkan posisi akhir.
plt.scatter(
    trajectory_array[-1, 0],
    trajectory_array[-1, 1],
    s=100,
    marker="*",
    label="End",
)


# Mengatur plot.
plt.xlabel(
    "X Position"
)

plt.ylabel(
    "Y Position"
)

plt.title(
    "Occupancy Grid Mapping"
)

plt.xlim(
    -0.5,
    MAP_WIDTH - 0.5,
)

plt.ylim(
    -0.5,
    MAP_HEIGHT - 0.5,
)

plt.grid(
    linewidth=0.3,
    alpha=0.4,
)

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
