# Import deque untuk Replay Buffer.
from collections import deque

# Import random untuk sampling pengalaman.
import random

# Import NumPy untuk operasi numerik.
import numpy as np

# Import PyTorch untuk neural network.
import torch
import torch.nn as nn


class QNetwork(nn.Module):
    """Neural network untuk memperkirakan Q-value setiap action."""

    def __init__(self, state_dim=2, num_actions=4):
        # Menyiapkan parent class PyTorch.
        super().__init__()

        # Membuat multilayer perceptron sederhana.
        self.network = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, num_actions),
        )

    def forward(self, state):
        # Menghasilkan Q-value untuk setiap action.
        return self.network(state)


class ReplayBuffer:
    """Buffer untuk menyimpan pengalaman agent."""

    def __init__(self, capacity=10000):
        # Membuat buffer dengan kapasitas maksimum.
        self.buffer = deque(
            maxlen=capacity
        )

    def add(
        self,
        state,
        action,
        reward,
        next_state,
        done,
    ):
        # Menyimpan satu transition.
        self.buffer.append(
            (
                state,
                action,
                reward,
                next_state,
                done,
            )
        )

    def sample(self, batch_size):
        # Mengambil mini-batch secara acak.
        batch = random.sample(
            self.buffer,
            batch_size,
        )

        # Memisahkan setiap komponen transition.
        (
            states,
            actions,
            rewards,
            next_states,
            dones,
        ) = zip(*batch)

        # Mengubah hasil menjadi NumPy array.
        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32),
        )

    def __len__(self):
        # Mengembalikan jumlah pengalaman dalam buffer.
        return len(self.buffer)


class DQNAgent:
    """Agent Deep Q-Network sederhana."""

    def __init__(
        self,
        state_dim=2,
        num_actions=4,
        gamma=0.95,
        learning_rate=0.001,
        epsilon=1.0,
        epsilon_min=0.05,
        epsilon_decay=0.995,
        batch_size=64,
        seed=42,
    ):
        # Menyimpan parameter utama DQN.
        self.num_actions = num_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size

        # Menentukan seed agar hasil lebih reproducible.
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

        # Membuat Online Network.
        self.online_network = QNetwork(
            state_dim,
            num_actions,
        )

        # Membuat Target Network.
        self.target_network = QNetwork(
            state_dim,
            num_actions,
        )

        # Menyamakan parameter awal kedua network.
        self.target_network.load_state_dict(
            self.online_network.state_dict()
        )
        self.target_network.eval()

        # Membuat optimizer.
        self.optimizer = torch.optim.Adam(
            self.online_network.parameters(),
            lr=learning_rate,
        )

        # Menggunakan Smooth L1 Loss untuk DQN.
        self.loss_fn = nn.SmoothL1Loss()

        # Membuat Replay Buffer.
        self.replay_buffer = ReplayBuffer()

    def select_action(self, state, training=True):
        # Melakukan exploration berdasarkan epsilon.
        if (
            training
            and np.random.random() < self.epsilon
        ):
            return int(
                np.random.randint(
                    self.num_actions
                )
            )

        # Mengubah state menjadi tensor.
        state_tensor = torch.tensor(
            state,
            dtype=torch.float32,
        ).unsqueeze(0)

        # Menghitung Q-value tanpa gradient.
        with torch.no_grad():
            q_values = self.online_network(
                state_tensor
            )

        # Memilih action dengan Q-value terbesar.
        return int(
            torch.argmax(
                q_values,
                dim=1,
            ).item()
        )

    def remember(
        self,
        state,
        action,
        reward,
        next_state,
        done,
    ):
        # Menyimpan pengalaman ke Replay Buffer.
        self.replay_buffer.add(
            state,
            action,
            reward,
            next_state,
            done,
        )

    def train_step(self):
        # Menunggu sampai buffer memiliki cukup sample.
        if len(self.replay_buffer) < self.batch_size:
            return None

        # Mengambil mini-batch dari Replay Buffer.
        (
            states,
            actions,
            rewards,
            next_states,
            dones,
        ) = self.replay_buffer.sample(
            self.batch_size
        )

        # Mengubah batch menjadi tensor.
        states = torch.tensor(
            states,
            dtype=torch.float32,
        )
        actions = torch.tensor(
            actions,
            dtype=torch.long,
        ).unsqueeze(1)
        rewards = torch.tensor(
            rewards,
            dtype=torch.float32,
        )
        next_states = torch.tensor(
            next_states,
            dtype=torch.float32,
        )
        dones = torch.tensor(
            dones,
            dtype=torch.float32,
        )

        # Membaca Q-value action yang dipilih.
        current_q = self.online_network(
            states
        ).gather(
            1,
            actions,
        ).squeeze(1)

        # Menghitung target Q-value dengan Target Network.
        with torch.no_grad():
            next_q = self.target_network(
                next_states
            ).max(
                dim=1
            ).values

            target_q = (
                rewards
                + self.gamma
                * next_q
                * (1.0 - dones)
            )

        # Menghitung loss.
        loss = self.loss_fn(
            current_q,
            target_q,
        )

        # Memperbarui Online Network.
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return float(
            loss.item()
        )

    def update_target_network(self):
        # Menyalin parameter Online Network ke Target Network.
        self.target_network.load_state_dict(
            self.online_network.state_dict()
        )

    def decay_exploration(self):
        # Mengurangi epsilon secara bertahap.
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon
            * self.epsilon_decay,
        )
