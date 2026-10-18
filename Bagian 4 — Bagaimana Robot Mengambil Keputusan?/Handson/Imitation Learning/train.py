# Import Path untuk mengatur path file.
from pathlib import Path

# Import PyTorch.
import torch

# Import neural network module dari PyTorch.
import torch.nn as nn

# Import DataLoader untuk batching dataset.
from torch.utils.data import DataLoader

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import demonstration dataset.
from dataset import DemonstrationDataset

# Import behavior cloning policy.
from policy import BehaviorCloningPolicy


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent

# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"

# Membuat folder results jika belum ada.
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# Menentukan file training demonstrations.
TRAIN_DATA_PATH = (
    RESULTS_DIR
    / "train_demonstrations.npz"
)

# Menentukan file model.
MODEL_OUTPUT_PATH = (
    RESULTS_DIR
    / "behavior_cloning_policy.pt"
)

# Menentukan file grafik training loss.
LOSS_OUTPUT_PATH = (
    RESULTS_DIR
    / "training_loss.png"
)


# Menentukan parameter training.
EPOCHS = 80
BATCH_SIZE = 128
LEARNING_RATE = 0.001

# Menentukan random seed.
SEED = 42

# Mengatur random seed PyTorch.
torch.manual_seed(
    SEED
)


# Memastikan demonstration data tersedia.
if not TRAIN_DATA_PATH.exists():
    raise FileNotFoundError(
        "Training demonstrations tidak ditemukan. "
        "Jalankan generate_demonstrations.py terlebih dahulu."
    )


# Membaca training dataset.
dataset = DemonstrationDataset(
    TRAIN_DATA_PATH
)

# Membuat DataLoader.
loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
)


# Membuat behavior cloning policy.
model = BehaviorCloningPolicy()

# Menggunakan MSE sebagai loss function.
criterion = nn.MSELoss()

# Membuat optimizer Adam.
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE,
)


# Menyiapkan training loss history.
loss_history = []


# Menjalankan training.
for epoch in range(
    EPOCHS
):
    # Menyimpan total loss dalam satu epoch.
    epoch_loss = 0.0

    # Membaca setiap batch.
    for (
        observations,
        expert_actions,
    ) in loader:
        # Menghasilkan predicted actions.
        predicted_actions = model(
            observations
        )

        # Menghitung loss terhadap expert actions.
        loss = criterion(
            predicted_actions,
            expert_actions,
        )

        # Menghapus gradient sebelumnya.
        optimizer.zero_grad()

        # Menghitung gradient.
        loss.backward()

        # Memperbarui parameter model.
        optimizer.step()

        # Menambahkan batch loss.
        epoch_loss += (
            loss.item()
            * len(
                observations
            )
        )

    # Menghitung rata-rata loss satu epoch.
    epoch_loss /= len(
        dataset
    )

    # Menyimpan loss history.
    loss_history.append(
        epoch_loss
    )

    # Menampilkan loss secara berkala.
    if (
        epoch == 0
        or (epoch + 1) % 10 == 0
    ):
        print(
            f"Epoch "
            f"{epoch + 1:03d} | "
            f"Loss: "
            f"{epoch_loss:.6f}"
        )


# Menyimpan model.
torch.save(
    model.state_dict(),
    MODEL_OUTPUT_PATH,
)


# Menampilkan status training.
print(
    "\nTraining completed."
)

print(
    "Model saved to:",
    MODEL_OUTPUT_PATH,
)


# Membuat grafik training loss.
plt.figure(
    figsize=(
        8,
        5,
    )
)

# Menampilkan loss history.
plt.plot(
    loss_history
)

# Mengatur plot.
plt.xlabel(
    "Epoch"
)

plt.ylabel(
    "MSE Loss"
)

plt.title(
    "Behavior Cloning Training Loss"
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

print(
    "Training loss saved to:",
    LOSS_OUTPUT_PATH,
)

# Menampilkan grafik.
plt.show()
