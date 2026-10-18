# Bonus Hands-on Mapping: Depth Image ke Point Cloud 3D

Demo sederhana untuk memahami bagaimana **depth image** dapat diubah menjadi **point cloud 3D** menggunakan model kamera pinhole.

Pada contoh ini, kita tidak menggunakan kamera depth sungguhan. Script membuat depth image sintetis terlebih dahulu, kemudian setiap pixel depth diproyeksikan menjadi titik 3D.

Secara sederhana:

```text
Depth Image
    ↓
Camera Intrinsic
    ↓
Depth-to-3D Projection
    ↓
Point Cloud 3D
```

---

## File

```text
Bonus/
├── depth_pointcloud_demo.py
├── requirements.txt
├── README.md
└── results/
    ├── depth_image.png
    └── point_cloud.png
```

Folder `results/` akan dibuat otomatis ketika script dijalankan.

---

## Menjalankan

Buat dan aktifkan virtual environment:

```bash
python -m venv embodied-ai
source embodied-ai/bin/activate
```

Untuk Windows:

```bash
embodied-ai\Scripts\activate
```

Kemudian install dependency:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jalankan demo:

```bash
python depth_pointcloud_demo.py
```

---

## Apa yang Dilakukan Script?

Script melakukan tiga tahap utama.

### 1. Membuat Depth Image Sintetis

Depth image adalah image yang setiap pixel-nya menyimpan **jarak dari kamera ke permukaan object**, bukan warna RGB.

Pada demo ini, background ditempatkan pada jarak:

```text
4.0 meter
```

Kemudian dibuat tiga area yang mewakili object pada jarak berbeda:

```text
Object 1 → 2.0 meter
Object 2 → 2.7 meter
Object 3 → 3.2 meter
Background → 4.0 meter
```

Karena nilai depth berbeda, kita dapat membedakan object yang lebih dekat dan lebih jauh dari kamera.

Script juga menampilkan informasi dasar seperti:

```text
Depth image shape
Minimum depth
Maximum depth
```

---

### 2. Mengubah Depth Menjadi Titik 3D

Setiap pixel pada depth image memiliki koordinat image:

```text
(u, v)
```

dan nilai depth:

```text
z
```

Dengan camera intrinsic sederhana:

```text
fx, fy
cx, cy
```

koordinat tersebut diproyeksikan menjadi posisi 3D:

```text
x = (u - cx) × z / fx
y = (v - cy) × z / fy
z = depth
```

Hasil akhirnya berupa kumpulan titik:

```text
[x, y, z]
```

yang membentuk **point cloud 3D**.

Untuk menjaga visualisasi tetap ringan, script menggunakan `stride=2`, sehingga tidak semua pixel depth diubah menjadi titik 3D.

---

## Hasil 1 — `depth_image.png`

File pertama disimpan ke:

```text
results/depth_image.png
```

Gambar ini menunjukkan depth image sintetis yang digunakan sebagai input.

Visualisasinya terdiri dari beberapa bidang dengan nilai depth yang berbeda. Area yang mewakili object memiliki jarak lebih kecil daripada background.

Secara konseptual:

```text
Kamera
  ↓

Object dekat        → 2.0 m
Object sedang       → 2.7 m
Object lebih jauh   → 3.2 m
Background          → 4.0 m
```

Pada gambar, perbedaan intensitas grayscale merepresentasikan **perbedaan nilai depth**, bukan warna asli object.

Colorbar di samping gambar menunjukkan hubungan antara intensitas visual dan jarak dalam meter.

Hal penting yang perlu diperhatikan adalah:

- pixel dengan nilai depth lebih kecil merepresentasikan permukaan yang lebih dekat ke kamera;
- pixel dengan nilai depth lebih besar merepresentasikan permukaan yang lebih jauh;
- bentuk persegi pada depth image akan menjadi sekumpulan titik 3D setelah proses proyeksi.

Gambar ini membantu kita memahami bahwa depth camera menghasilkan struktur data 2D seperti image biasa, tetapi isi setiap pixel adalah informasi jarak.

---

## Hasil 2 — `point_cloud.png`

File kedua disimpan ke:

```text
results/point_cloud.png
```

Gambar ini merupakan visualisasi **3D point cloud** yang dihasilkan dari depth image.

Setiap titik pada plot berasal dari satu pixel depth yang telah diproyeksikan ke koordinat 3D.

Sumbu plot merepresentasikan:

```text
X → posisi horizontal terhadap kamera
Y → depth atau jarak dari kamera
Z → posisi vertikal terhadap kamera
```

Pada script, depth ditampilkan pada sumbu `Y` plot agar struktur point cloud lebih mudah diamati.

Hasilnya akan terlihat seperti beberapa bidang titik pada jarak berbeda:

```text
Camera
  ↓

Point cloud object 1     sekitar 2.0 m
Point cloud object 2     sekitar 2.7 m
Point cloud object 3     sekitar 3.2 m
Background points        sekitar 4.0 m
```

Object yang pada depth image hanya terlihat sebagai area 2D sekarang memiliki posisi di ruang 3D.

Semakin jauh nilai depth suatu pixel, semakin jauh pula posisi titik tersebut dari kamera pada point cloud.

Dengan kata lain:

```text
Depth Image
    ↓
Setiap pixel memiliki jarak
    ↓
Pixel diproyeksikan ke ruang 3D
    ↓
Point Cloud
```

Demo ini menunjukkan prinsip dasar yang juga digunakan pada berbagai sistem robot untuk mengubah data depth camera menjadi representasi geometris lingkungan.

---

## Output

Setelah script selesai dijalankan, struktur hasilnya menjadi:

```text
results/
├── depth_image.png
└── point_cloud.png
```

Terminal juga akan menampilkan informasi seperti:

```text
Depth image shape: (120, 160)
Minimum depth: 2.0 meter
Maximum depth: 4.0 meter
Number of 3D points: ...
```

Jumlah titik 3D bergantung pada ukuran depth image dan nilai `stride` yang digunakan saat melakukan proyeksi.

---

## Inti Konsep

Hands-on ini memperlihatkan hubungan sederhana antara perception dan mapping:

```text
Depth Sensor
    ↓
Depth Image
    ↓
3D Geometry
    ↓
Point Cloud
    ↓
Representasi Lingkungan
```

Point cloud seperti ini dapat menjadi salah satu representasi awal yang digunakan robot untuk memahami bentuk dan jarak object di sekitarnya.
