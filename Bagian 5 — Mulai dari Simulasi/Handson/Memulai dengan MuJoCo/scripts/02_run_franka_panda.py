# Import NumPy untuk membuat action vector.
import numpy as np

# Import robosuite.
import robosuite as suite


# Membuat environment Lift dengan Franka Panda.
env = suite.make(
    env_name="Lift",
    robots="Panda",
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    reward_shaping=True,
    control_freq=20,
    horizon=300,
)


# Reset environment dan mengambil observation awal.
observation = env.reset()


# Membaca batas minimum dan maksimum action.
action_low, action_high = env.action_spec


# Menampilkan jumlah dimensi action.
print(
    "Action dimension:",
    action_low.shape[0]
)


# Menampilkan semua observation key.
print(
    "Observation keys:"
)


# Membaca setiap observation key.
for key in observation.keys():

    print(
        "-",
        key
    )


# Menjalankan demo gerakan sederhana.
for step in range(240):

    # Membuat action nol.
    action = np.zeros_like(
        action_low,
        dtype=np.float32
    )


    # Menggerakkan robot perlahan ke arah +X.
    if step < 80:

        action[0] = 0.25


    # Menggerakkan robot perlahan ke arah -X.
    elif step < 160:

        action[0] = -0.25


    # Menghentikan gerakan translasi.
    else:

        action[0] = 0.0


    # Membiarkan gripper tetap terbuka.
    if action.size > 0:

        action[-1] = -1.0


    # Menjalankan action di environment.
    observation, reward, done, info = env.step(
        action
    )


    # Menampilkan simulator.
    env.render()


    # Menghentikan rollout jika episode selesai.
    if done:

        break


# Menutup environment.
env.close()
