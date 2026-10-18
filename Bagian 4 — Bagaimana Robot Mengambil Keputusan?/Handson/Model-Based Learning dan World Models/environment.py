# Import NumPy untuk operasi numerik.
import numpy as np


class PointWorld:
    # Membuat environment 2D sederhana.
    def __init__(self):
        # Menentukan skala pengaruh action.
        self.action_scale = 0.18

        # Menentukan skala drift environment.
        self.drift_scale = 0.025

        # Menentukan posisi awal agent.
        self.start = np.array(
            [
                0.10,
                0.15,
            ],
            dtype=np.float32,
        )

        # Menentukan posisi goal.
        self.goal = np.array(
            [
                0.90,
                0.85,
            ],
            dtype=np.float32,
        )

        # Menentukan threshold keberhasilan.
        self.goal_threshold = 0.06

        # Menentukan jumlah langkah maksimum.
        self.max_steps = 35

        # Menyimpan state dan jumlah langkah.
        self.state = None
        self.steps = 0

        # Mengatur environment ke kondisi awal.
        self.reset()

    def reset(self):
        # Mengembalikan agent ke posisi awal.
        self.state = self.start.copy()
        self.steps = 0

        return self.state.copy()

    def transition(
        self,
        state,
        action,
    ):
        # Mengubah state menjadi NumPy array.
        state = np.asarray(
            state,
            dtype=np.float32,
        )

        # Mengubah action menjadi NumPy array.
        action = np.asarray(
            action,
            dtype=np.float32,
        )

        # Membatasi action pada rentang yang valid.
        action = np.clip(
            action,
            -1.0,
            1.0,
        )

        # Menghitung drift berdasarkan state saat ini.
        drift = self.drift_scale * np.array(
            [
                np.sin(
                    np.pi * state[1]
                ),
                np.cos(
                    np.pi * state[0]
                ),
            ],
            dtype=np.float32,
        )

        # Menghitung next state dari action dan drift.
        next_state = (
            state
            + self.action_scale * action
            + drift
        )

        # Membatasi state agar tetap berada di environment.
        next_state = np.clip(
            next_state,
            0.0,
            1.0,
        )

        return next_state.astype(
            np.float32
        )

    def step(
        self,
        action,
    ):
        # Menambah jumlah langkah.
        self.steps += 1

        # Memperbarui state menggunakan dynamics sebenarnya.
        self.state = self.transition(
            self.state,
            action,
        )

        # Menghitung jarak menuju goal.
        distance = np.linalg.norm(
            self.goal
            - self.state
        )

        # Memberikan reward berdasarkan jarak ke goal.
        reward = -float(
            distance
        )

        # Menentukan apakah episode selesai.
        done = (
            distance < self.goal_threshold
            or self.steps >= self.max_steps
        )

        # Memberikan bonus jika goal tercapai.
        if distance < self.goal_threshold:
            reward += 1.0

        return (
            self.state.copy(),
            reward,
            done,
        )
