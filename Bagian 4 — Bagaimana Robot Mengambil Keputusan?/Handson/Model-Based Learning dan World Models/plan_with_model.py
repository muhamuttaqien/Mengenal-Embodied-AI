# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk operasi numerik.
import numpy as np

# Import PyTorch.
import torch

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import environment dan world model.
from environment import PointWorld
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

# Menentukan file trained model.
MODEL_PATH = (
    RESULTS_DIR
    / "world_model.pt"
)

# Menentukan file hasil planning.
PLANNING_OUTPUT_PATH = (
    RESULTS_DIR
    / "planning_result.png"
)

# Menentukan parameter planner.
HORIZON = 8
NUM_CANDIDATES = 512
SEED = 7


# Membuat random generator.
rng = np.random.default_rng(
    SEED
)

# Membuat environment.
env = PointWorld()

# Membuat dynamics model.
model = DynamicsModel()

# Membaca trained model.
model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location="cpu",
    )
)

# Mengubah model ke evaluation mode.
model.eval()


def choose_action(
    current_state,
    goal,
):
    # Membuat banyak candidate action sequences.
    action_sequences = rng.uniform(
        -1.0,
        1.0,
        size=(
            NUM_CANDIDATES,
            HORIZON,
            2,
        ),
    ).astype(
        np.float32
    )

    # Mengulang current state untuk semua candidate.
    predicted_states = np.repeat(
        current_state[
            None,
            :,
        ],
        NUM_CANDIDATES,
        axis=0,
    )

    # Menyimpan cumulative cost setiap candidate.
    cumulative_cost = np.zeros(
        NUM_CANDIDATES,
        dtype=np.float32,
    )

    # Melakukan imagined rollout tanpa gradient.
    with torch.no_grad():
        # Mengubah state awal menjadi tensor.
        state_tensor = torch.tensor(
            predicted_states,
            dtype=torch.float32,
        )

        # Mengubah goal menjadi tensor.
        goal_tensor = torch.tensor(
            goal,
            dtype=torch.float32,
        )

        # Melakukan rollout selama horizon.
        for t in range(
            HORIZON
        ):
            # Mengambil action pada timestep saat ini.
            action_tensor = torch.tensor(
                action_sequences[
                    :,
                    t,
                    :,
                ],
                dtype=torch.float32,
            )

            # Memprediksi next state dengan world model.
            state_tensor = (
                model.predict_next_state(
                    state_tensor,
                    action_tensor,
                )
            )

            # Membatasi predicted state pada environment.
            state_tensor = torch.clamp(
                state_tensor,
                0.0,
                1.0,
            )

            # Menghitung jarak predicted state ke goal.
            distance = torch.linalg.norm(
                state_tensor
                - goal_tensor,
                dim=1,
            )

            # Menambahkan jarak sebagai cumulative cost.
            cumulative_cost += (
                distance.numpy()
            )

    # Memilih candidate dengan cost terkecil.
    best_index = np.argmin(
        cumulative_cost
    )

    # Menjalankan hanya action pertama dari sequence terbaik.
    return action_sequences[
        best_index,
        0,
    ]


# Mengatur state awal environment.
state = env.reset()

# Menyimpan trajectory yang benar-benar dijalankan.
trajectory = [
    state.copy()
]

# Menyimpan one-step prediction world model.
predicted_one_step = []


# Menjalankan Model Predictive Control.
for _ in range(
    env.max_steps
):
    # Memilih action menggunakan imagined rollout.
    action = choose_action(
        state,
        env.goal,
    )

    # Mengubah state menjadi tensor.
    state_tensor = torch.tensor(
        state,
        dtype=torch.float32,
    ).unsqueeze(
        0
    )

    # Mengubah action menjadi tensor.
    action_tensor = torch.tensor(
        action,
        dtype=torch.float32,
    ).unsqueeze(
        0
    )

    # Memprediksi next state satu langkah.
    with torch.no_grad():
        model_next_state = (
            model.predict_next_state(
                state_tensor,
                action_tensor,
            )[0].numpy()
        )

    # Menyimpan prediction.
    predicted_one_step.append(
        model_next_state
    )

    # Menjalankan action pada environment sebenarnya.
    (
        state,
        reward,
        done,
    ) = env.step(
        action
    )

    # Menyimpan state aktual.
    trajectory.append(
        state.copy()
    )

    # Mengakhiri rollout jika episode selesai.
    if done:
        break


# Mengubah history menjadi NumPy array.
trajectory = np.array(
    trajectory
)

predicted_one_step = np.array(
    predicted_one_step
)


# Menghitung jarak akhir ke goal.
distance_to_goal = np.linalg.norm(
    trajectory[-1]
    - env.goal
)

# Menentukan keberhasilan planning.
success = (
    distance_to_goal
    < env.goal_threshold
)


# Menampilkan hasil planning.
print(
    "Planning success:",
    success,
)

print(
    "Final distance to goal:",
    round(
        float(
            distance_to_goal
        ),
        4,
    ),
)

print(
    "Executed steps:",
    len(
        trajectory
    ) - 1,
)


# Membuat visualisasi trajectory.
plt.figure(
    figsize=(
        7,
        7,
    )
)


# Menampilkan trajectory aktual.
plt.plot(
    trajectory[:, 0],
    trajectory[:, 1],
    marker="o",
    linewidth=2,
    label="Executed Trajectory",
)


# Menampilkan posisi awal.
plt.scatter(
    env.start[0],
    env.start[1],
    marker="s",
    s=100,
    label="Start",
)


# Menampilkan goal.
plt.scatter(
    env.goal[0],
    env.goal[1],
    marker="*",
    s=180,
    label="Goal",
)


# Mengatur plot.
plt.xlim(
    0.0,
    1.0,
)

plt.ylim(
    0.0,
    1.0,
)

plt.xlabel(
    "X Position"
)

plt.ylabel(
    "Y Position"
)

plt.title(
    "Planning with a Learned World Model"
)

plt.grid(
    alpha=0.3
)

plt.legend()

plt.tight_layout()


# Menyimpan hasil planning.
plt.savefig(
    PLANNING_OUTPUT_PATH,
    dpi=200,
)


# Menampilkan hasil planning.
plt.show()


# Menutup figure setelah window ditutup.
plt.close()


print(
    "Planning result saved to:",
    PLANNING_OUTPUT_PATH,
)
