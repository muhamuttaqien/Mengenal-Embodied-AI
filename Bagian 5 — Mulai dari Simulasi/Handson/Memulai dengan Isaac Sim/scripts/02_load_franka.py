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
import asyncio
from pathlib import Path

import omni.usd

import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils

from isaacsim.core.experimental.objects import GroundPlane
from isaacsim.core.experimental.prims import Articulation
from isaacsim.core.experimental.prims import XformPrim
from isaacsim.core.rendering_manager import ViewportManager
from isaacsim.storage.native import get_assets_root_path

from omni.kit.viewport.utility import capture_viewport_to_file
from omni.kit.viewport.utility import get_active_viewport

from pxr import Gf
from pxr import UsdGeom
from pxr import UsdLux


# Menentukan folder results.
project_dir = Path(
    __file__
).resolve().parent.parent

results_dir = (
    project_dir
    / "results"
)

results_dir.mkdir(
    parents=True,
    exist_ok=True,
)


# Menentukan file screenshot.
image_path = (
    results_dir
    / "02_load_franka.png"
)


# Membaca root asset Isaac Sim.
assets_root_path = get_assets_root_path()


if assets_root_path is None:

    raise RuntimeError(
        "Isaac Sim asset root could not be found."
    )


# Membuat USD stage baru.
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


print(
    "Ground plane added.",
    flush=True,
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
    "Lighting added.",
    flush=True,
)


# Membuat path asset Franka Panda.
franka_asset_path = (
    assets_root_path
    + "/Isaac/Robots_Multiphysics/"
      "FrankaRobotics/FrankaPanda/"
      "franka/franka.usda"
)


print(
    "Franka asset:",
    franka_asset_path,
    flush=True,
)


# Menambahkan Franka ke stage.
stage_utils.add_reference_to_stage(
    usd_path=franka_asset_path,
    path="/World/Franka",
)


print(
    "Franka added to stage.",
    flush=True,
)


# Membuat wrapper transform Franka.
franka_transform = XformPrim(
    "/World/Franka"
)


# Menempatkan Franka pada world origin.
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


# Menjalankan simulation timeline.
app_utils.play()


print(
    "Simulation started.",
    flush=True,
)


# Menunggu physics dan asset selesai diinisialisasi.
app_utils.update_app(
    steps=30
)


# Mengambil kamera aktif.
camera = ViewportManager.get_camera()


# Mengatur kamera agar fokus ke Franka.
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


# Update beberapa frame setelah kamera dipindahkan.
app_utils.update_app(
    steps=30
)


print(
    "Camera focused on Franka.",
    flush=True,
)


# Menampilkan jumlah DoF.
print(
    "Number of DoFs:",
    franka.num_dofs,
)


# Menampilkan nama joint.
print(
    "Joint names:",
    franka.dof_names,
)


# Membaca posisi joint.
joint_positions = franka.get_dof_positions()


print(
    "Joint positions:",
    joint_positions,
)


print(
    "Franka successfully initialized.",
    flush=True,
)


# Mengambil viewport aktif.
viewport = get_active_viewport()


if viewport is None:

    raise RuntimeError(
        "Active viewport could not be found."
    )


# Menyimpan viewport sebagai gambar.
capture_helper = capture_viewport_to_file(
    viewport,
    file_path=str(
        image_path
    ),
)


# Menunggu proses screenshot selesai.
capture_task = asyncio.ensure_future(
    capture_helper.wait_for_result(
        completion_frames=30
    )
)


while not capture_task.done():

    simulation_app.update()


# Memeriksa hasil screenshot.
capture_task.result()


print(
    "Screenshot saved to:",
    image_path,
    flush=True,
)


print(
    "Tutup window Isaac Sim untuk mengakhiri program.",
    flush=True,
)


# Menjaga simulator tetap berjalan.
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
