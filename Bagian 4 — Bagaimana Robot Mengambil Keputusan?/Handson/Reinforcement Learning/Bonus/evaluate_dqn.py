# Import Path untuk mengatur folder hasil.
from pathlib import Path

# Import NumPy untuk trajectory.
import numpy as np

# Import PyTorch untuk inference.
import torch

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import environment dan Q-Network.
from gridworld import GridWorld
from dqn_agent import QNetwork


# Menentukan folder script dan folder hasil.
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Membuat environment.
env = GridWorld()

# Membuat Q-Network.
model = QNetwork(
    state_dim=2,
    num_actions=4,
)

# Memuat trained DQN.
MODEL_PATH = RESULTS_DIR / "dqn_policy.pt"
model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location="cpu",
    )
)
model.eval()

# Mengembalikan environment ke kondisi awal.
state = env.reset()

# Menyimpan trajectory rollout.
trajectory = [
    env.position
]

total_reward = 0.0

# Menjalankan greedy rollout tanpa exploration.
for _ in range(env.max_steps):
    # Mengubah state menjadi tensor.
    state_tensor = torch.tensor(
        state,
        dtype=torch.float32,
    ).unsqueeze(0)

    # Menghitung Q-value tanpa gradient.
    with torch.no_grad():
        q_values = model(
            state_tensor
        )

    # Memilih action dengan Q-value terbesar.
    action = int(
        torch.argmax(
            q_values,
            dim=1,
        ).item()
    )

    # Menjalankan action pada environment.
    state, reward, done = env.step(
        action
    )

    # Memperbarui reward dan trajectory.
    total_reward += reward
    trajectory.append(
        env.position
    )

    # Mengakhiri rollout jika selesai.
    if done:
        break

# Memeriksa apakah goal tercapai.
success = (
    env.position == env.goal
)

# Menampilkan hasil evaluation.
print(
    "Evaluation success:",
    success,
)
print(
    "Total reward:",
    round(total_reward, 3),
)
print(
    "Trajectory length:",
    len(trajectory) - 1,
)

# Membuat visualisasi trajectory.
fig, ax = plt.subplots(
    figsize=(7, 7)
)

# Menggambar obstacle.
for row in range(env.height):
    for col in range(env.width):
        cell = (
            row,
            col,
        )

        if cell in env.obstacles:
            ax.add_patch(
                plt.Rectangle(
                    (
                        col - 0.5,
                        row - 0.5,
                    ),
                    1,
                    1,
                    fill=True,
                    alpha=0.35,
                )
            )

# Mengubah trajectory ke koordinat plot.
trajectory_array = np.array(
    [
        (
            col,
            row,
        )
        for row, col in trajectory
    ]
)

# Menampilkan trajectory DQN.
ax.plot(
    trajectory_array[:, 0],
    trajectory_array[:, 1],
    marker="o",
    linewidth=2,
    label="DQN Rollout",
)

# Menampilkan posisi start.
ax.scatter(
    env.start[1],
    env.start[0],
    marker="s",
    s=100,
    label="Start",
)

# Menampilkan goal.
ax.scatter(
    env.goal[1],
    env.goal[0],
    marker="*",
    s=180,
    label="Goal",
)

# Mengatur plot.
ax.set_xlim(
    -0.5,
    env.width - 0.5,
)
ax.set_ylim(
    env.height - 0.5,
    -0.5,
)
ax.set_xticks(
    range(env.width)
)
ax.set_yticks(
    range(env.height)
)
ax.grid(alpha=0.4)
ax.set_xlabel("Column")
ax.set_ylabel("Row")
ax.set_title("Deep Q-Network Evaluation")
ax.legend()
plt.tight_layout()

# Menyimpan hasil evaluation.
OUTPUT_PATH = RESULTS_DIR / "evaluation_result.png"
plt.savefig(
    OUTPUT_PATH,
    dpi=200,
)
# Menampilkan gambar.
plt.show()

# Menutup figure setelah window ditutup.
plt.close()

print(
    "Saved:",
    OUTPUT_PATH,
)
