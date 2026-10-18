# Import Path untuk mengatur folder hasil.
from pathlib import Path

# Import NumPy untuk membaca Q-table.
import numpy as np

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import environment.
from gridworld import GridWorld


# Menentukan folder script dan folder hasil.
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Menentukan simbol action untuk visualisasi policy.
ARROWS = {
    0: "↑",
    1: "→",
    2: "↓",
    3: "←",
}

# Membuat environment.
env = GridWorld()

# Memuat Q-table hasil training.
Q_TABLE_PATH = RESULTS_DIR / "q_table.npy"
q_table = np.load(
    Q_TABLE_PATH
)

# Mengembalikan agent ke posisi awal.
state = env.reset()

# Menyimpan trajectory evaluation.
trajectory = [
    state
]

total_reward = 0.0

# Menjalankan greedy rollout tanpa exploration.
for _ in range(env.max_steps):
    # Membaca posisi agent.
    row, col = state

    # Memilih action dengan Q-value terbesar.
    action = int(
        np.argmax(
            q_table[
                row,
                col,
            ]
        )
    )

    # Menjalankan action pada environment.
    next_state, reward, done = env.step(
        action
    )

    # Memperbarui reward dan state.
    total_reward += reward
    state = next_state

    # Menyimpan trajectory.
    trajectory.append(
        state
    )

    # Mengakhiri rollout jika selesai.
    if done:
        break

# Memeriksa apakah goal tercapai.
success = (
    state == env.goal
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

# Membuat visualisasi learned policy.
fig, ax = plt.subplots(
    figsize=(7, 7)
)

# Menggambar setiap cell pada GridWorld.
for row in range(env.height):
    for col in range(env.width):
        cell = (
            row,
            col,
        )

        # Menampilkan obstacle.
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

        # Menampilkan goal.
        elif cell == env.goal:
            ax.text(
                col,
                row,
                "G",
                ha="center",
                va="center",
                fontsize=15,
                fontweight="bold",
            )

        # Menampilkan start.
        elif cell == env.start:
            ax.text(
                col,
                row,
                "S",
                ha="center",
                va="center",
                fontsize=15,
                fontweight="bold",
            )

        # Menampilkan action terbaik pada cell lain.
        else:
            best_action = int(
                np.argmax(
                    q_table[
                        row,
                        col,
                    ]
                )
            )

            ax.text(
                col,
                row,
                ARROWS[best_action],
                ha="center",
                va="center",
                fontsize=15,
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

# Menampilkan greedy rollout.
ax.plot(
    trajectory_array[:, 0],
    trajectory_array[:, 1],
    marker="o",
    linewidth=2,
    label="Greedy Rollout",
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
ax.set_title("Learned Q-Learning Policy")
ax.legend(loc="upper right")
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
