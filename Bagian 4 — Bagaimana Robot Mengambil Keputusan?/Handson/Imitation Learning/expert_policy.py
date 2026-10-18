# Import NumPy untuk operasi numerik.
import numpy as np


def expert_action(
    observation,
    max_speed=1.0,
):
    # Membaca posisi robot dan target dari observation.
    robot_position = observation[:2]
    target_position = observation[2:]

    # Menghitung arah dari robot menuju target.
    direction = (
        target_position
        - robot_position
    )

    # Menghitung jarak menuju target.
    distance = np.linalg.norm(
        direction
    )

    # Menghasilkan action nol jika robot sudah berada di target.
    if distance < 1e-8:
        return np.zeros(
            2,
            dtype=np.float32,
        )

    # Menghasilkan velocity menuju target.
    velocity = (
        direction
        / distance
        * max_speed
    )

    # Mengembalikan action dalam format float32.
    return velocity.astype(
        np.float32
    )
