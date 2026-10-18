# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk membaca dataset.
import numpy as np

# Import PyTorch.
import torch
import torch.nn as nn

# Import DataLoader dan TensorDataset.
from torch.utils.data import (
    DataLoader,
    TensorDataset,
)

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import dynamics model.
from world_model import DynamicsModel


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent

# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"

# Membuat folder results jika belum ada.
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# Menentukan file input dan output.
TRAIN_DATA_PATH = (
    RESULTS_DIR
    / "train_transitions.npz"
)

MODEL_PATH = (
    RESULTS_DIR
    / "world_model.pt"
)

LOSS_OUTPUT_PATH = (
    RESULTS_DIR
    / "training_loss.png"
)

# Menentukan parameter training.
EPOCHS = 120
BATCH_SIZE = 256
LEARNING_RATE = 0.001
SEED = 42


# Menentukan random seed PyTorch.
torch.manual_seed(
    SEED
)


# Membaca training data.
train_data = np.load(
    TRAIN_DATA_PATH
)


# Mengubah state menjadi tensor.
states = torch.tensor(
    train_data["states"],
    dtype=torch.float32,
)

# Mengubah action menjadi tensor.
actions = torch.tensor(
    train_data["actions"],
    dtype=torch.float32,
)

# Mengubah next state menjadi tensor.
next_states = torch.tensor(
    train_data["next_states"],
    dtype=torch.float32,
)


# Menghitung target perubahan state.
target_delta = (
    next_states
    - states
)


# Membuat dataset training.
dataset = TensorDataset(
    states,
    actions,
    target_delta,
)


# Membuat DataLoader.
loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
)


# Membuat dynamics model.
model = DynamicsModel()

# Menggunakan MSE sebagai loss.
criterion = nn.MSELoss()

# Membuat optimizer Adam.
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE,
)


# Menyimpan training loss.
loss_history = []


# Menjalankan training.
for epoch in range(
    EPOCHS
):
    # Menyimpan total loss setiap epoch.
    epoch_loss = 0.0

    # Membaca setiap batch.
    for (
        state_batch,
        action_batch,
        delta_batch,
    ) in loader:
        # Memprediksi perubahan state.
        predicted_delta = model(
            state_batch,
            action_batch,
        )

        # Menghitung loss.
        loss = criterion(
            predicted_delta,
            delta_batch,
        )

        # Menghapus gradient sebelumnya.
        optimizer.zero_grad()

        # Menghitung gradient.
        loss.backward()

        # Memperbarui parameter model.
        optimizer.step()

        # Menambahkan loss batch.
        epoch_loss += (
            loss.item()
            * len(
                state_batch
            )
        )

    # Menghitung rata-rata loss.
    epoch_loss /= len(
        dataset
    )

    # Menyimpan loss.
    loss_history.append(
        epoch_loss
    )

    # Menampilkan progres training.
    if (
        epoch == 0
        or (epoch + 1) % 20 == 0
    ):
        print(
            f"Epoch "
            f"{epoch + 1:03d} | "
            f"Loss: "
            f"{epoch_loss:.8f}"
        )


# Menyimpan trained model.
torch.save(
    model.state_dict(),
    MODEL_PATH,
)


# Membuat grafik training loss.
plt.figure(
    figsize=(
        8,
        5,
    )
)

plt.plot(
    loss_history
)

plt.xlabel(
    "Epoch"
)

plt.ylabel(
    "MSE Loss"
)

plt.title(
    "Dynamics Model Training"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()


# Menyimpan grafik training loss.
plt.savefig(
    LOSS_OUTPUT_PATH,
    dpi=200,
)


# Menampilkan grafik training loss.
plt.show()


# Menutup figure setelah window ditutup.
plt.close()


# Menampilkan informasi hasil training.
print(
    "\nWorld model training completed."
)

print(
    "Model saved to:",
    MODEL_PATH,
)

print(
    "Training loss saved to:",
    LOSS_OUTPUT_PATH,
)
