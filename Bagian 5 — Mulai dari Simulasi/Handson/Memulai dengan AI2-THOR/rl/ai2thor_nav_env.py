# Import math untuk menghitung jarak.
import math

# Import random untuk randomisasi posisi awal agent.
import random

# Import NumPy untuk memproses observation.
import numpy as np

# Import Pillow untuk resize image.
from PIL import Image

# Import AI2-THOR Controller.
from ai2thor.controller import Controller


# Menentukan action space untuk navigation.
ACTIONS = [
    "RotateLeft",
    "MoveAhead",
    "RotateRight",
]


# Membuat environment RL berbasis AI2-THOR.
class AI2THORNavigationEnv:

    # Inisialisasi environment.
    def __init__(
        self,
        scene="FloorPlan1",
        target_object_type="Fridge",
        image_size=84,
        max_steps=150,
        success_distance=0.75,
        step_penalty=-0.01,
        failed_action_penalty=-0.05,
        progress_scale=1.0,
        success_reward=1.0,
        random_start=True,
        seed=42,
    ):

        # Menyimpan nama scene.
        self.scene = scene

        # Menyimpan jenis object tujuan.
        self.target_object_type = target_object_type

        # Menyimpan ukuran input CNN.
        self.image_size = image_size

        # Menyimpan jumlah timestep maksimum.
        self.max_steps = max_steps

        # Menyimpan jarak keberhasilan.
        self.success_distance = success_distance

        # Menyimpan penalty setiap timestep.
        self.step_penalty = step_penalty

        # Menyimpan penalty jika action gagal.
        self.failed_action_penalty = failed_action_penalty

        # Menyimpan skala reward progress.
        self.progress_scale = progress_scale

        # Menyimpan reward keberhasilan.
        self.success_reward = success_reward

        # Menentukan random starting position.
        self.random_start = random_start

        # Membuat random generator.
        self.rng = random.Random(
            seed
        )


        # Membuat AI2-THOR Controller.
        self.controller = Controller(
            scene=self.scene,
            agentMode="default",

            # Konfigurasi navigation.
            gridSize=0.25,
            snapToGrid=True,
            rotateStepDegrees=90,

            # Konfigurasi visual.
            width=640,
            height=480,
            fieldOfView=90,

            # Tidak menggunakan depth atau segmentation.
            renderDepthImage=False,
            renderInstanceSegmentation=False,

            # Selalu menampilkan Unity window.
            headless=False,
            fullscreen=False,
        )


        # Menyiapkan posisi goal.
        self.goal_position = None

        # Menyiapkan jarak sebelumnya.
        self.previous_distance = None

        # Menyiapkan penghitung timestep.
        self.step_count = 0


    # Mengembalikan jumlah action.
    @property
    def num_actions(
        self
    ):

        return len(
            ACTIONS
        )


    # Mengubah RGB frame menjadi state untuk CNN.
    def _frame_to_state(
        self,
        frame,
    ):

        # Mengubah NumPy array menjadi image.
        image = Image.fromarray(
            frame
        )


        # Resize menjadi 84x84.
        image = image.resize(
            (
                self.image_size,
                self.image_size,
            ),
            Image.BILINEAR,
        )


        # Mengubah image menjadi NumPy array.
        state = np.asarray(
            image,
            dtype=np.uint8,
        )


        # Mengubah format HWC menjadi CHW.
        state = np.transpose(
            state,
            (
                2,
                0,
                1,
            ),
        )


        # Mengembalikan state.
        return np.ascontiguousarray(
            state
        )


    # Menghitung jarak pada bidang XZ.
    @staticmethod
    def _xz_distance(
        position_a,
        position_b,
    ):

        # Menghitung selisih X.
        dx = (
            float(
                position_a["x"]
            )
            -
            float(
                position_b["x"]
            )
        )


        # Menghitung selisih Z.
        dz = (
            float(
                position_a["z"]
            )
            -
            float(
                position_b["z"]
            )
        )


        # Menghitung Euclidean distance.
        return math.sqrt(
            dx * dx
            +
            dz * dz
        )


    # Mencari object tujuan.
    def _find_target_object(
        self
    ):

        # Membaca semua object.
        objects = (
            self.controller
            .last_event
            .metadata["objects"]
        )


        # Mencari object sesuai target.
        candidates = [
            obj
            for obj in objects
            if obj["objectType"]
            == self.target_object_type
        ]


        # Menghentikan jika target tidak ditemukan.
        if not candidates:

            # Membaca semua jenis object.
            available = sorted(
                {
                    obj["objectType"]
                    for obj in objects
                }
            )


            raise RuntimeError(
                f"Target object type "
                f"{self.target_object_type!r} "
                f"was not found in "
                f"{self.scene}. "
                f"Available types include: "
                f"{available}"
            )


        # Menggunakan object pertama.
        return candidates[0]


    # Mencari navigation goal dekat target.
    def _find_goal_position(
        self
    ):

        # Mencari target object.
        target_object = (
            self._find_target_object()
        )


        # Membaca posisi target.
        target_position = (
            target_object["position"]
        )


        # Mencari semua posisi yang dapat dicapai.
        event = self.controller.step(
            action="GetReachablePositions"
        )


        # Membaca reachable positions.
        positions = event.metadata[
            "actionReturn"
        ]


        # Memastikan posisi tersedia.
        if not positions:

            raise RuntimeError(
                "GetReachablePositions "
                "returned no positions."
            )


        # Memilih posisi terdekat dengan target.
        goal_position = min(
            positions,
            key=lambda position:
            self._xz_distance(
                position,
                target_position,
            ),
        )


        # Mengembalikan goal.
        return goal_position


    # Mengacak starting position.
    def _randomize_start(
        self
    ):

        # Membaca reachable positions.
        event = self.controller.step(
            action="GetReachablePositions"
        )


        # Mengambil daftar posisi.
        reachable_positions = (
            event.metadata[
                "actionReturn"
            ]
        )


        # Memilih posisi minimal 1 meter dari goal.
        far_positions = [
            position
            for position
            in reachable_positions
            if self._xz_distance(
                position,
                self.goal_position,
            ) >= 1.0
        ]


        # Menggunakan semua posisi jika perlu.
        candidate_positions = (
            far_positions
            if far_positions
            else reachable_positions
        )


        # Memilih posisi awal random.
        start_position = (
            self.rng.choice(
                candidate_positions
            )
        )


        # Memilih orientasi awal.
        yaw = self.rng.choice(
            [
                0,
                90,
                180,
                270,
            ]
        )


        # Memindahkan agent.
        event = self.controller.step(
            action="Teleport",
            position=start_position,
            rotation={
                "x": 0.0,
                "y": float(yaw),
                "z": 0.0,
            },
            horizon=0.0,
            standing=True,
        )


        # Memastikan teleport berhasil.
        if not event.metadata[
            "lastActionSuccess"
        ]:

            raise RuntimeError(
                "Random-start Teleport failed: "
                + event.metadata.get(
                    "errorMessage",
                    "",
                )
            )


    # Membaca posisi agent.
    def _agent_position(
        self
    ):

        return (
            self.controller
            .last_event
            .metadata[
                "agent"
            ][
                "position"
            ]
        )


    # Reset episode.
    def reset(
        self
    ):

        # Reset scene.
        self.controller.reset(
            scene=self.scene
        )


        # Menentukan navigation goal.
        self.goal_position = (
            self._find_goal_position()
        )


        # Mengacak posisi awal.
        if self.random_start:

            self._randomize_start()


        # Reset penghitung timestep.
        self.step_count = 0


        # Menghitung jarak awal.
        self.previous_distance = (
            self._xz_distance(
                self._agent_position(),
                self.goal_position,
            )
        )


        # Membuat state awal.
        state = self._frame_to_state(
            self.controller
            .last_event
            .frame
        )


        # Mengembalikan state.
        return state


    # Menjalankan satu RL action.
    def step(
        self,
        action_index,
    ):

        # Memastikan action valid.
        if (
            action_index < 0
            or action_index >= len(ACTIONS)
        ):

            raise ValueError(
                f"Invalid action index: "
                f"{action_index}"
            )


        # Mengubah index menjadi nama action.
        action_name = ACTIONS[
            action_index
        ]


        # Menjalankan action.
        event = self.controller.step(
            action=action_name
        )


        # Menambah timestep.
        self.step_count += 1


        # Membaca status action.
        action_success = bool(
            event.metadata[
                "lastActionSuccess"
            ]
        )


        # Membaca posisi agent terbaru.
        agent_position = event.metadata[
            "agent"
        ][
            "position"
        ]


        # Menghitung jarak menuju goal.
        current_distance = (
            self._xz_distance(
                agent_position,
                self.goal_position,
            )
        )


        # Menghitung progress.
        progress = (
            self.previous_distance
            -
            current_distance
        )


        # Memberikan step penalty.
        reward = (
            self.step_penalty
        )


        # Memberikan reward berdasarkan progress.
        reward += (
            self.progress_scale
            *
            progress
        )


        # Memberikan penalty jika action gagal.
        if not action_success:

            reward += (
                self.failed_action_penalty
            )


        # Mengecek keberhasilan.
        success = (
            current_distance
            <= self.success_distance
        )


        # Memberikan success reward.
        if success:

            reward += (
                self.success_reward
            )


        # Mengecek apakah episode selesai.
        done = (
            success
            or
            self.step_count
            >= self.max_steps
        )


        # Menyimpan jarak terbaru.
        self.previous_distance = (
            current_distance
        )


        # Membuat state berikutnya.
        next_state = (
            self._frame_to_state(
                event.frame
            )
        )


        # Menyimpan informasi tambahan.
        info = {
            "action_name": action_name,
            "action_success": action_success,
            "distance_to_goal": current_distance,
            "progress": progress,
            "success": success,
            "step_count": self.step_count,
        }


        # Mengembalikan transition.
        return (
            next_state,
            float(reward),
            bool(done),
            info,
        )


    # Mengambil RGB frame asli.
    def rgb_frame(
        self
    ):

        return (
            self.controller
            .last_event
            .frame
            .copy()
        )


    # Menutup AI2-THOR.
    def close(
        self
    ):

        self.controller.stop()
