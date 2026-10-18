# Menambahkan root repository ke Python path.
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# Import robosuite.
import robosuite as suite

# Import fungsi untuk memuat controller Panda.
from robosuite import load_composite_controller_config

# Import scripted expert.
from src.expert_policy import PickPlaceScriptedExpert

# Import helper untuk membaca state dan mengecek keberhasilan task.
from src.observation_utils import (
    check_success,
    get_can_position,
    get_eef_position,
    get_target_position,
)


# Fungsi untuk mengubah reference frame controller menjadi world.
def set_world_frame(config):

    # Mengecek setiap key dan value pada config.
    for key, value in config.items():

        # Jika menemukan input_ref_frame, ubah menjadi world.
        if key == "input_ref_frame":
            config[key] = "world"

        # Jika value masih berupa dictionary,
        # lanjutkan pencarian ke dalamnya.
        elif isinstance(value, dict):
            set_world_frame(value)


# Memuat controller default khusus Panda.
controller_config = load_composite_controller_config(
    robot="Panda"
)


# Mengubah reference frame controller menjadi world.
set_world_frame(
    controller_config
)


# Membuat environment PickPlaceCan.
env = suite.make(
    env_name="PickPlaceCan",
    robots="Panda",
    controller_configs=controller_config,
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    reward_shaping=True,
    control_freq=20,
    horizon=500,
)


# Membuat scripted expert.
expert = PickPlaceScriptedExpert()


# Reset environment.
observation = env.reset()


# Reset state machine expert.
expert.reset()


# Menampilkan informasi awal.
print("\nInitial setup")


# Menampilkan posisi end-effector.
print(
    "EEF position   :",
    get_eef_position(
        observation
    )
)


# Menampilkan posisi Can.
print(
    "Can position   :",
    get_can_position(
        observation
    )
)


# Menampilkan posisi target.
print(
    "Target position:",
    get_target_position(
        env
    )
)


# Menampilkan pesan awal rollout.
print(
    "\nStarting scripted expert...\n"
)


# Status keberhasilan awal.
success = False


# Menjalankan satu rollout.
for step in range(500):

    # Expert menghasilkan action dari observation.
    action = expert.act(
        observation,
        env,
    )


    # Menjalankan action di simulator.
    observation, reward, done, info = env.step(
        action
    )


    # Menampilkan simulator.
    env.render()


    # Mengecek apakah task berhasil.
    success = check_success(
        env,
        info,
    )


    # Menampilkan progress setiap 20 timestep.
    if step % 20 == 0:

        # Membaca posisi end-effector.
        eef_position = get_eef_position(
            observation
        )


        # Membaca posisi Can.
        can_position = get_can_position(
            observation
        )


        # Menampilkan informasi progress.
        print(
            f"Step {step:03d} | "
            f"phase={expert.phase:14s} | "
            f"reward={reward:.3f} | "
            f"success={success} | "
            f"EEF z={eef_position[2]:.3f} | "
            f"Can z={can_position[2]:.3f}"
        )


    # Menghentikan rollout jika task berhasil.
    if success:

        print(
            "\nTask succeeded "
            f"at step {step}!"
        )

        break


    # Menghentikan rollout jika episode selesai.
    if done:

        print(
            "\nEnvironment terminated."
        )

        break


# Menampilkan hasil akhir.
print(
    "\nFinal success:",
    success
)


# Menampilkan phase terakhir.
print(
    "Final phase  :",
    expert.phase
)


# Menutup environment.
env.close()
