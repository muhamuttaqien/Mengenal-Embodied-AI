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


# Menentukan file hasil depth image.
DEPTH_OUTPUT_PATH = (
    RESULTS_DIR
    / "depth_image.png"
)


# Menentukan file hasil point cloud.
POINT_CLOUD_OUTPUT_PATH = (
    RESULTS_DIR
    / "point_cloud.png"
)


# Menentukan ukuran camera.
WIDTH = 160
HEIGHT = 120


# Menentukan camera intrinsic.
fx = 140.0
fy = 140.0

cx = WIDTH / 2
cy = HEIGHT / 2


def create_depth_image():

    # Membuat background pada jarak 4 meter.
    depth = np.full(
        (
            HEIGHT,
            WIDTH,
        ),
        4.0,
        dtype=np.float32,
    )


    # Membuat tiga object pada jarak berbeda.
    depth[
        35:85,
        20:55,
    ] = 2.0

    depth[
        50:100,
        70:105,
    ] = 2.7

    depth[
        25:70,
        115:145,
    ] = 3.2


    # Mengembalikan depth image.
    return depth


def depth_to_point_cloud(
    depth,
    fx,
    fy,
    cx,
    cy,
    stride=2,
):

    # Menyimpan point cloud.
    points = []


    # Membaca ukuran depth image.
    height, width = depth.shape


    # Membaca pixel depth.
    for v in range(
        0,
        height,
        stride,
    ):

        for u in range(
            0,
            width,
            stride,
        ):

            # Membaca nilai depth.
            z = depth[
                v,
                u,
            ]


            # Mengabaikan depth tidak valid.
            if z <= 0:

                continue


            # Menghitung koordinat 3D.
            x = (
                (u - cx)
                * z
                / fx
            )

            y = (
                (v - cy)
                * z
                / fy
            )


            # Menyimpan titik 3D.
            points.append(
                [
                    x,
                    y,
                    z,
                ]
            )


    # Mengubah hasil menjadi NumPy array.
    return np.array(
        points
    )


# Membuat depth image.
depth_image = create_depth_image()


# Menampilkan informasi depth image.
print(
    "Depth image shape:",
    depth_image.shape,
)

print(
    "Minimum depth:",
    depth_image.min(),
    "meter",
)

print(
    "Maximum depth:",
    depth_image.max(),
    "meter",
)


# Mengubah depth image menjadi point cloud.
point_cloud = depth_to_point_cloud(
    depth_image,
    fx,
    fy,
    cx,
    cy,
)


# Menampilkan jumlah titik 3D.
print(
    "Number of 3D points:",
    len(point_cloud),
)


# Membuat visualisasi depth image.
plt.figure(
    figsize=(
        8,
        5,
    )
)


# Menampilkan depth image.
plt.imshow(
    depth_image,
    cmap="gray",
)


# Mengatur plot.
plt.title(
    "Depth Image"
)

plt.xlabel(
    "Pixel X"
)

plt.ylabel(
    "Pixel Y"
)

plt.colorbar(
    label="Depth (meter)"
)

plt.tight_layout()


# Menyimpan depth image.
plt.savefig(
    DEPTH_OUTPUT_PATH,
    dpi=200,
)


print(
    "Depth image disimpan ke:",
    DEPTH_OUTPUT_PATH,
)


# Menampilkan depth image.
plt.show()


# Membuat visualisasi point cloud.
fig = plt.figure(
    figsize=(
        9,
        7,
    )
)


# Membuat plot 3D.
ax = fig.add_subplot(
    111,
    projection="3d",
)


# Menampilkan point cloud.
ax.scatter(
    point_cloud[:, 0],
    point_cloud[:, 2],
    -point_cloud[:, 1],
    s=2,
)


# Mengatur plot.
ax.set_xlabel(
    "X (m)"
)

ax.set_ylabel(
    "Z / Depth (m)"
)

ax.set_zlabel(
    "Y (m)"
)

ax.set_title(
    "3D Point Cloud from Depth Image"
)

plt.tight_layout()


# Menyimpan point cloud.
plt.savefig(
    POINT_CLOUD_OUTPUT_PATH,
    dpi=200,
)


print(
    "Point cloud disimpan ke:",
    POINT_CLOUD_OUTPUT_PATH,
)


# Menampilkan point cloud.
plt.show()
