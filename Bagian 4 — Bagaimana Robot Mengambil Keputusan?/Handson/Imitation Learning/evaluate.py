# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk operasi numerik.
import numpy as np

# Import PyTorch.
import torch

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import behavior cloning policy.
from policy import BehaviorCloningPolicy

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

# Menentukan file testing demonstrations.
TEST_DATA_PATH = (
    RESULTS_DIR
    / "test_demonstrations.npz"
)

# Menentukan file model.
MODEL_PATH = (
    RESULTS_DIR
    / "behavior_cloning_policy.pt"
)

# Menentukan file visualisasi evaluation.
EVALUATION_OUTPUT_PATH = (
    RESULTS_DIR
    / "evaluation_result.png"
)


# Menentukan parameter rollout.
DT = 0.15
MAX_STEPS = 100
GOAL_THRESHOLD = 0.20


# Memastikan file model tersedia.
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "Model tidak ditemukan. "
        "Jalankan train.py terlebih dahulu."
    )

# Memastikan testing data tersedia.
if not TEST_DATA_PATH.exists():
    raise FileNotFoundError(
        "Testing demonstrations tidak ditemukan. "
        "Jalankan generate_demonstrations.py terlebih dahulu."
    )


# Membuat model.
model = BehaviorCloningPolicy()

# Membaca model hasil training.
model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location="cpu",
        weights_only=True,
    )
)

# Mengubah model ke evaluation mode.
model.eval()


# Membaca testing demonstrations.
data = np.load(
    TEST_DATA_PATH
)

# Mengubah observations menjadi tensor.
test_observations = torch.tensor(
    data["observations"],
    dtype=torch.float32,
)

# Mengubah expert actions menjadi tensor.
test_actions = torch.tensor(
    data["actions"],
    dtype=torch.float32,
)


# Menghasilkan action tanpa menghitung gradient.
with torch.no_grad():
    predicted_actions = model(
        test_observations
    )


# Menghitung test MSE.
mse = torch.mean(
    (
        predicted_actions
        - test_actions
    ) ** 2
).item()


# Menampilkan test MSE.
print(
    f"Test MSE: "
    f"{mse:.6f}"
)


def learned_action(
    observation,
):
    # Mengubah observation menjadi tensor.
    observation_tensor = torch.tensor(
        observation,
        dtype=torch.float32,
    ).unsqueeze(0)

    # Menghasilkan action dari learned policy.
    with torch.no_grad():
        action = model(
            observation_tensor
        )[0].numpy()

    return action


def rollout(
    start,
    target,
    action_function,
):
    # Menentukan posisi awal robot.
    position = np.array(
        start,
        dtype=np.float32,
    )

    # Menentukan target.
    target = np.array(
        target,
        dtype=np.float32,
    )

    # Menyimpan trajectory robot.
    trajectory = [
        position.copy()
    ]

    # Menjalankan rollout.
    for _ in range(
        MAX_STEPS
    ):
        # Menghitung jarak menuju target.
        distance = np.linalg.norm(
            target
            - position
        )

        # Menghentikan rollout jika target tercapai.
        if distance < GOAL_THRESHOLD:
            break

        # Membentuk observation.
        observation = np.concatenate(
            [
                position,
                target,
            ]
        ).astype(
            np.float32
        )

        # Menghasilkan action.
        action = action_function(
            observation
        )

        # Memperbarui posisi robot.
        position = (
            position
            + action
            * DT
        )

        # Menyimpan trajectory.
        trajectory.append(
            position.copy()
        )

    return np.array(
        trajectory
    )


# Menentukan posisi awal rollout.
start = np.array(
    [
        1.0,
        1.0,
    ]
)

# Menentukan target rollout.
target = np.array(
    [
        8.5,
        7.5,
    ]
)


# Menjalankan expert rollout.
expert_trajectory = rollout(
    start,
    target,
    expert_action,
)

# Menjalankan learned-policy rollout.
learned_trajectory = rollout(
    start,
    target,
    learned_action,
)


# Menghitung final distance expert.
expert_final_distance = np.linalg.norm(
    target
    - expert_trajectory[-1]
)

# Menghitung final distance learned policy.
learned_final_distance = np.linalg.norm(
    target
    - learned_trajectory[-1]
)


# Menampilkan hasil rollout.
print(
    "Expert rollout steps:",
    len(expert_trajectory),
)

print(
    "Learned rollout steps:",
    len(learned_trajectory),
)

print(
    f"Expert final distance: "
    f"{expert_final_distance:.4f}"
)

print(
    f"Learned final distance: "
    f"{learned_final_distance:.4f}"
)


# Membuat visualisasi evaluation.
plt.figure(
    figsize=(
        8,
        7,
    )
)

# Menampilkan expert trajectory.
plt.plot(
    expert_trajectory[:, 0],
    expert_trajectory[:, 1],
    "--",
    linewidth=2,
    label="Expert Demonstration",
)

# Menampilkan learned trajectory.
plt.plot(
    learned_trajectory[:, 0],
    learned_trajectory[:, 1],
    "-",
    linewidth=2,
    label="Learned Policy",
)

# Menampilkan posisi awal.
plt.scatter(
    start[0],
    start[1],
    marker="s",
    s=100,
    label="Start",
)

# Menampilkan target.
plt.scatter(
    target[0],
    target[1],
    marker="*",
    s=180,
    label="Target",
)

# Mengatur plot.
plt.xlabel(
    "X Position"
)

plt.ylabel(
    "Y Position"
)

plt.title(
    "Behavior Cloning: Expert vs Learned Policy"
)

plt.xlim(
    0,
    10,
)

plt.ylim(
    0,
    10,
)

plt.grid(
    alpha=0.3
)

plt.legend()

plt.tight_layout()

# Menyimpan visualisasi evaluation.
plt.savefig(
    EVALUATION_OUTPUT_PATH,
    dpi=200,
)

print(
    "Evaluation result saved to:",
    EVALUATION_OUTPUT_PATH,
)

# Menampilkan visualisasi.
plt.show()
