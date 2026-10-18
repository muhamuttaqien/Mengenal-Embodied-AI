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
import omni.usd

import isaacsim.core.experimental.utils.stage as stage_utils

from isaacsim.core.experimental.objects import GroundPlane
from isaacsim.core.rendering_manager import RenderingManager
from isaacsim.core.simulation_manager import SimulationManager

from pxr import Gf
from pxr import UsdGeom
from pxr import UsdLux


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


# Menjalankan beberapa frame awal.
for step in range(120):

    # Menjalankan satu simulation step.
    SimulationManager.step()

    # Render viewport.
    RenderingManager.render()

    # Menampilkan progress.
    if step % 30 == 0:

        print(
            f"Simulation step: {step}",
            flush=True,
        )


print(
    "Scene ready.",
    flush=True,
)


print(
    "Tutup window Isaac Sim untuk mengakhiri program.",
    flush=True,
)


# Menjaga simulator tetap berjalan.
try:

    while simulation_app.is_running():

        # Menjalankan simulation.
        SimulationManager.step()

        # Render viewport.
        RenderingManager.render()


finally:

    # Menutup Isaac Sim.
    simulation_app.close()


print(
    "Isaac Sim closed.",
    flush=True,
)
