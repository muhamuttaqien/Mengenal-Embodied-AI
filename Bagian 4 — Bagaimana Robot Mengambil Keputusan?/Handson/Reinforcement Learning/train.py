# Import Path untuk mengatur folder hasil.
from pathlib import Path

# Import NumPy untuk menyimpan dan menganalisis data training.
import numpy as np

# Import Matplotlib untuk membuat grafik training.
import matplotlib.pyplot as plt

# Import environment dan agent.
from gridworld import GridWorld
from q_agent import QLearningAgent


# Menentukan folder script dan folder hasil.
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Menentukan parameter training.
EPISODES = 2000
SEED = 42

# Membuat environment.
env = GridWorld()

# Membuat Q-Learning agent.
agent = QLearningAgent(
    height=env.height,
    width=env.width,
    learning_rate=0.15,
    gamma=0.95,
    epsilon=1.0,
    epsilon_min=0.05,
    epsilon_decay=0.995,
    seed=SEED,
)

# Menyimpan riwayat training.
episode_rewards = []
episode_lengths = []
success_history = []

# Menjalankan training untuk beberapa episode.
for episode in range(EPISODES):
    # Mengembalikan environment ke kondisi awal.
    state = env.reset()

    total_reward = 0.0
    success = 0

    # Menjalankan satu episode.
    for step in range(env.max_steps):
        # Memilih action dengan epsilon-greedy policy.
        action = agent.select_action(
            state,
            training=True,
        )

        # Menjalankan action pada environment.
        next_state, reward, done = env.step(
            action
        )

        # Memperbarui Q-table.
        agent.update(
            state,
            action,
            reward,
            next_state,
            done,
        )

        # Memperbarui state dan reward.
        state = next_state
        total_reward += reward

        # Mengakhiri episode jika selesai.
        if done:
            if state == env.goal:
                success = 1
            break

    # Mengurangi exploration setelah setiap episode.
    agent.decay_exploration()

    # Menyimpan statistik episode.
    episode_rewards.append(total_reward)
    episode_lengths.append(step + 1)
    success_history.append(success)

    # Menampilkan progress training secara berkala.
    if (
        episode == 0
        or (episode + 1) % 200 == 0
    ):
        recent_success = np.mean(
            success_history[-100:]
        )

        print(
            f"Episode {episode + 1:04d} | "
            f"Reward: {total_reward:.3f} | "
            f"Epsilon: {agent.epsilon:.3f} | "
            f"Recent success: "
            f"{recent_success * 100:.1f}%"
        )

# Menyimpan Q-table.
Q_TABLE_PATH = RESULTS_DIR / "q_table.npy"
np.save(
    Q_TABLE_PATH,
    agent.q_table,
)

# Menyimpan riwayat training.
HISTORY_PATH = RESULTS_DIR / "training_history.npz"
np.savez(
    HISTORY_PATH,
    rewards=np.array(episode_rewards),
    lengths=np.array(episode_lengths),
    success=np.array(success_history),
)

# Menghitung moving average reward.
window = 50
moving_average = np.convolve(
    episode_rewards,
    np.ones(window) / window,
    mode="valid",
)

# Membuat grafik training reward.
plt.figure(
    figsize=(8, 5)
)

plt.plot(
    episode_rewards,
    alpha=0.25,
    label="Episode Reward",
)

plt.plot(
    range(
        window - 1,
        EPISODES,
    ),
    moving_average,
    linewidth=2,
    label="50-Episode Moving Average",
)

plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.title("Q-Learning Training")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

# Menyimpan grafik training.
REWARD_PLOT_PATH = RESULTS_DIR / "training_reward.png"
plt.savefig(
    REWARD_PLOT_PATH,
    dpi=200,
)
# Menampilkan gambar.
plt.show()

# Menutup figure setelah window ditutup.
plt.close()

# Menampilkan lokasi hasil.
print("\nTraining completed.")
print("Saved:", Q_TABLE_PATH)
print("Saved:", HISTORY_PATH)
print("Saved:", REWARD_PLOT_PATH)
