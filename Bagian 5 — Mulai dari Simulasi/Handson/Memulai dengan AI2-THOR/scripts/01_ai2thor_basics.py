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

    # Mengambil event awal.
    event = controller.last_event


    # Membaca posisi awal agent.
    initial_position = event.metadata[
        "agent"
    ][
        "position"
    ]


    # Menampilkan posisi awal agent.
    print(
        "Initial position:",
        initial_position
    )


    # Menjalankan MoveAhead.
    event = controller.step(
        action="MoveAhead"
    )


    # Menampilkan status MoveAhead.
    print(
        "MoveAhead success:",
        event.metadata[
            "lastActionSuccess"
        ]
    )


    # Menjalankan RotateRight.
    event = controller.step(
        action="RotateRight"
    )


    # Menampilkan status RotateRight.
    print(
        "RotateRight success:",
        event.metadata[
            "lastActionSuccess"
        ]
    )


    # Membaca semua object pada scene.
    objects = event.metadata[
        "objects"
    ]


    # Menampilkan jumlah object.
    print(
        "Objects in scene:",
        len(objects)
    )


    # Mengambil RGB observation.
    rgb_frame = event.frame


    # Menentukan lokasi output.
    output_path = (
        RESULT_DIR
        / "ai2thor_basics.png"
    )


    # Menyimpan RGB observation.
    Image.fromarray(
        rgb_frame
    ).save(
        output_path
    )


    # Menampilkan lokasi hasil.
    print(
        "Saved:",
        output_path
    )


    # Menjaga simulator tetap terbuka.
    print(
        "\nSimulator tetap terbuka."
    )

    print(
        "Silakan ambil screenshot jika diperlukan."
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
