# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk operasi numerik.
import numpy as np

# Import expert policy.
from expert_policy import expert_action


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
TRAIN_OUTPUT_PATH = (
    RESULTS_DIR
    / "train_demonstrations.npz"
)

# Menentukan file dataset testing.
TEST_OUTPUT_PATH = (
    RESULTS_DIR
    / "test_demonstrations.npz"
)


# Menentukan jumlah demonstration.
NUM_DEMONSTRATIONS = 6000

# Menentukan rasio training data.
TRAIN_RATIO = 0.8

# Menentukan batas environment.
WORLD_MIN = 0.0
WORLD_MAX = 10.0

# Menentukan random seed.
SEED = 42


# Membuat random generator.
rng = np.random.default_rng(
    SEED
)


# Menyiapkan demonstration data.
observations = []
actions = []


# Membuat demonstration satu per satu.
for _ in range(
    NUM_DEMONSTRATIONS
):
    # Membuat posisi robot secara acak.
    robot_position = rng.uniform(
        WORLD_MIN,
        WORLD_MAX,
        size=2,
    ).astype(
        np.float32
    )

    # Membuat posisi target secara acak.
    target_position = rng.uniform(
        WORLD_MIN,
        WORLD_MAX,
        size=2,
    ).astype(
        np.float32
    )

    # Membentuk observation.
    observation = np.concatenate(
        [
            robot_position,
            target_position,
        ]
    ).astype(
        np.float32
    )

    # Meminta expert menghasilkan action.
    action = expert_action(
        observation
    )

    # Menyimpan observation.
    observations.append(
        observation
    )

    # Menyimpan expert action.
    actions.append(
        action
    )


# Mengubah data menjadi NumPy array.
observations = np.array(
    observations,
    dtype=np.float32,
)

actions = np.array(
    actions,
    dtype=np.float32,
)


# Mengacak urutan data.
indices = rng.permutation(
    NUM_DEMONSTRATIONS
)

observations = observations[
    indices
]

actions = actions[
    indices
]


# Menentukan posisi pembagian dataset.
split_index = int(
    NUM_DEMONSTRATIONS
    * TRAIN_RATIO
)


# Membagi training observations.
train_observations = observations[
    :split_index
]

# Membagi training actions.
train_actions = actions[
    :split_index
]

# Membagi testing observations.
test_observations = observations[
    split_index:
]

# Membagi testing actions.
test_actions = actions[
    split_index:
]


# Menyimpan training demonstrations.
np.savez(
    TRAIN_OUTPUT_PATH,
    observations=train_observations,
    actions=train_actions,
)

# Menyimpan testing demonstrations.
np.savez(
    TEST_OUTPUT_PATH,
    observations=test_observations,
    actions=test_actions,
)


# Menampilkan informasi dataset.
print(
    "Demonstration dataset generated."
)

print(
    "Training demonstrations:",
    len(train_observations),
)

print(
    "Testing demonstrations:",
    len(test_observations),
)

print(
    "Training data saved to:",
    TRAIN_OUTPUT_PATH,
)

print(
    "Testing data saved to:",
    TEST_OUTPUT_PATH,
)
