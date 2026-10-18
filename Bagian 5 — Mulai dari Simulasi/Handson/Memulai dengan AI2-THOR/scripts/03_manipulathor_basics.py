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


# Membuat ManipulaTHOR Controller.
controller = Controller(
    agentMode="arm",
    scene="FloorPlan3",
    visibilityDistance=1.5,
    gridSize=0.25,
    width=800,
    height=600,
    fieldOfView=90,
    renderDepthImage=False,
    renderInstanceSegmentation=False,
)


try:

    # Mengambil event awal.
    event = controller.last_event


    # Menampilkan posisi awal hand sphere.
    print(
        "Initial hand sphere:",
        event.metadata["arm"]["handSphereCenter"]
    )


    # Menggerakkan agent sedikit agar background kitchen lebih terlihat.
    event = controller.step(
        action="MoveAgent",
        ahead=0.10,
        right=0.0,
        returnToStart=True,
        speed=1,
        fixedDeltaTime=0.02,
    )

    print(
        "MoveAgent success:",
        event.metadata["lastActionSuccess"]
    )


    # Memutar agent sedikit ke kanan.
    event = controller.step(
        action="RotateAgent",
        degrees=15,
        returnToStart=True,
        speed=15,
        fixedDeltaTime=0.02,
    )

    print(
        "RotateAgent success:",
        event.metadata["lastActionSuccess"]
    )


    # Menaikkan arm base agar lengan lebih masuk ke frame kamera.
    event = controller.step(
        action="MoveArmBase",
        y=0.75,
        speed=1,
        returnToStart=True,
        fixedDeltaTime=0.02,
    )

    print(
        "MoveArmBase success:",
        event.metadata["lastActionSuccess"]
    )


    # Menggerakkan arm ke depan dan sedikit ke atas
    # agar arm terlihat jelas pada view.
    event = controller.step(
        action="MoveArm",
        position={
            "x": 0.00,
            "y": 0.15,
            "z": 0.45,
        },
        coordinateSpace="armBase",
        restrictMovement=False,
        speed=1,
        returnToStart=True,
        fixedDeltaTime=0.02,
    )

    print(
        "MoveArm success:",
        event.metadata["lastActionSuccess"]
    )


    # Menampilkan posisi akhir hand sphere.
    print(
        "Final hand sphere:",
        event.metadata["arm"]["handSphereCenter"]
    )


    # Menampilkan object yang dekat dengan hand.
    print(
        "Pickupable near hand:",
        event.metadata["arm"]["pickupableObjects"]
    )


    # Mengambil frame terakhir.
    rgb_frame = event.frame


    # Menentukan lokasi output image.
    output_path = (
        RESULT_DIR
        / "manipulathor_basics_view.png"
    )


    # Menyimpan image.
    Image.fromarray(
        rgb_frame
    ).save(
        output_path
    )


    # Menampilkan lokasi file hasil.
    print(
        "Saved:",
        output_path
    )


    # Menjaga simulator tetap terbuka.
    print(
        "\nSimulator tetap terbuka."
    )

    print(
        "Silakan cek view dan ambil screenshot jika diperlukan."
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


# Selalu menutup controller.
finally:

    controller.stop()
