# Import Path untuk mengelola folder hasil.
from pathlib import Path

# Import NumPy untuk membuat dataset sintetis.
import numpy as np


# Parameter dataset.
SEED = 42
NUM_TRAIN = 1800
NUM_TEST = 400
IMAGE_SIZE = 64

# Warna target: merah, hijau, dan biru.
COLORS_RGB = np.array(
    [
        [200, 55, 55],
        [70, 150, 75],
        [60, 90, 190],
    ],
    dtype=np.uint8,
)

# Sembilan titik pada workspace 3 x 3.
GRID_POINTS = np.array(
    [
        [0.20, 0.20],
        [0.50, 0.20],
        [0.80, 0.20],
        [0.20, 0.50],
        [0.50, 0.50],
        [0.80, 0.50],
        [0.20, 0.80],
        [0.50, 0.80],
        [0.80, 0.80],
    ],
    dtype=np.float32,
)

# Folder utama script.
BASE_DIR = Path(__file__).resolve().parent

# Semua hasil disimpan ke folder results.
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def render_scene(target_cell, color_id, distractor_cells):
    # Membuat background workspace.
    image = np.full(
        (IMAGE_SIZE, IMAGE_SIZE, 3),
        245,
        dtype=np.uint8,
    )

    # Membuat batas workspace.
    image[1:3, 1:-2] = 70
    image[-3:-1, 1:-2] = 70
    image[1:-2, 1:3] = 70
    image[1:-2, -3:-1] = 70

    half = 5

    # Menggambar objek pengganggu berwarna abu-abu.
    for cell_id in distractor_cells:
        x_norm, y_norm = GRID_POINTS[cell_id]
        x = int(x_norm * IMAGE_SIZE)
        y = int(y_norm * IMAGE_SIZE)

        image[
            y - half:y + half + 1,
            x - half:x + half + 1,
        ] = [165, 165, 165]

    # Menggambar target berwarna.
    x_norm, y_norm = GRID_POINTS[target_cell]
    x = int(x_norm * IMAGE_SIZE)
    y = int(y_norm * IMAGE_SIZE)

    image[
        y - half:y + half + 1,
        x - half:x + half + 1,
    ] = COLORS_RGB[color_id]

    # Menggambar marker robot/end-effector.
    rx = IMAGE_SIZE // 2
    ry = IMAGE_SIZE - 7

    image[
        ry - 2:ry + 3,
        rx - 2:rx + 3,
    ] = 25

    return image


def create_split(num_samples, seed):
    # Membuat random generator yang reproducible.
    rng = np.random.default_rng(seed)

    # Menyiapkan array dataset.
    images = np.zeros(
        (num_samples, IMAGE_SIZE, IMAGE_SIZE, 3),
        dtype=np.uint8,
    )
    color_ids = np.zeros(num_samples, dtype=np.int64)
    verb_ids = np.zeros(num_samples, dtype=np.int64)
    target_cells = np.zeros(num_samples, dtype=np.int64)
    gripper = np.zeros(num_samples, dtype=np.float32)

    # Membuat setiap demonstration sample.
    for i in range(num_samples):
        # Memilih satu target dan dua distractor.
        cells = rng.choice(
            9,
            size=3,
            replace=False,
        )

        target_cell = int(cells[0])
        distractors = cells[1:]

        # Memilih warna target dan jenis instruction.
        color_id = int(rng.integers(0, 3))
        verb_id = int(rng.integers(0, 2))

        # Menyimpan observation dan action target.
        images[i] = render_scene(
            target_cell,
            color_id,
            distractors,
        )
        color_ids[i] = color_id
        verb_ids[i] = verb_id
        target_cells[i] = target_cell

        # pick -> gripper close, move -> gripper open.
        gripper[i] = 1.0 if verb_id == 1 else 0.0

    return {
        "images": images,
        "color_ids": color_ids,
        "verb_ids": verb_ids,
        "target_cells": target_cells,
        "gripper": gripper,
    }


def main():
    # Membuat training dan testing split.
    train_data = create_split(
        NUM_TRAIN,
        SEED,
    )
    test_data = create_split(
        NUM_TEST,
        SEED + 1,
    )

    # Menentukan path hasil dataset.
    train_path = RESULTS_DIR / "train_vla.npz"
    test_path = RESULTS_DIR / "test_vla.npz"

    # Menyimpan dataset terkompresi.
    np.savez_compressed(
        train_path,
        **train_data,
    )
    np.savez_compressed(
        test_path,
        **test_data,
    )

    print("Synthetic VLA dataset created.")
    print("Training samples:", NUM_TRAIN)
    print("Testing samples:", NUM_TEST)
    print("Training dataset saved to:", train_path)
    print("Testing dataset saved to:", test_path)


if __name__ == "__main__":
    main()
