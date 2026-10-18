# Import Path untuk mengatur folder output.
from pathlib import Path

# Import Pillow untuk menyimpan RGB observation.
from PIL import Image

# Import AI2-THOR Controller.
from ai2thor.controller import Controller


# Membuat folder results jika belum tersedia.
RESULT_DIR = Path(
    "results"
)

RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# Menentukan empat kategori room dan scene perwakilannya.
ROOM_SCENES = [
    ("Kitchen", "FloorPlan1"),
    ("LivingRoom", "FloorPlan201"),
    ("Bedroom", "FloorPlan301"),
    ("Bathroom", "FloorPlan401"),
]


# Membuat AI2-THOR Controller.
controller = Controller(
    scene="FloorPlan1",
    gridSize=0.25,
    rotateStepDegrees=90,
    width=640,
    height=480,
    fieldOfView=90,
)


try:

    # Membuka setiap scene secara bergantian.
    for room_name, scene_name in ROOM_SCENES:

        # Membuka scene.
        event = controller.reset(
            scene_name
        )


        # Mengambil observation terbaru.
        event = controller.step(
            action="Pass"
        )


        # Mengambil RGB observation.
        rgb_frame = event.frame


        # Membuat nama file berdasarkan scene dan room.
        output_path = (
            RESULT_DIR
            / f"{scene_name}_{room_name}.png"
        )


        # Menyimpan RGB observation.
        Image.fromarray(
            rgb_frame
        ).save(
            output_path
        )


        # Menampilkan hasil.
        print(
            f"{scene_name:<12} "
            f"{room_name:<12} "
            f"-> {output_path}"
        )


    # Menampilkan informasi setelah semua gambar tersimpan.
    print(
        "\nEmpat gambar berhasil disimpan."
    )


    # Menjaga scene terakhir tetap terbuka.
    print(
        "Simulator tetap terbuka pada scene terakhir."
    )


    # Menunggu sebelum simulator ditutup.
    input(
        "\nTekan Enter untuk menutup simulator..."
    )


# Menangani Ctrl+C.
except KeyboardInterrupt:

    print(
        "\nSimulator dihentikan."
    )


# Selalu menutup controller dengan aman.
finally:

    controller.stop()
