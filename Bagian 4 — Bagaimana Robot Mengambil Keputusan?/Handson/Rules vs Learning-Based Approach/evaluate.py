# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk evaluasi.
import numpy as np

# Import PyTorch untuk inference.
import torch

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import model policy.
from model import RobotPolicy

# Import rule-based controller dan nama action.
from rules import ACTION_NAMES
from rules import rule_based_action


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent

# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"

# Membuat folder results jika belum ada.
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# Menentukan file testing data.
TEST_DATA_PATH = (
    RESULTS_DIR
    / "test_data.npz"
)

# Menentukan file model.
MODEL_PATH = (
    RESULTS_DIR
    / "policy_model.pt"
)

# Menentukan file hasil evaluasi.
COMPARISON_OUTPUT_PATH = (
    RESULTS_DIR
    / "comparison_result.png"
)


# Memastikan testing data tersedia.
if not TEST_DATA_PATH.exists():
    raise FileNotFoundError(
        "Testing data belum tersedia. "
        "Jalankan generate_data.py terlebih dahulu."
    )

# Memastikan model tersedia.
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "Model belum tersedia. "
        "Jalankan train.py terlebih dahulu."
    )

# Membaca testing dataset.
data = np.load(
    TEST_DATA_PATH
)

# Membaca observation dan target action.
test_x = data[
    "observations"
]

test_y = data[
    "actions"
]

# Membuat neural network policy.
model = RobotPolicy()

# Memuat parameter hasil training.
model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location="cpu",
    )
)

# Mengaktifkan evaluation mode.
model.eval()

# Mengubah observation menjadi tensor.
observations = torch.tensor(
    test_x,
    dtype=torch.float32,
)

# Menjalankan inference tanpa gradient.
with torch.no_grad():
    logits = model(
        observations
    )

    predictions = torch.argmax(
        logits,
        dim=1,
    ).numpy()

# Menghitung accuracy.
accuracy = np.mean(
    predictions
    == test_y
)

print(
    f"Learning-Based Accuracy: "
    f"{accuracy * 100:.2f}%"
)

# Menentukan beberapa contoh observation.
examples = np.array(
    [
        [1.2, 1.5, 0.8],
        [1.5, 0.3, 0.4],
        [0.4, 0.2, 1.4],
        [0.8, 0.9, 0.7],
    ],
    dtype=np.float32,
)

print(
    "\nExample Decisions"
)

print(
    "-" * 55
)

# Membandingkan keputusan rule-based dan model.
for example in examples:
    left, front, right = example

    # Mengambil keputusan rule-based.
    rule_action = rule_based_action(
        left,
        front,
        right,
    )

    # Mengubah example menjadi tensor.
    input_tensor = torch.tensor(
        example,
        dtype=torch.float32,
    ).unsqueeze(0)

    # Mengambil keputusan learning-based.
    with torch.no_grad():
        output = model(
            input_tensor
        )

        learned_action = int(
            torch.argmax(
                output,
                dim=1,
            ).item()
        )

    # Menampilkan observation.
    print(
        f"Sensor: "
        f"L={left:.2f}, "
        f"F={front:.2f}, "
        f"R={right:.2f}"
    )

    # Menampilkan keputusan rule-based.
    print(
        "Rule-Based    :",
        ACTION_NAMES[
            rule_action
        ],
    )

    # Menampilkan keputusan learning-based.
    print(
        "Learning-Based:",
        ACTION_NAMES[
            learned_action
        ],
    )

    print()

# Menentukan jumlah class.
num_classes = 3

# Membuat confusion matrix kosong.
confusion_matrix = np.zeros(
    (
        num_classes,
        num_classes,
    ),
    dtype=int,
)

# Mengisi confusion matrix.
for true_action, predicted_action in zip(
    test_y,
    predictions,
):
    confusion_matrix[
        true_action,
        predicted_action,
    ] += 1

# Membuat visualisasi confusion matrix.
fig, ax = plt.subplots(
    figsize=(7, 6)
)

image = ax.imshow(
    confusion_matrix,
    cmap="Greys",
)

# Menentukan label sumbu.
ax.set_xticks(
    range(num_classes)
)

ax.set_yticks(
    range(num_classes)
)

ax.set_xticklabels(
    ACTION_NAMES
)

ax.set_yticklabels(
    ACTION_NAMES
)

ax.set_xlabel(
    "Learning-Based Prediction"
)

ax.set_ylabel(
    "Rule-Based Target"
)

ax.set_title(
    "Rule-Based vs Learning-Based Decisions"
)

# Menampilkan jumlah sample pada setiap cell.
for i in range(num_classes):
    for j in range(num_classes):
        ax.text(
            j,
            i,
            confusion_matrix[
                i,
                j,
            ],
            ha="center",
            va="center",
        )

# Menampilkan colorbar.
plt.colorbar(
    image,
    ax=ax,
)

plt.tight_layout()

# Menyimpan confusion matrix.
plt.savefig(
    COMPARISON_OUTPUT_PATH,
    dpi=200,
)

print(
    "Comparison result saved to:",
    COMPARISON_OUTPUT_PATH,
)

# Menampilkan visualisasi.
plt.show()
