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


# Durasi gerakan robot.
MOVE_DURATION = 10.0


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


# Membuat path asset Franka Panda.
franka_asset_path = (
    assets_root_path
    + "/Isaac/Robots_Multiphysics/"
      "FrankaRobotics/FrankaPanda/"
      "franka/franka.usda"
)


# Menambahkan Franka ke stage.
stage_utils.add_reference_to_stage(
    usd_path=franka_asset_path,
    path="/World/Franka",
)


# Menempatkan Franka di world origin.
franka_transform = XformPrim(
    "/World/Franka"
)

franka_transform.set_world_poses(
    positions=[
        0.0,
        0.0,
        0.0,
    ]
)


# Membuat articulation wrapper.
franka = Articulation(
    "/World/Franka"
)


print(
    "Franka added.",
    flush=True,
)


# Menjalankan simulation timeline.
app_utils.play()


# Menunggu physics articulation aktif.
app_utils.update_app(
    steps=30
)


# Mengatur kamera agar fokus ke robot.
camera = ViewportManager.get_camera()

ViewportManager.set_camera_view(
    camera,
    eye=[
        1.7,
        1.7,
        1.3,
    ],
    target=[
        0.0,
        0.0,
        0.55,
    ],
)


app_utils.update_app(
    steps=10
)


# Membaca posisi awal.
initial_positions = np.asarray(
    franka.get_dof_positions(),
    dtype=np.float32,
).copy()


print(
    "Initial joint positions:",
    initial_positions,
    flush=True,
)


# Menentukan posisi target.
target_positions = np.array(
    [
        [
            0.0,
            -0.7,
            0.0,
            -2.0,
            0.0,
            1.5,
            0.8,
            0.04,
            0.04,
        ]
    ],
    dtype=np.float32,
)


print(
    "Target joint positions:",
    target_positions,
    flush=True,
)


print(
    f"Moving Franka for {MOVE_DURATION:.1f} seconds...",
    flush=True,
)


# Mencatat waktu mulai.
start_time = time.perf_counter()

last_second = -1


# Menggerakkan robot secara perlahan.
while True:

    # Menghitung waktu yang sudah berjalan.
    elapsed = time.perf_counter() - start_time

    # Menghitung progress gerakan.
    alpha = min(
        elapsed / MOVE_DURATION,
        1.0,
    )

    # Membuat gerakan lebih halus.
    smooth_alpha = (
        3.0 * alpha**2
        - 2.0 * alpha**3
    )

    # Menghitung target sementara.
    current_target = (
        initial_positions
        + smooth_alpha
        * (
            target_positions
            - initial_positions
        )
    )

    # Mengirim target ke robot.
    franka.set_dof_position_targets(
        current_target
    )

    # Update simulator.
    simulation_app.update()

    # Menampilkan posisi setiap satu detik.
    current_second = int(elapsed)

    if current_second != last_second:

        print(
            f"Time {elapsed:5.2f} s | "
            f"Progress {alpha * 100:5.1f}% | "
            f"Joint positions:",
            franka.get_dof_positions(),
            flush=True,
        )

        last_second = current_second

    # Selesai ketika target tercapai.
    if alpha >= 1.0:
        break

    # Membatasi loop agar tidak terlalu cepat.
    time.sleep(
        1.0 / 120.0
    )


# Memastikan target akhir tetap dikirim.
franka.set_dof_position_targets(
    target_positions
)


# Menjalankan beberapa frame tambahan.
app_utils.update_app(
    steps=30
)


# Membaca posisi akhir.
final_positions = franka.get_dof_positions()


print(
    "Final joint positions:",
    final_positions,
    flush=True,
)


print(
    "Joint movement completed.",
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
