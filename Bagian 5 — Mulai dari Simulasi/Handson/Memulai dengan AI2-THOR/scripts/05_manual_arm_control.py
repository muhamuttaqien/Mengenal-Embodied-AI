# Import OpenCV untuk menampilkan live view.
import cv2

# Import AI2-THOR Controller.
from ai2thor.controller import Controller


# Menentukan langkah gerakan arm.
ARM_STEP = 0.05

# Menentukan langkah gerakan mobile base.
BASE_STEP = 0.10

# Menentukan langkah rotasi.
ROTATE_STEP = 15.0

# Menentukan posisi awal arm base.
arm_base_height = 0.50


# Menentukan scene.
SCENE_NAME = "FloorPlan3"


# Fungsi untuk menentukan kategori ruangan.
def get_room_name(scene_name):

    # Mengambil nomor FloorPlan.
    number = int(
        scene_name.replace(
            "FloorPlan",
            ""
        )
    )

    # FloorPlan 1-30 adalah kitchen.
    if 1 <= number <= 30:
        return "Kitchen"

    # FloorPlan 201-230 adalah living room.
    elif 201 <= number <= 230:
        return "Living Room"

    # FloorPlan 301-330 adalah bedroom.
    elif 301 <= number <= 330:
        return "Bedroom"

    # FloorPlan 401-430 adalah bathroom.
    elif 401 <= number <= 430:
        return "Bathroom"

    return "Unknown"


# Fungsi untuk mengambil object yang terlihat.
def get_visible_objects(event):

    # Memilih object dengan visible=True.
    visible_objects = [
        obj["objectType"]
        for obj in event.metadata["objects"]
        if obj.get(
            "visible",
            False
        )
    ]

    # Menghapus nama object yang sama.
    visible_objects = sorted(
        set(
            visible_objects
        )
    )

    return visible_objects


# Fungsi untuk menampilkan live view.
def show_monitor(event):

    # Mengambil RGB image.
    frame = event.frame.copy()


    # Mengubah RGB menjadi BGR untuk OpenCV.
    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2BGR
    )


    # Membaca metadata agent.
    agent = event.metadata[
        "agent"
    ]


    # Membaca posisi robot.
    position = agent[
        "position"
    ]


    # Membaca rotasi robot.
    rotation = agent[
        "rotation"
    ]


    # Membaca object yang terlihat.
    visible_objects = get_visible_objects(
        event
    )


    # Membatasi daftar object agar tidak terlalu panjang.
    visible_text = ", ".join(
        visible_objects[:8]
    )


    # Menambahkan tanda jika masih ada object lain.
    if len(visible_objects) > 8:

        visible_text += ", ..."


    # Menentukan nama ruangan.
    room_name = get_room_name(
        SCENE_NAME
    )


    # Membuat background gelap untuk teks.
    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (640, 105),
        (0, 0, 0),
        -1
    )


    # Membuat background sedikit transparan.
    frame = cv2.addWeighted(
        overlay,
        0.65,
        frame,
        0.35,
        0
    )


    # Menampilkan nama ruangan.
    cv2.putText(
        frame,
        f"Room: {room_name} | {SCENE_NAME}",
        (15, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )


    # Menampilkan posisi robot.
    cv2.putText(
        frame,
        (
            f"Robot: "
            f"x={position['x']:.2f}, "
            f"y={position['y']:.2f}, "
            f"z={position['z']:.2f}, "
            f"rot={rotation['y']:.1f} deg"
        ),
        (15, 52),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )


    # Menampilkan object yang terlihat.
    cv2.putText(
        frame,
        (
            f"Visible objects "
            f"({len(visible_objects)}): "
            f"{visible_text}"
        ),
        (15, 79),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.43,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )


    # Menampilkan window.
    cv2.imshow(
        "ManipulaTHOR Monitor",
        frame
    )


    # Memperbarui window OpenCV.
    cv2.waitKey(1)


# Membuat ManipulaTHOR Controller.
controller = Controller(
    agentMode="arm",
    scene=SCENE_NAME,
    visibilityDistance=1.5,
    gridSize=0.25,
    width=640,
    height=480,
    fieldOfView=60,
)


# Menampilkan daftar kontrol.
print(
    """
Commands
--------

w / s : base forward / backward
a / d : rotate left / right

j / l : arm left / right
u / o : arm up / down
i / k : arm forward / backward

r / f : arm base up / down

p     : pickup object
x     : release object

info  : print information
q     : quit
"""
)


try:

    # Menampilkan view awal.
    show_monitor(
        controller.last_event
    )


    # Menjalankan kontrol manual.
    while True:

        # Membaca command.
        command = input(
            "control> "
        ).strip().lower()


        # Keluar dari program.
        if command == "q":

            break


        # Menggerakkan base ke depan.
        if command == "w":

            event = controller.step(
                action="MoveAgent",
                ahead=BASE_STEP,
                right=0.0,
            )


        # Menggerakkan base ke belakang.
        elif command == "s":

            event = controller.step(
                action="MoveAgent",
                ahead=-BASE_STEP,
                right=0.0,
            )


        # Memutar robot ke kiri.
        elif command == "a":

            event = controller.step(
                action="RotateAgent",
                degrees=-ROTATE_STEP,
            )


        # Memutar robot ke kanan.
        elif command == "d":

            event = controller.step(
                action="RotateAgent",
                degrees=ROTATE_STEP,
            )


        # Menggerakkan arm ke kiri.
        elif command == "j":

            event = controller.step(
                action="MoveArm",
                position={
                    "x": -ARM_STEP,
                    "y": 0.0,
                    "z": 0.0,
                },
                coordinateSpace="wrist",
                restrictMovement=True,
            )


        # Menggerakkan arm ke kanan.
        elif command == "l":

            event = controller.step(
                action="MoveArm",
                position={
                    "x": ARM_STEP,
                    "y": 0.0,
                    "z": 0.0,
                },
                coordinateSpace="wrist",
                restrictMovement=True,
            )


        # Menggerakkan arm ke atas.
        elif command == "u":

            event = controller.step(
                action="MoveArm",
                position={
                    "x": 0.0,
                    "y": ARM_STEP,
                    "z": 0.0,
                },
                coordinateSpace="wrist",
                restrictMovement=True,
            )


        # Menggerakkan arm ke bawah.
        elif command == "o":

            event = controller.step(
                action="MoveArm",
                position={
                    "x": 0.0,
                    "y": -ARM_STEP,
                    "z": 0.0,
                },
                coordinateSpace="wrist",
                restrictMovement=True,
            )


        # Menggerakkan arm ke depan.
        elif command == "i":

            event = controller.step(
                action="MoveArm",
                position={
                    "x": 0.0,
                    "y": 0.0,
                    "z": ARM_STEP,
                },
                coordinateSpace="wrist",
                restrictMovement=True,
            )


        # Menggerakkan arm ke belakang.
        elif command == "k":

            event = controller.step(
                action="MoveArm",
                position={
                    "x": 0.0,
                    "y": 0.0,
                    "z": -ARM_STEP,
                },
                coordinateSpace="wrist",
                restrictMovement=True,
            )


        # Menaikkan arm base.
        elif command == "r":

            arm_base_height = min(
                1.0,
                arm_base_height + 0.05
            )

            event = controller.step(
                action="MoveArmBase",
                y=arm_base_height,
            )


        # Menurunkan arm base.
        elif command == "f":

            arm_base_height = max(
                0.0,
                arm_base_height - 0.05
            )

            event = controller.step(
                action="MoveArmBase",
                y=arm_base_height,
            )


        # Mengambil object.
        elif command == "p":

            event = controller.step(
                action="PickupObject",
            )


        # Melepaskan object.
        elif command == "x":

            event = controller.step(
                action="ReleaseObject",
            )


        # Menampilkan informasi.
        elif command == "info":

            event = controller.last_event

            print(
                "Held objects:",
                event.metadata[
                    "arm"
                ][
                    "heldObjects"
                ]
            )

            print(
                "Pickupable near hand:",
                event.metadata[
                    "arm"
                ][
                    "pickupableObjects"
                ]
            )

            print(
                "Hand sphere:",
                event.metadata[
                    "arm"
                ][
                    "handSphereCenter"
                ]
            )


        # Menangani command yang tidak dikenal.
        else:

            print(
                "Unknown command."
            )

            continue


        # Menampilkan status action.
        print(
            "Success:",
            event.metadata[
                "lastActionSuccess"
            ],
            "|",
            event.metadata.get(
                "errorMessage",
                ""
            ),
        )


        # Memperbarui live view.
        show_monitor(
            event
        )


# Menutup simulator dengan aman.
finally:

    # Menutup window OpenCV.
    cv2.destroyAllWindows()

    # Menutup Unity process.
    controller.stop()
