# Import Path untuk mengelola file hasil.
from pathlib import Path

# Import Matplotlib untuk visualisasi prediction.
import matplotlib.pyplot as plt

# Import NumPy untuk menghitung accuracy.
import numpy as np

# Import PyTorch untuk inference.
import torch

# Import dataset dan koordinat workspace.
from dataset import (
    SyntheticVLADataset,
    GRID_POINTS,
)

# Import Mini-VLA.
from vla_model import MiniVLA


# Folder utama script.
BASE_DIR = Path(__file__).resolve().parent

# Semua hasil disimpan ke folder results.
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Path input dan output.
TEST_DATA_PATH = RESULTS_DIR / "test_vla.npz"
MODEL_PATH = RESULTS_DIR / "mini_vla.pt"
METRICS_PATH = RESULTS_DIR / "evaluation_metrics.txt"
FIGURE_PATH = RESULTS_DIR / "evaluation_result.png"

# Menggunakan GPU jika tersedia.
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


def predict_sample(model, sample):
    # Menambahkan batch dimension pada image.
    image = sample["image"].unsqueeze(0).to(
        device
    )

    # Menambahkan batch dimension pada token.
    tokens = sample["tokens"].unsqueeze(0).to(
        device
    )

    # Menjalankan inference.
    with torch.no_grad():
        (
            cell_logits,
            gripper_logit,
        ) = model(
            image,
            tokens,
        )

    # Memilih target cell dengan logit tertinggi.
    predicted_cell = int(
        torch.argmax(
            cell_logits,
            dim=1,
        ).item()
    )

    # Mengubah gripper logit menjadi probability.
    predicted_gripper = float(
        torch.sigmoid(
            gripper_logit[0]
        ).item()
    )

    return (
        predicted_cell,
        predicted_gripper,
    )


def main():
    # Memastikan dataset dan model tersedia.
    if not TEST_DATA_PATH.exists():
        raise FileNotFoundError(
            "Test dataset not found. "
            "Run generate_dataset.py first."
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. "
            "Run train_vla.py first."
        )

    # Membaca testing dataset.
    dataset = SyntheticVLADataset(
        TEST_DATA_PATH
    )

    # Membuat Mini-VLA.
    model = MiniVLA().to(
        device
    )

    # Membaca weight hasil training.
    model.load_state_dict(
        torch.load(
            MODEL_PATH,
            map_location=device,
            weights_only=True,
        )
    )

    # Mengaktifkan evaluation mode.
    model.eval()

    # Menyimpan correctness setiap sample.
    cell_correct = []
    gripper_correct = []

    # Mengevaluasi seluruh testing dataset.
    for i in range(len(dataset)):
        sample = dataset[i]

        (
            predicted_cell,
            predicted_gripper,
        ) = predict_sample(
            model,
            sample,
        )

        # Membaca target sebenarnya.
        true_cell = int(
            sample["target_cell"].item()
        )
        true_gripper = bool(
            sample["gripper"].item()
            >= 0.5
        )

        # Mengubah gripper probability menjadi binary action.
        predicted_gripper_binary = (
            predicted_gripper >= 0.5
        )

        # Menyimpan correctness.
        cell_correct.append(
            predicted_cell == true_cell
        )
        gripper_correct.append(
            predicted_gripper_binary
            == true_gripper
        )

    # Menghitung accuracy.
    cell_accuracy = float(
        np.mean(cell_correct)
    )
    gripper_accuracy = float(
        np.mean(gripper_correct)
    )

    # Menampilkan metrics.
    print(
        f"Target-cell accuracy: "
        f"{cell_accuracy * 100:.2f}%"
    )
    print(
        f"Gripper accuracy: "
        f"{gripper_accuracy * 100:.2f}%"
    )

    # Menyimpan metrics ke file.
    METRICS_PATH.write_text(
        (
            "Mini-VLA Evaluation\n"
            f"Target-cell accuracy: "
            f"{cell_accuracy * 100:.2f}%\n"
            f"Gripper accuracy: "
            f"{gripper_accuracy * 100:.2f}%\n"
        ),
        encoding="utf-8",
    )

    # Memilih empat sample untuk visualisasi.
    indices = [
        0,
        1,
        2,
        3,
    ]

    # Membuat figure 2 x 2.
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(8, 8),
    )

    for ax, index in zip(
        axes.ravel(),
        indices,
    ):
        # Membaca sample.
        sample = dataset[index]

        # Menjalankan prediction.
        (
            predicted_cell,
            predicted_gripper,
        ) = predict_sample(
            model,
            sample,
        )

        # Membaca target cell.
        true_cell = int(
            sample["target_cell"].item()
        )

        # Mengubah image tensor kembali ke format H x W x C.
        image_np = (
            sample["image"]
            .permute(1, 2, 0)
            .numpy()
        )

        # Menampilkan image.
        ax.imshow(
            image_np
        )

        image_size = image_np.shape[0]

        # Membaca posisi target dan prediction.
        true_xy = GRID_POINTS[
            true_cell
        ]
        predicted_xy = GRID_POINTS[
            predicted_cell
        ]

        # Menandai target action.
        ax.scatter(
            true_xy[0] * image_size,
            true_xy[1] * image_size,
            marker="*",
            s=140,
            label="Target Action",
        )

        # Menandai predicted action.
        ax.scatter(
            predicted_xy[0] * image_size,
            predicted_xy[1] * image_size,
            marker="x",
            s=90,
            label="Predicted Action",
        )

        # Menampilkan instruction dan gripper probability.
        ax.set_title(
            sample["instruction"]
            + "\n"
            + f"gripper={predicted_gripper:.2f}"
        )

        ax.axis(
            "off"
        )

    # Mengambil legend dari subplot pertama.
    handles, labels = axes[
        0,
        0,
    ].get_legend_handles_labels()

    # Menambahkan legend global.
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=2,
    )

    # Menambahkan judul figure.
    fig.suptitle(
        "Mini-VLA: Target vs Predicted Action"
    )

    fig.tight_layout(
        rect=[
            0,
            0.05,
            1,
            0.96,
        ]
    )

    # Menyimpan visualisasi.
    plt.savefig(
        FIGURE_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    print("Evaluation metrics saved to:", METRICS_PATH)
    print("Evaluation figure saved to:", FIGURE_PATH)

    # Menampilkan visualisasi saat script dijalankan.
    plt.show()

    # Menutup figure setelah window ditutup.
    plt.close()


if __name__ == "__main__":
    main()
