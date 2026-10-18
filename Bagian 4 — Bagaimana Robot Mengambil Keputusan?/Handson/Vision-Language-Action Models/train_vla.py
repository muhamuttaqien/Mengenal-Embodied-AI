# Import Path untuk mengelola file hasil.
from pathlib import Path

# Import Matplotlib untuk visualisasi training loss.
import matplotlib.pyplot as plt

# Import NumPy untuk menyimpan history.
import numpy as np

# Import PyTorch untuk training model.
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# Import dataset dan Mini-VLA.
from dataset import SyntheticVLADataset
from vla_model import MiniVLA


# Hyperparameter training.
EPOCHS = 15
BATCH_SIZE = 64
LEARNING_RATE = 0.001
SEED = 42

# Folder utama script.
BASE_DIR = Path(__file__).resolve().parent

# Semua hasil disimpan ke folder results.
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Path input dan output.
TRAIN_DATA_PATH = RESULTS_DIR / "train_vla.npz"
MODEL_PATH = RESULTS_DIR / "mini_vla.pt"
HISTORY_PATH = RESULTS_DIR / "training_history.npz"
LOSS_PLOT_PATH = RESULTS_DIR / "training_loss.png"

# Membuat training reproducible.
torch.manual_seed(SEED)

# Menggunakan GPU jika tersedia.
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


def main():
    # Memastikan dataset sudah dibuat.
    if not TRAIN_DATA_PATH.exists():
        raise FileNotFoundError(
            "Training dataset not found. "
            "Run generate_dataset.py first."
        )

    # Membaca training dataset.
    dataset = SyntheticVLADataset(
        TRAIN_DATA_PATH
    )

    # Membuat DataLoader.
    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    # Membuat Mini-VLA.
    model = MiniVLA().to(
        device
    )

    # Loss untuk target workspace cell.
    cell_loss_fn = nn.CrossEntropyLoss()

    # Loss untuk gripper command.
    gripper_loss_fn = nn.BCEWithLogitsLoss()

    # Optimizer.
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE,
    )

    # Menyimpan loss setiap epoch.
    loss_history = []

    # Training loop.
    for epoch in range(EPOCHS):
        model.train()
        epoch_loss = 0.0

        for batch in loader:
            # Memindahkan input ke device.
            images = batch["image"].to(device)
            tokens = batch["tokens"].to(device)

            # Memindahkan target ke device.
            target_cells = batch["target_cell"].to(device)
            target_gripper = batch["gripper"].to(device)

            # Forward pass.
            (
                cell_logits,
                gripper_logit,
            ) = model(
                images,
                tokens,
            )

            # Menghitung dua komponen loss.
            cell_loss = cell_loss_fn(
                cell_logits,
                target_cells,
            )
            gripper_loss = gripper_loss_fn(
                gripper_logit,
                target_gripper,
            )

            # Menggabungkan loss.
            loss = (
                cell_loss
                + 0.5 * gripper_loss
            )

            # Backpropagation.
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Menjumlahkan loss.
            epoch_loss += (
                loss.item()
                * len(images)
            )

        # Menghitung rata-rata loss per epoch.
        epoch_loss /= len(dataset)

        loss_history.append(
            epoch_loss
        )

        print(
            f"Epoch {epoch + 1:02d} | "
            f"Loss: {epoch_loss:.5f}"
        )

    # Menyimpan model.
    torch.save(
        model.state_dict(),
        MODEL_PATH,
    )

    # Menyimpan history training.
    np.savez(
        HISTORY_PATH,
        loss=np.asarray(
            loss_history,
            dtype=np.float32,
        ),
    )

    # Membuat grafik training loss.
    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        loss_history
    )

    plt.xlabel(
        "Epoch"
    )

    plt.ylabel(
        "Training Loss"
    )

    plt.title(
        "Mini-VLA Training"
    )

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    # Menyimpan grafik.
    plt.savefig(
        LOSS_PLOT_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    print()
    print("Training completed.")
    print("Device:", device)
    print("Model saved to:", MODEL_PATH)
    print("Training history saved to:", HISTORY_PATH)
    print("Training plot saved to:", LOSS_PLOT_PATH)

    # Menampilkan grafik saat script dijalankan.
    plt.show()

    # Menutup figure setelah window ditutup.
    plt.close()


if __name__ == "__main__":
    main()
