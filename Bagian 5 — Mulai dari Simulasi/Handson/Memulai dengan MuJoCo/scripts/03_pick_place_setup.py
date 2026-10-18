# Menambahkan root repository ke Python path.
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# Import NumPy untuk menampilkan nilai numerik dengan lebih rapi.
import numpy as np

# Import robosuite.
import robosuite as suite

# Import helper function dari folder src.
from src.observation_utils import (
    get_can_position,
    get_eef_position,
    get_target_position,
)


# Mengatur tampilan NumPy agar lebih mudah dibaca.
np.set_printoptions(
    precision=4,
    suppress=True,
)


# Membuat environment PickPlaceCan.
env = suite.make(
    env_name="PickPlaceCan",
    robots="Panda",
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    reward_shaping=True,
    control_freq=20,
    horizon=500,
)


# Reset environment dan membaca observation pertama.
observation = env.reset()


# Membaca batas action.
action_low, action_high = env.action_spec


# Menampilkan jumlah dimensi action.
print("Action dimension:", action_low.shape[0])


# Menampilkan semua observation key.
print("\nObservation keys:")

for key, value in observation.items():

    # Mengubah value menjadi NumPy array agar shape bisa dibaca.
    array_value = np.asarray(value)

    print(
        f"- {key}: shape={array_value.shape}"
    )


# Membaca posisi end-effector.
eef_position = get_eef_position(
    observation
)


# Membaca posisi Can.
can_position = get_can_position(
    observation
)


# Membaca posisi target placement.
target_position = get_target_position(
    env
)


# Menampilkan posisi penting.
print(
    "\nEnd-effector position:",
    eef_position
)

print(
    "Can position         :",
    can_position
)

print(
    "Target position      :",
    target_position
)


# Menjalankan simulator beberapa timestep
# agar setup tetap terlihat di viewer.
for _ in range(200):

    # Membuat action nol.
    action = np.zeros_like(
        action_low,
        dtype=np.float32
    )

    # Membuka gripper.
    action[-1] = -1.0

    # Menjalankan satu simulation step.
    observation, reward, done, info = env.step(
        action
    )

    # Render environment.
    env.render()

    # Hentikan jika episode selesai.
    if done:
        break


# Menutup environment.
env.close()
