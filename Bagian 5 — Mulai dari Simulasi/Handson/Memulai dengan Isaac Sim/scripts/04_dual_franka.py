# Import SimulationApp terlebih dahulu.
from isaacsim.simulation_app import SimulationApp


# Membuka Isaac Sim.
simulation_app = SimulationApp(
    {
        "headless": False,
        "width": 1280,
        "height": 720,

        # Mengabaikan konfigurasi user lama.
        "extra_args": [
            "--reset-user",
        ],
    }
)


print(
    "Isaac Sim ready.",
    flush=True,
)


# Import API setelah SimulationApp aktif.
import time
import numpy as np
import omni.usd

import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils

from isaacsim.core.experimental.objects import GroundPlane
from isaacsim.core.experimental.prims import Articulation
from isaacsim.core.experimental.prims import XformPrim
from isaacsim.core.rendering_manager import ViewportManager
from isaacsim.storage.native import get_assets_root_path

from pxr import Gf
from pxr import UsdGeom
from pxr import UsdLux


# Durasi satu gerakan.
MOVE_DURATION = 8.0

# Jeda setelah mencapai pose.
HOLD_DURATION = 1.5


def move_robots(
    robots,
    target_positions,
    duration,
    description,
):
    """Menggerakkan kedua robot secara halus."""

    # Membaca posisi awal.
    start_positions = np.asarray(
        robots.get_dof_positions(),
        dtype=np.float32,
    ).copy()

    # Mengubah target menjadi array.
    target_positions = np.asarray(
        target_positions,
        dtype=np.float32,
    )

    print(
        description,
        flush=True,
    )

    start_time = time.perf_counter()

    last_second = -1


    while True:

        # Menghitung waktu.
        elapsed = (
            time.perf_counter()
            - start_time
        )

        # Menghitung progress.
        alpha = min(
            elapsed / duration,
            1.0,
        )

        # Membuat gerakan lebih halus.
        smooth_alpha = (
            3.0 * alpha**2
            - 2.0 * alpha**3
        )

        # Menghitung target sementara.
        current_target = (
            start_positions
            + smooth_alpha
            * (
                target_positions
                - start_positions
            )
        )

        # Mengirim target ke kedua robot.
        robots.set_dof_position_targets(
            current_target
        )

        # Update simulator.
        simulation_app.update()

        # Menampilkan progress setiap satu detik.
        current_second = int(
            elapsed
        )

        if current_second != last_second:

            print(
                f"Time {elapsed:5.2f} s | "
                f"Progress {alpha * 100:5.1f}%",
                flush=True,
            )

            last_second = current_second


        # Keluar ketika selesai.
        if alpha >= 1.0:
            break


        # Membatasi loop.
        time.sleep(
            1.0 / 120.0
        )


# Membaca root asset Isaac Sim.
assets_root_path = get_assets_root_path()


if assets_root_path is None:

    raise RuntimeError(
        "Isaac Sim asset root could not be found."
    )


# Membuat stage baru.
stage_utils.create_new_stage()


print(
    "USD Stage created.",
    flush=True,
)


# Mengambil stage aktif.
stage = omni.usd.get_context().get_stage()


# Menambahkan ground plane.
GroundPlane(
    "/World/GroundPlane",
    positions=[
        0.0,
        0.0,
        0.0,
    ],
)


# Menambahkan pencahayaan lingkungan.
dome_light = UsdLux.DomeLight.Define(
    stage,
    "/World/DomeLight",
)

dome_light.CreateIntensityAttr(
    800.0
)


# Menambahkan directional light.
distant_light = UsdLux.DistantLight.Define(
    stage,
    "/World/DistantLight",
)

distant_light.CreateIntensityAttr(
    2500.0
)

distant_light.CreateAngleAttr(
    1.0
)


# Mengatur arah cahaya.
light_xform = UsdGeom.Xformable(
    distant_light.GetPrim()
)

light_xform.AddRotateXYZOp().Set(
    Gf.Vec3f(
        -45.0,
        30.0,
        0.0,
    )
)


print(
    "Scene and lighting ready.",
    flush=True,
)


# Path asset Franka Panda.
franka_asset_path = (
    assets_root_path
    + "/Isaac/Robots_Multiphysics/"
      "FrankaRobotics/FrankaPanda/"
      "franka/franka.usda"
)


# Menambahkan Franka kiri.
stage_utils.add_reference_to_stage(
    usd_path=franka_asset_path,
    path="/World/Franka_Left",
)


# Menambahkan Franka kanan.
stage_utils.add_reference_to_stage(
    usd_path=franka_asset_path,
    path="/World/Franka_Right",
)


print(
    "Two Franka robots added.",
    flush=True,
)


# Membuat transform robot kiri.
franka_left_xform = XformPrim(
    "/World/Franka_Left"
)


# Menempatkan robot kiri.
franka_left_xform.set_world_poses(
    positions=np.array(
        [
            [
                -0.75,
                0.0,
                0.0,
            ]
        ],
        dtype=np.float32,
    ),
    orientations=np.array(
        [
            [
                1.0,
                0.0,
                0.0,
                0.0,
            ]
        ],
        dtype=np.float32,
    ),
)


# Membuat transform robot kanan.
franka_right_xform = XformPrim(
    "/World/Franka_Right"
)


# Menempatkan robot kanan dan memutarnya 180 derajat.
franka_right_xform.set_world_poses(
    positions=np.array(
        [
            [
                0.75,
                0.0,
                0.0,
            ]
        ],
        dtype=np.float32,
    ),
    orientations=np.array(
        [
            [
                0.0,
                0.0,
                0.0,
                1.0,
            ]
        ],
        dtype=np.float32,
    ),
)


print(
    "Franka robots positioned face-to-face.",
    flush=True,
)


# Membuat articulation untuk kedua robot.
robots = Articulation(
    "/World/Franka_.*"
)


# Menjalankan simulation timeline.
app_utils.play()


# Menunggu physics aktif.
app_utils.update_app(
    steps=30
)


print(
    "Simulation started.",
    flush=True,
)


# Mengatur kamera agar kedua robot terlihat.
camera = ViewportManager.get_camera()


ViewportManager.set_camera_view(
    camera,
    eye=[
        0.0,
        3.2,
        1.8,
    ],
    target=[
        0.0,
        0.0,
        0.65,
    ],
)


# Update setelah kamera dipindahkan.
app_utils.update_app(
    steps=10
)


print(
    "Camera focused on both robots.",
    flush=True,
)


# Menampilkan robot yang terdeteksi.
print(
    "Robot paths:",
    robots.paths,
    flush=True,
)


print(
    "Number of robots:",
    len(robots.paths),
    flush=True,
)


print(
    "Number of DoFs:",
    robots.num_dofs,
    flush=True,
)


print(
    "Joint names:",
    robots.dof_names,
    flush=True,
)


# Membaca posisi awal kedua robot.
initial_positions = np.asarray(
    robots.get_dof_positions(),
    dtype=np.float32,
).copy()


print(
    "Initial joint positions:",
    initial_positions,
    flush=True,
)


# Target robot pertama.
left_target = [
    0.30,
    -0.75,
    0.0,
    -2.0,
    0.0,
    1.55,
    0.8,
    0.04,
    0.04,
]


# Target robot kedua.
right_target = [
    -0.30,
    -0.75,
    0.0,
    -2.0,
    0.0,
    1.55,
    0.8,
    0.04,
    0.04,
]


# Menggabungkan target kedua robot.
coordinated_target = np.array(
    [
        left_target,
        right_target,
    ],
    dtype=np.float32,
)


print(
    "Coordinated target:",
    coordinated_target,
    flush=True,
)


# Menggerakkan kedua robot menuju tengah.
move_robots(
    robots,
    coordinated_target,
    MOVE_DURATION,
    "Moving both Franka robots toward the center...",
)


print(
    "Center pose reached.",
    flush=True,
)


# Menahan pose sebentar.
hold_start = time.perf_counter()


while (
    time.perf_counter()
    - hold_start
    < HOLD_DURATION
):

    simulation_app.update()


# Mengembalikan kedua robot ke pose awal.
move_robots(
    robots,
    initial_positions,
    MOVE_DURATION,
    "Returning both Franka robots to the initial pose...",
)


print(
    "Both robots returned.",
    flush=True,
)


# Menjalankan beberapa frame tambahan.
app_utils.update_app(
    steps=30
)


# Membaca posisi akhir.
final_positions = np.asarray(
    robots.get_dof_positions(),
    dtype=np.float32,
)


print(
    "Final joint positions:",
    final_positions,
    flush=True,
)


print(
    "Dual Franka demonstration completed.",
    flush=True,
)


print(
    "Tutup window Isaac Sim untuk mengakhiri program.",
    flush=True,
)


# Menjaga simulator tetap terbuka.
try:

    while simulation_app.is_running():

        simulation_app.update()


finally:

    # Menghentikan simulation.
    app_utils.stop()

    # Menutup Isaac Sim.
    simulation_app.close()


print(
    "Isaac Sim closed.",
    flush=True,
)
