# Import argparse untuk menerima pilihan dari terminal.
import argparse

# Import AI2-THOR Controller.
from ai2thor.controller import Controller


# Membuat command-line parser.
parser = argparse.ArgumentParser(
    description="Inspect a ManipulaTHOR kitchen pick-and-place setup."
)


# Menentukan scene.
parser.add_argument(
    "--scene",
    default="FloorPlan1",
)


# Menentukan object yang akan diambil.
parser.add_argument(
    "--object-type",
    default="Tomato",
)


# Menentukan receptacle tujuan.
parser.add_argument(
    "--receptacle-type",
    default="Drawer",
)


# Membaca argument dari terminal.
args = parser.parse_args()


# Membuat ManipulaTHOR Controller.
controller = Controller(
    agentMode="arm",
    scene=args.scene,
    visibilityDistance=1.5,
    gridSize=0.25,
    width=640,
    height=480,
    fieldOfView=60,
)


try:

    # Membaca semua metadata object.
    objects = controller.last_event.metadata[
        "objects"
    ]


    # Mencari object yang sesuai.
    pickup_candidates = [
        obj
        for obj in objects
        if obj[
            "objectType"
        ] == args.object_type
    ]


    # Mencari receptacle yang sesuai.
    receptacle_candidates = [
        obj
        for obj in objects
        if obj[
            "objectType"
        ] == args.receptacle_type
    ]


    # Memeriksa apakah object tersedia.
    if not pickup_candidates:

        # Membaca semua tipe object pada scene.
        available = sorted(
            {
                obj["objectType"]
                for obj in objects
            }
        )


        # Menghentikan script jika object tidak ditemukan.
        raise RuntimeError(
            f"{args.object_type} was not found "
            f"in {args.scene}. "
            f"Available types include: {available}"
        )


    # Memeriksa apakah receptacle tersedia.
    if not receptacle_candidates:

        # Membaca semua receptacle yang tersedia.
        available_receptacles = sorted(
            {
                obj["objectType"]
                for obj in objects
                if obj.get(
                    "receptacle",
                    False
                )
            }
        )


        # Menghentikan script jika receptacle tidak ditemukan.
        raise RuntimeError(
            f"{args.receptacle_type} was not found "
            f"in {args.scene}. "
            f"Available receptacle types include: "
            f"{available_receptacles}"
        )


    # Memilih object pertama yang ditemukan.
    pickup_object = pickup_candidates[0]


    # Memilih receptacle pertama yang ditemukan.
    receptacle = receptacle_candidates[0]


    # Menampilkan nama scene.
    print(
        "Scene:",
        args.scene
    )


    # Menampilkan ID object.
    print(
        "Object:",
        pickup_object[
            "objectId"
        ]
    )


    # Menampilkan apakah object dapat diambil.
    print(
        "Pickupable:",
        pickup_object[
            "pickupable"
        ]
    )


    # Menampilkan posisi object.
    print(
        "Object position:",
        pickup_object[
            "position"
        ]
    )


    # Menampilkan ID receptacle.
    print(
        "Receptacle:",
        receptacle[
            "objectId"
        ]
    )


    # Menampilkan status receptacle.
    print(
        "Is receptacle:",
        receptacle[
            "receptacle"
        ]
    )


    # Menampilkan posisi receptacle.
    print(
        "Receptacle position:",
        receptacle[
            "position"
        ]
    )


    # Menampilkan posisi hand sphere.
    print(
        "Hand sphere:",
        controller.last_event.metadata[
            "arm"
        ][
            "handSphereCenter"
        ]
    )


    # Menampilkan status setup.
    print(
        "\nSetup validated."
    )

    print(
        "The next step is manual "
        "or learned control."
    )


    # Menjaga simulator tetap terbuka.
    print(
        "\nSimulator tetap terbuka."
    )

    print(
        "Silakan periksa setup atau "
        "ambil screenshot."
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
