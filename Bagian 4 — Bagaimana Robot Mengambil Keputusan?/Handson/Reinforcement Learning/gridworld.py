# Import NumPy untuk operasi numerik.
import numpy as np


class GridWorld:
    """Environment GridWorld 2D sederhana untuk Q-Learning."""

    # Menentukan empat action yang dapat dipilih agent.
    ACTIONS = {
        0: (-1, 0),
        1: (0, 1),
        2: (1, 0),
        3: (0, -1),
    }

    # Menentukan nama setiap action.
    ACTION_NAMES = [
        "UP",
        "RIGHT",
        "DOWN",
        "LEFT",
    ]

    def __init__(self):
        # Menentukan ukuran grid.
        self.height = 6
        self.width = 6

        # Menentukan posisi start dan goal.
        self.start = (5, 0)
        self.goal = (0, 5)

        # Menentukan obstacle pada grid.
        self.obstacles = {
            (1, 1),
            (1, 2),
            (2, 2),
            (3, 2),
            (3, 3),
            (4, 4),
        }

        # Menentukan jumlah langkah maksimum per episode.
        self.max_steps = 80

        # Menyiapkan state environment.
        self.position = None
        self.steps = 0

        # Mengembalikan agent ke posisi awal.
        self.reset()

    def reset(self):
        # Mengembalikan posisi agent ke start.
        self.position = self.start
        self.steps = 0

        return self.position

    def step(self, action):
        # Menambah penghitung langkah.
        self.steps += 1

        # Membaca perubahan posisi dari action.
        dr, dc = self.ACTIONS[action]

        # Menghitung kandidat posisi berikutnya.
        candidate = (
            self.position[0] + dr,
            self.position[1] + dc,
        )

        # Memberikan biaya kecil untuk setiap langkah.
        reward = -0.02
        done = False

        # Memberikan penalti jika agent menabrak dinding.
        if not self._inside(candidate):
            candidate = self.position
            reward = -0.15

        # Memberikan penalti jika agent menabrak obstacle.
        elif candidate in self.obstacles:
            candidate = self.position
            reward = -0.25

        # Memperbarui posisi agent.
        self.position = candidate

        # Memberikan reward besar jika goal tercapai.
        if self.position == self.goal:
            reward = 1.0
            done = True

        # Mengakhiri episode jika langkah maksimum tercapai.
        if self.steps >= self.max_steps:
            done = True

        return (
            self.position,
            reward,
            done,
        )

    def _inside(self, position):
        # Membaca posisi row dan column.
        row, col = position

        # Memeriksa apakah posisi masih berada di dalam grid.
        return (
            0 <= row < self.height
            and 0 <= col < self.width
        )
