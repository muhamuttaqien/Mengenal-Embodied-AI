# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk membuat dataset.
import numpy as np

# Import rule-based controller.
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

# Menentukan file dataset training.
TRAIN_DATA_PATH = (
    RESULTS_DIR
    / "train_data.npz"
)

# Menentukan file dataset testing.
TEST_DATA_PATH = (
    RESULTS_DIR
    / "test_data.npz"
)


# Menentukan konfigurasi dataset.
NUM_SAMPLES = 6000
TRAIN_RATIO = 0.8
MIN_DISTANCE = 0.10
MAX_DISTANCE = 2.00
SEED = 42

# Membuat random number generator.
rng = np.random.default_rng(
    SEED
)

# Membuat observation sensor secara acak.
observations = rng.uniform(
    MIN_DISTANCE,
    MAX_DISTANCE,
    size=(NUM_SAMPLES, 3),
).astype(np.float32)

# Menyimpan target action.
actions = []

# Memberi label action dengan rule-based controller.
for observation in observations:
    left, front, right = observation

    actions.append(
        rule_based_action(
            left,
            front,
            right,
        )
    )

# Mengubah action menjadi NumPy array.
actions = np.array(
    actions,
    dtype=np.int64,
)

# Mengacak urutan dataset.
indices = rng.permutation(
    NUM_SAMPLES
)

observations = observations[
    indices
]

actions = actions[
    indices
]

# Menentukan titik pembagian dataset.
split_index = int(
    NUM_SAMPLES
    * TRAIN_RATIO
)

# Membagi training data.
train_x = observations[
    :split_index
]

train_y = actions[
    :split_index
]

# Membagi testing data.
test_x = observations[
    split_index:
]

test_y = actions[
    split_index:
]

# Menyimpan training dataset.
np.savez(
    TRAIN_DATA_PATH,
    observations=train_x,
    actions=train_y,
)

# Menyimpan testing dataset.
np.savez(
    TEST_DATA_PATH,
    observations=test_x,
    actions=test_y,
)

# Menampilkan informasi dataset.
print(
    "Dataset generated."
)

print(
    "Training samples:",
    len(train_x),
)

print(
    "Testing samples:",
    len(test_x),
)

print(
    "Training data saved to:",
    TRAIN_DATA_PATH,
)

print(
    "Testing data saved to:",
    TEST_DATA_PATH,
)
