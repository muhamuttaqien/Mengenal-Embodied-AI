# Menambahkan root repository ke Python path.
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# Import argparse untuk menerima argument dari terminal.
import argparse

# Import NumPy untuk menyimpan demonstration data.
import numpy as np

# Import robosuite.
import robosuite as suite

# Import progress bar.
from tqdm import tqdm

# Import fungsi untuk memuat controller Panda.
from robosuite import load_composite_controller_config

# Import scripted expert.
from src.expert_policy import PickPlaceScriptedExpert

# Import helper untuk observation dan success.
from src.observation_utils import (
    check_success,
    flatten_observation,
    select_observation_keys,
)


# Fungsi untuk mengubah reference frame controller menjadi world.
def set_world_frame(config):

    # Membaca setiap bagian controller config.
    for key, value in config.items():

        # Mengubah input reference frame menjadi world.
        if key == "input_ref_frame":
            config[key] = "world"

        # Melanjutkan pencarian jika masih berupa dictionary.
        elif isinstance(value, dict):
            set_world_frame(value)


# Membuat command-line parser.
parser = argparse.ArgumentParser(
    description="Collect scripted PickPlaceCan demonstrations."
)


# Menentukan jumlah demonstration yang ingin disimpan.
parser.add_argument(
    "--episodes",
    type=int,
    default=3,
    help="Number of successful demonstrations to save.",
)


# Menambahkan pilihan untuk menampilkan simulator.
parser.add_argument(
    "--render",
    action="store_true",
    help="Show the robosuite viewer during collection.",
)


# Menentukan jumlah percobaan maksimum.
parser.add_argument(
    "--max-attempts",
    type=int,
    default=20,
    help="Maximum episode attempts before stopping.",
)


# Membaca argument dari terminal.
args = parser.parse_args()


# Menentukan folder penyimpanan dataset.
DATA_DIR = Path(
    "data/demonstrations"
)


# Membuat folder dataset jika belum tersedia.
DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# Memuat controller default Panda.
controller_config = load_composite_controller_config(
    robot="Panda"
)


# Mengubah reference frame menjadi world.
set_world_frame(
    controller_config
)


# Membuat environment PickPlaceCan.
env = suite.make(
    env_name="PickPlaceCan",
    robots="Panda",
    controller_configs=controller_config,
    has_renderer=args.render,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    reward_shaping=True,
    control_freq=20,
    horizon=500,
)


# Membuat scripted expert.
expert = PickPlaceScriptedExpert()


# Menghitung jumlah demonstration yang berhasil disimpan.
saved_episodes = 0


# Menghitung jumlah percobaan.
attempts = 0


# Membuat progress bar.
progress = tqdm(
    total=args.episodes,
    desc="Successful demos",
)


# Mengumpulkan demonstration sampai jumlah yang diminta tercapai.
while (
    saved_episodes < args.episodes
    and attempts < args.max_attempts
):

    # Menambah jumlah percobaan.
    attempts += 1


    # Reset environment.
    observation = env.reset()


    # Reset scripted expert.
    expert.reset()


    # Memilih observation yang akan disimpan.
    observation_keys = select_observation_keys(
        observation
    )


    # Menyiapkan tempat penyimpanan observation.
    observations = []


    # Menyiapkan tempat penyimpanan action.
    actions = []


    # Menyiapkan tempat penyimpanan reward.
    rewards = []


    # Status keberhasilan awal.
    success = False


    # Menjalankan satu episode.
    for step in range(500):

        # Mengubah observation menjadi satu vector.
        state_vector = flatten_observation(
            observation,
            observation_keys,
        )


        # Scripted expert menghasilkan action.
        action = expert.act(
            observation,
            env,
        )


        # Menyimpan observation.
        observations.append(
            state_vector
        )


        # Menyimpan action.
        actions.append(
            np.asarray(
                action,
                dtype=np.float32,
            )
        )


        # Menjalankan action di simulator.
        next_observation, reward, done, info = env.step(
            action
        )


        # Menyimpan reward.
        rewards.append(
            float(reward)
        )


        # Menampilkan simulator jika diminta.
        if args.render:
            env.render()


        # Mengecek keberhasilan task.
        success = check_success(
            env,
            info,
        )


        # Menggunakan observation berikutnya.
        observation = next_observation


        # Menghentikan episode jika berhasil.
        if success:
            break


        # Menghentikan episode jika selesai.
        if done:
            break


    # Menyimpan hanya episode yang berhasil.
    if success:

        # Membuat nama file demonstration.
        output_path = (
            DATA_DIR
            / f"demo_{saved_episodes:03d}.npz"
        )


        # Menyimpan demonstration ke file NPZ.
        np.savez_compressed(
            output_path,

            observations=np.asarray(
                observations,
                dtype=np.float32,
            ),

            actions=np.asarray(
                actions,
                dtype=np.float32,
            ),

            rewards=np.asarray(
                rewards,
                dtype=np.float32,
            ),

            success=np.asarray(
                [True],
                dtype=np.bool_,
            ),

            observation_keys=np.asarray(
                observation_keys,
                dtype=str,
            ),
        )


        # Menambah jumlah demonstration yang berhasil.
        saved_episodes += 1


        # Memperbarui progress bar.
        progress.update(1)


        # Menampilkan lokasi file yang disimpan.
        progress.write(
            f"Saved {output_path} "
            f"with {len(actions)} timesteps."
        )


    # Menampilkan percobaan yang gagal.
    else:

        progress.write(
            f"Attempt {attempts} failed; not saved."
        )


# Menutup progress bar.
progress.close()


# Menutup environment.
env.close()


# Menampilkan hasil pengumpulan demonstration.
print(
    f"Saved {saved_episodes}/{args.episodes} "
    f"successful demonstrations "
    f"after {attempts} attempts."
)


# Menampilkan peringatan jika target belum tercapai.
if saved_episodes < args.episodes:

    print(
        "The requested number of successful demos "
        "was not reached."
    )
