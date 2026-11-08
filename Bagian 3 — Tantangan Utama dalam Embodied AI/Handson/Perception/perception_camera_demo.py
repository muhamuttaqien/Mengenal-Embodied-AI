# Import YOLO untuk object detection.
from ultralytics import YOLO

# Import OpenCV untuk mengakses camera.
import cv2

# Import Path untuk mengatur path file.
from pathlib import Path


# Menentukan model YOLO yang akan diunduh otomatis jika belum tersedia.
MODEL_NAME = "yolo11n.pt"

# Menentukan confidence threshold.
CONFIDENCE_THRESHOLD = 0.50

# Menentukan camera yang digunakan.
CAMERA_INDEX = 0

# Menentukan target object.
TARGET_OBJECT = "bottle"

# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent

# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"

# Membuat folder results jika belum ada.
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# Menentukan file hasil.
OUTPUT_PATH = (
    RESULTS_DIR
    / "perception_camera_result.jpg"
)


# Memuat model YOLO.
model = YOLO(
    MODEL_NAME
)


# Membuka camera.
camera = cv2.VideoCapture(
    CAMERA_INDEX
)


# Memastikan camera berhasil dibuka.
if not camera.isOpened():

    camera.release()

    raise RuntimeError(
        "Camera tidak dapat dibuka. "
        "Coba ganti CAMERA_INDEX menjadi 1 "
        "atau device kamera lain."
    )


print(
    "Camera aktif."
)

print(
    "Tekan 'q' untuk keluar.\n"
)


# Menyimpan frame terakhir.
last_annotated_frame = None


try:

    # Menjalankan camera loop.
    while True:

        # Membaca frame camera.
        ret, frame = camera.read()


        # Memeriksa frame.
        if not ret:

            print(
                "Gagal membaca frame dari camera."
            )

            break


        # Menjalankan object detection dengan confidence threshold yang sama.
        results = model(
            frame,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False,
        )

        result = results[0]


        # Menyimpan daftar object yang melewati confidence threshold.
        detected_objects = []


        # Membaca setiap hasil detection.
        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )

            class_name = (
                model.names[class_id]
            )

            confidence = float(
                box.conf[0]
            )


            detected_objects.append(
                class_name
            )


            print(
                f"Detected: {class_name:<12} "
                f"confidence={confidence:.2f}"
            )


        # Membuat visualisasi detection.
        annotated_frame = (
            result.plot()
        )


        # Memberikan indikator target object.
        if TARGET_OBJECT in detected_objects:

            cv2.putText(
                annotated_frame,
                f"Target detected: {TARGET_OBJECT}",
                (
                    20,
                    35,
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (
                    0,
                    255,
                    0,
                ),
                2,
                cv2.LINE_AA,
            )


        # Menyimpan frame terakhir.
        last_annotated_frame = (
            annotated_frame.copy()
        )


        # Menampilkan camera.
        cv2.imshow(
            "Robot Perception - YOLO",
            annotated_frame,
        )


        # Keluar jika tombol q ditekan.
        if (
            cv2.waitKey(1)
            & 0xFF
            == ord("q")
        ):

            break


finally:

    # Menyimpan frame terakhir jika tersedia.
    if last_annotated_frame is not None:

        cv2.imwrite(
            str(OUTPUT_PATH),
            last_annotated_frame,
        )

        print(
            "\nHasil visualisasi disimpan ke:",
            OUTPUT_PATH,
        )


    # Melepaskan camera.
    camera.release()


    # Menutup window.
    cv2.destroyAllWindows()
