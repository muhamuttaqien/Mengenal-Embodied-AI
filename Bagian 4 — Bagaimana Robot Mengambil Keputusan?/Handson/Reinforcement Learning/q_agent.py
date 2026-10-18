# Import NumPy untuk Q-table dan random sampling.
import numpy as np


class QLearningAgent:
    """Agent tabular Q-Learning sederhana."""

    def __init__(
        self,
        height,
        width,
        num_actions=4,
        learning_rate=0.15,
        gamma=0.95,
        epsilon=1.0,
        epsilon_min=0.05,
        epsilon_decay=0.995,
        seed=42,
    ):
        # Menyimpan jumlah action.
        self.num_actions = num_actions

        # Menentukan hyperparameter Q-Learning.
        self.learning_rate = learning_rate
        self.gamma = gamma

        # Menentukan parameter exploration.
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        # Membuat random generator yang reproducible.
        self.rng = np.random.default_rng(seed)

        # Membuat Q-table dengan nilai awal nol.
        self.q_table = np.zeros(
            (
                height,
                width,
                num_actions,
            ),
            dtype=np.float32,
        )

    def select_action(self, state, training=True):
        # Melakukan exploration berdasarkan epsilon.
        if (
            training
            and self.rng.random() < self.epsilon
        ):
            return int(
                self.rng.integers(
                    self.num_actions
                )
            )

        # Membaca posisi agent.
        row, col = state

        # Memilih action dengan Q-value terbesar.
        return int(
            np.argmax(
                self.q_table[
                    row,
                    col,
                ]
            )
        )

    def update(
        self,
        state,
        action,
        reward,
        next_state,
        done,
    ):
        # Membaca state saat ini dan state berikutnya.
        row, col = state
        next_row, next_col = next_state

        # Membaca Q-value saat ini.
        current_q = self.q_table[
            row,
            col,
            action,
        ]

        # Menghitung target Q-Learning.
        if done:
            target = reward
        else:
            best_next_q = np.max(
                self.q_table[
                    next_row,
                    next_col,
                ]
            )

            target = (
                reward
                + self.gamma
                * best_next_q
            )

        # Memperbarui Q-value.
        self.q_table[
            row,
            col,
            action,
        ] += (
            self.learning_rate
            * (
                target
                - current_q
            )
        )

    def decay_exploration(self):
        # Mengurangi epsilon secara bertahap.
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon
            * self.epsilon_decay,
        )
