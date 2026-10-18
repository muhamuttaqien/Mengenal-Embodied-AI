# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk membaca dataset.
import numpy as np

# Import PyTorch untuk training neural network.
import torch
import torch.nn as nn

# Import Matplotlib untuk visualisasi loss.
import matplotlib.pyplot as plt

# Import model policy.
from model import RobotPolicy


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent

# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"

# Membuat folder results jika belum ada.
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# Menentukan file input training data.
TRAIN_DATA_PATH = (
    RESULTS_DIR
    / "train_data.npz"
)

# Menentukan file model hasil training.
MODEL_OUTPUT_PATH = (
    RESULTS_DIR
    / "policy_model.pt"
)

# Menentukan file visualisasi loss.
LOSS_OUTPUT_PATH = (
    RESULTS_DIR
    / "training_loss.png"
)


# Menentukan konfigurasi training.
EPOCHS = 100
LEARNING_RATE = 0.001
SEED = 42

# Menentukan random seed PyTorch.
torch.manual_seed(
    SEED
)

# Memastikan training data sudah tersedia.
if not TRAIN_DATA_PATH.exists():
    raise FileNotFoundError(
        "Training data belum tersedia. "
        "Jalankan generate_data.py terlebih dahulu."
    )

# Membaca training dataset.
data = np.load(
    TRAIN_DATA_PATH
)

# Mengubah observation menjadi tensor.
observations = torch.tensor(
    data["observations"],
    dtype=torch.float32,
)

# Mengubah action menjadi tensor.
actions = torch.tensor(
    data["actions"],
    dtype=torch.long,
)

# Membuat neural network policy.
model = RobotPolicy()

# Menentukan loss function.
criterion = nn.CrossEntropyLoss()

# Menentukan optimizer.
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE,
)

# Menyimpan nilai loss setiap epoch.
loss_history = []

# Menjalankan training.
for epoch in range(EPOCHS):
    # Menjalankan forward pass.
    logits = model(
        observations
    )

    # Menghitung loss.
    loss = criterion(
        logits,
        actions,
    )

    # Menghapus gradient sebelumnya.
    optimizer.zero_grad()

    # Menghitung gradient.
    loss.backward()

    # Memperbarui parameter model.
    optimizer.step()

    # Menyimpan loss.
    loss_history.append(
        loss.item()
    )

    # Menampilkan progress training.
    if (
        epoch == 0
        or (epoch + 1) % 10 == 0
    ):
        print(
            f"Epoch {epoch + 1:03d} | "
            f"Loss: {loss.item():.4f}"
        )

# Menyimpan model.
torch.save(
    model.state_dict(),
    MODEL_OUTPUT_PATH,
)

print(
    "\nTraining completed."
)

print(
    "Model saved to:",
    MODEL_OUTPUT_PATH,
)

# Membuat visualisasi training loss.
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
    "Loss"
)

plt.title(
    "Learning-Based Policy Training"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()

# Menyimpan visualisasi training loss.
plt.savefig(
    LOSS_OUTPUT_PATH,
    dpi=200,
)

print(
    "Training loss saved to:",
    LOSS_OUTPUT_PATH,
)

# Menampilkan visualisasi.
plt.show()
