# Import NumPy untuk operasi array.
import numpy as np


# Observation keys yang ingin kita gunakan
# ketika mengumpulkan demonstration data.
PREFERRED_KEYS = [
    "robot0_joint_pos",
    "robot0_joint_vel",
    "robot0_eef_pos",
    "robot0_eef_quat",
    "robot0_gripper_qpos",
    "Can_pos",
    "Can_quat",
]


# Memilih observation key yang tersedia.
def select_observation_keys(observation):

    selected_keys = []

    # Prioritaskan key yang sudah kita tentukan.
    for key in PREFERRED_KEYS:

        if key in observation:

            value = np.asarray(
                observation[key]
            )

            if (
                np.issubdtype(
                    value.dtype,
                    np.number
                )
                and value.size > 0
            ):

                selected_keys.append(
                    key
                )

    # Jika key utama ditemukan,
    # langsung gunakan.
    if selected_keys:

        return selected_keys


    # Fallback:
    # gunakan semua numeric observation
    # selain image.
    for key in sorted(
        observation.keys()
    ):

        if "image" in key.lower():

            continue


        value = np.asarray(
            observation[key]
        )


        if (
            np.issubdtype(
                value.dtype,
                np.number
            )
            and value.size > 0
        ):

            selected_keys.append(
                key
            )


    return selected_keys


# Menggabungkan observation menjadi
# satu vector.
def flatten_observation(
    observation,
    keys,
):

    parts = []


    for key in keys:

        value = np.asarray(
            observation[key],
            dtype=np.float32,
        )

        parts.append(
            value.reshape(-1)
        )


    if not parts:

        raise ValueError(
            "No numeric observation entries "
            "were selected."
        )


    state = np.concatenate(
        parts,
        axis=0,
    )


    return state.astype(
        np.float32
    )


# Mengambil posisi Can.
def get_can_position(
    observation
):

    # Key default PickPlaceCan.
    if "Can_pos" in observation:

        return np.asarray(
            observation["Can_pos"],
            dtype=np.float32,
        )


    # Fallback jika penamaan berbeda.
    for key in observation:

        lower_key = key.lower()

        if (
            "can" in lower_key
            and lower_key.endswith("_pos")
        ):

            return np.asarray(
                observation[key],
                dtype=np.float32,
            )


    raise KeyError(
        "Could not find Can position "
        "in observation."
    )


# Mengambil posisi end-effector.
def get_eef_position(
    observation
):

    if "robot0_eef_pos" not in observation:

        raise KeyError(
            "robot0_eef_pos was not found."
        )


    return np.asarray(
        observation["robot0_eef_pos"],
        dtype=np.float32,
    )


# Mengambil target placement
# untuk PickPlaceCan.
def get_target_position(
    env
):

    # PickPlace memiliki empat target bin:
    #
    # Milk   = 0
    # Bread  = 1
    # Cereal = 2
    # Can    = 3

    if hasattr(
        env,
        "target_bin_placements"
    ):

        placements = np.asarray(
            env.target_bin_placements,
            dtype=np.float32,
        )


        # PickPlaceCan memiliki
        # object_id = 3.
        object_id = int(
            getattr(
                env,
                "object_id",
                0,
            )
        )


        if (
            placements.ndim >= 2
            and object_id
            < len(placements)
        ):

            return placements[
                object_id
            ].copy()


    # Fallback jika API berbeda.
    if hasattr(
        env,
        "bin2_pos"
    ):

        bin_position = np.asarray(
            env.bin2_pos,
            dtype=np.float32,
        )


        return (
            bin_position
            + np.array(
                [
                    0.0,
                    0.0,
                    0.03,
                ],
                dtype=np.float32,
            )
        )


    raise AttributeError(
        "Could not determine "
        "PickPlace target position."
    )


# Mengecek keberhasilan task.
def check_success(
    env,
    info=None,
):

    # Jika info sudah memberikan
    # success flag, gunakan itu.
    if (
        info is not None
        and "success" in info
    ):

        return bool(
            info["success"]
        )


    # PickPlace memiliki
    # internal success checker.
    if hasattr(
        env,
        "_check_success"
    ):

        return bool(
            env._check_success()
        )


    return False
