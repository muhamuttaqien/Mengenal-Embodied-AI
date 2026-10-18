# Import Path untuk mengatur folder hasil.
from pathlib import Path

# Import NumPy untuk menyimpan dan menganalisis data training.
import numpy as np

# Import PyTorch untuk menyimpan model.
import torch

# Import Matplotlib untuk membuat grafik training.
import matplotlib.pyplot as plt

# Import environment dan DQN agent.
from gridworld import GridWorld
from dqn_agent import DQNAgent


# Menentukan folder script dan folder hasil.
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Menentukan parameter training.
EPISODES = 1200
TARGET_UPDATE_INTERVAL = 25
SEED = 42

# Membuat environment.
env = GridWorld()

# Membuat DQN agent.
agent = DQNAgent(
    state_dim=2,
    num_actions=4,
    gamma=0.95,
    learning_rate=0.001,
    epsilon=1.0,
    epsilon_min=0.05,
    epsilon_decay=0.995,
    batch_size=64,
    seed=SEED,
)

# Menyimpan riwayat training.
episode_rewards = []
success_history = []
loss_history = []

# Menjalankan training.
for episode in range(EPISODES):
    # Mengembalikan environment ke kondisi awal.
    state = env.reset()

    total_reward = 0.0
    success = 0

    # Menjalankan satu episode.
    for _ in range(env.max_steps):
        # Memilih action dengan epsilon-greedy policy.
        action = agent.select_action(
            state,
            training=True,
        )

        # Menjalankan action pada environment.
        next_state, reward, done = env.step(
            action
        )

        # Menyimpan transition ke Replay Buffer.
        agent.remember(
            state,
            action,
            reward,
            next_state,
            done,
        )

        # Melatih Online Network dari mini-batch.
        loss = agent.train_step()

        if loss is not None:
            loss_history.append(loss)

        # Memperbarui state dan reward.
        state = next_state
        total_reward += reward

        # Mengakhiri episode jika selesai.
        if done:
            if env.position == env.goal:
                success = 1
            break

    # Mengurangi exploration setelah setiap episode.
    agent.decay_exploration()

    # Memperbarui Target Network secara berkala.
    if (
        episode + 1
    ) % TARGET_UPDATE_INTERVAL == 0:
        agent.update_target_network()

    # Menyimpan statistik episode.
    episode_rewards.append(total_reward)
    success_history.append(success)

    # Menampilkan progress training secara berkala.
    if (
        episode == 0
        or (episode + 1) % 100 == 0
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

# Menyimpan trained policy.
MODEL_PATH = RESULTS_DIR / "dqn_policy.pt"
torch.save(
    agent.online_network.state_dict(),
    MODEL_PATH,
)

# Menyimpan riwayat training.
HISTORY_PATH = RESULTS_DIR / "training_history.npz"
np.savez(
    HISTORY_PATH,
    rewards=np.array(episode_rewards),
    success=np.array(success_history),
    losses=np.array(loss_history),
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
plt.title("DQN Training")
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
print("Saved:", MODEL_PATH)
print("Saved:", HISTORY_PATH)
print("Saved:", REWARD_PLOT_PATH)
