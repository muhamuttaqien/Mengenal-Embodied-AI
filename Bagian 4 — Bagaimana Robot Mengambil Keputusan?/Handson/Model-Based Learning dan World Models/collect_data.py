# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk operasi numerik.
import numpy as np

# Import environment.
from environment import PointWorld


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent

# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"

# Membuat folder results jika belum ada.
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# Menentukan jumlah transition.
NUM_TRANSITIONS = 8000

# Menentukan rasio training data.
TRAIN_RATIO = 0.8

# Menentukan random seed.
SEED = 42


# Membuat environment.
env = PointWorld()

# Membuat random generator.
rng = np.random.default_rng(
    SEED
)


# Membuat state secara acak.
states = rng.uniform(
    0.0,
    1.0,
    size=(
        NUM_TRANSITIONS,
        2,
    ),
).astype(
    np.float32
)


# Membuat action secara acak.
actions = rng.uniform(
    -1.0,
    1.0,
    size=(
        NUM_TRANSITIONS,
        2,
    ),
).astype(
    np.float32
)


# Menghitung next state menggunakan dynamics sebenarnya.
next_states = np.array(
    [
        env.transition(
            state,
            action,
        )
        for state, action in zip(
            states,
            actions,
        )
    ],
    dtype=np.float32,
)


# Mengacak urutan transition.
indices = rng.permutation(
    NUM_TRANSITIONS
)

states = states[
    indices
]

actions = actions[
    indices
]

next_states = next_states[
    indices
]


# Menentukan batas training dan testing data.
split_index = int(
    NUM_TRANSITIONS
    * TRAIN_RATIO
)


# Menentukan file training data.
TRAIN_DATA_PATH = (
    RESULTS_DIR
    / "train_transitions.npz"
)

# Menentukan file testing data.
TEST_DATA_PATH = (
    RESULTS_DIR
    / "test_transitions.npz"
)


# Menyimpan training data.
np.savez(
    TRAIN_DATA_PATH,
    states=states[
        :split_index
    ],
    actions=actions[
        :split_index
    ],
    next_states=next_states[
        :split_index
    ],
)


# Menyimpan testing data.
np.savez(
    TEST_DATA_PATH,
    states=states[
        split_index:
    ],
    actions=actions[
        split_index:
    ],
    next_states=next_states[
        split_index:
    ],
)


# Menampilkan informasi dataset.
print(
    "Transition dataset generated."
)

print(
    "Training transitions:",
    split_index,
)

print(
    "Testing transitions:",
    NUM_TRANSITIONS
    - split_index,
)

print(
    "Training data saved to:",
    TRAIN_DATA_PATH,
)

print(
    "Testing data saved to:",
    TEST_DATA_PATH,
)
