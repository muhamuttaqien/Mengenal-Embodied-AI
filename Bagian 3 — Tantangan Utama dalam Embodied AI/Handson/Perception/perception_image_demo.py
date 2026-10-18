# Import YOLO untuk object detection.
from ultralytics import YOLO

# Import OpenCV untuk membaca dan menampilkan gambar.
import cv2

# Import Path untuk mengatur path file.
from pathlib import Path


# Menentukan model YOLO.
MODEL_NAME = "yolo11n.pt"


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent


# Menentukan gambar input.
IMAGE_PATH = BASE_DIR / "table.jpg"


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
    / "perception_image_result.jpg"
)


def main():

    # Memuat model YOLO.
    model = YOLO(
        MODEL_NAME
    )


    # Memastikan gambar tersedia.
    if not IMAGE_PATH.exists():

        raise FileNotFoundError(
            f"Gambar '{IMAGE_PATH.name}' tidak ditemukan.\n"
            "Letakkan file gambar bernama 'table.jpg' "
            "di folder yang sama dengan script."
        )


    # Membaca gambar.
    image = cv2.imread(
        str(IMAGE_PATH)
    )


    # Memastikan gambar berhasil dibaca.
    if image is None:

        raise RuntimeError(
            f"Gagal membaca gambar: {IMAGE_PATH}"
        )


    # Menampilkan informasi gambar.
    print(
        "=== Informasi Gambar ==="
    )

    print(
        "Image shape     :",
        image.shape,
    )

    print(
        "Image data type :",
        image.dtype,
    )


    # Mengambil ukuran gambar.
    h, w = image.shape[:2]


    # Menentukan contoh pixel.
    sample_y = min(
        100,
        h - 1,
    )

    sample_x = min(
        100,
        w - 1,
    )


    # Menampilkan nilai pixel.
    print(
        f"Pixel BGR [{sample_y}, {sample_x}] :",
        image[
            sample_y,
            sample_x,
        ],
    )


    # Menjalankan object detection.
    results = model(
        image,
        verbose=False,
    )

    result = results[0]


    # Menampilkan hasil detection.
    print(
        "\n=== Hasil Object Detection ==="
    )


    # Memeriksa apakah ada object.
    if len(result.boxes) == 0:

        print(
            "Tidak ada objek yang terdeteksi."
        )


    else:

        # Membaca setiap hasil detection.
        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )

            x1, y1, x2, y2 = (
                box.xyxy[0].tolist()
            )

            class_name = (
                model.names[class_id]
            )


            # Menampilkan informasi object.
            print(
                f"Object: {class_name:<12} | "
                f"Confidence: {confidence:.2f} | "
                f"Bounding Box: "
                f"[{x1:.0f}, {y1:.0f}, "
                f"{x2:.0f}, {y2:.0f}]"
            )


    # Membuat visualisasi hasil detection.
    annotated_image = (
        result.plot()
    )


    # Menyimpan hasil detection.
    cv2.imwrite(
        str(OUTPUT_PATH),
        annotated_image,
    )


    print(
        "\nHasil visualisasi disimpan ke:",
        OUTPUT_PATH,
    )


    # Menampilkan hasil detection.
    cv2.imshow(
        "Object Detection",
        annotated_image,
    )


    print(
        "Tekan tombol apa pun pada "
        "jendela gambar untuk keluar."
    )


    # Menunggu input keyboard.
    cv2.waitKey(0)


    # Menutup window.
    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()
