# Hands-on Perception

Folder ini berisi contoh sederhana **robot perception menggunakan object detection** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Hands-on ini menggunakan model pretrained **YOLO11n** untuk mendeteksi object dari dua sumber input:

```text
Image
  ↓
YOLO
  ↓
Object Detection
  ↓
Bounding Box + Class + Confidence
```

dan:

```text
Webcam
  ↓
YOLO
  ↓
Real-Time Object Detection
```

---

## File

```text
Perception/
├── perception_image_demo.py
├── perception_camera_demo.py
├── table.jpg
├── requirements.txt
├── README.md
└── results/
    ├── perception_image_result.jpg
    └── perception_camera_result.jpg
```

Folder `results/` akan dibuat otomatis ketika script dijalankan.

---

## Menjalankan

Pastikan environment Python sudah aktif dan dependency sudah terpasang:

```bash
pip install -r requirements.txt
```

---

## 1. Object Detection dari Image

Letakkan sebuah image bernama:

```text
table.jpg
```

di folder yang sama dengan script.

Kemudian jalankan:

```bash
python perception_image_demo.py
```

Script akan:

```text
Membaca image
    ↓
Menampilkan informasi dasar image
    ↓
Menjalankan YOLO11n
    ↓
Mendeteksi object
    ↓
Menampilkan class, confidence, dan bounding box
    ↓
Menyimpan hasil visualisasi
```

Terminal akan menampilkan informasi seperti:

```text
=== Informasi Gambar ===
Image shape     : ...
Image data type : ...
Pixel BGR [...] : ...

=== Hasil Object Detection ===
Object: bottle       | Confidence: 0.87 | Bounding Box: [...]
Object: cup          | Confidence: 0.73 | Bounding Box: [...]
```

`Image shape` menunjukkan dimensi image, sedangkan `Image data type` menunjukkan tipe data pixel yang digunakan oleh OpenCV.

Nilai pixel ditampilkan dalam format:

```text
BGR
```

karena OpenCV menggunakan urutan channel **Blue, Green, Red**.

---

## Hasil — `perception_image_result.jpg`

Hasil object detection disimpan ke:

```text
results/perception_image_result.jpg
```

Gambar ini merupakan image asli yang sudah diberi anotasi hasil YOLO.

Setiap object yang terdeteksi akan ditandai menggunakan:

```text
Bounding Box
Class Name
Confidence Score
```

Contohnya:

```text
┌───────────────────────┐
│ bottle 0.87           │
│                       │
│       object          │
│                       │
└───────────────────────┘
```

**Bounding box** menunjukkan lokasi object pada image.

**Class name** menunjukkan kategori object yang diprediksi oleh model.

**Confidence score** menunjukkan tingkat keyakinan model terhadap prediksi tersebut.

Semakin tinggi confidence, semakin yakin model bahwa object yang berada di dalam bounding box termasuk ke dalam class tersebut.

Contoh ini menunjukkan bentuk perception yang sangat umum pada robot:

```text
Camera Image
     ↓
Visual Model
     ↓
Object Detected
     ↓
Location + Semantic Class
```

---

## 2. Real-Time Object Detection dari Webcam

Jalankan:

```bash
python perception_camera_demo.py
```

Script membuka webcam dan menjalankan YOLO pada setiap frame secara real-time.

Alurnya:

```text
Webcam Frame
     ↓
YOLO11n
     ↓
Object Detection
     ↓
Annotated Frame
     ↓
Display
```

Secara default:

```python
CAMERA_INDEX = 0
```

Jika webcam tidak dapat dibuka, coba ubah menjadi:

```python
CAMERA_INDEX = 1
```

atau index lain yang sesuai dengan camera device yang tersedia.

Untuk keluar dari program, tekan:

```text
q
```

---

## Target Object

Pada script webcam terdapat:

```python
TARGET_OBJECT = "bottle"
```

Jika `bottle` terdeteksi, frame akan diberi informasi tambahan:

```text
Target detected: bottle
```

Bagian ini menunjukkan bahwa hasil perception dapat digunakan sebagai kondisi sederhana untuk menentukan apakah object tertentu sedang terlihat oleh robot.

Secara konseptual:

```text
Camera
  ↓
Object Detection
  ↓
Is bottle detected?
  ↓
Yes / No
```

---

## Hasil — `perception_camera_result.jpg`

Ketika program dihentikan dengan tombol `q`, frame terakhir akan disimpan ke:

```text
results/perception_camera_result.jpg
```

Gambar tersebut berisi frame webcam terakhir beserta bounding box dan label object yang terdeteksi.

Jika target `bottle` terlihat pada frame tersebut, tulisan:

```text
Target detected: bottle
```

juga akan tersimpan pada hasil image.

Dengan demikian, kedua demo menghasilkan output visual yang dapat dibandingkan:

```text
Static Image
→ results/perception_image_result.jpg

Webcam
→ results/perception_camera_result.jpg
```

---

## Inti Konsep

Hands-on ini menunjukkan bahwa perception mengubah data visual menjadi informasi yang lebih bermakna bagi robot.

```text
Pixels
  ↓
Visual Perception
  ↓
Object Class
  ↓
Object Location
  ↓
Information for Robot Decision
```

Robot tidak cukup hanya menerima image dari camera. Sistem perception perlu menginterpretasikan image tersebut agar robot dapat mengetahui **object apa yang terlihat dan di mana object tersebut berada**.
