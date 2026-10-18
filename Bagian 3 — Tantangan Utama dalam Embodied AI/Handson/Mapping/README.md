# Hands-on Mapping

Folder ini berisi contoh sederhana **occupancy grid mapping 2D** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Tujuannya adalah memahami bagaimana robot dapat membangun representasi lingkungan dari hasil pengamatan sensor.

Secara sederhana:

```text
Robot Position
      ↓
Simulated LiDAR
      ↓
Free / Occupied Cells
      ↓
Occupancy Grid Update
      ↓
2D Map
```

---

## File

```text
Mapping/
├── mapping_demo.py
├── requirements.txt
├── README.md
├── results/
│   └── mapping_result.png
└── Bonus/
    └── ...
```

`mapping_demo.py` menjalankan simulasi mapping menggunakan sensor LiDAR sederhana.

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
python mapping_demo.py
```

---

## Apa yang Dilakukan Script?

Script membuat sebuah **ground-truth environment** berbentuk grid 2D.

Setiap cell memiliki dua kemungkinan kondisi:

```text
0 → free space
1 → obstacle
```

Ground-truth environment hanya digunakan oleh simulator untuk menentukan apakah sinar LiDAR mengenai obstacle. Robot tidak membaca map ini secara langsung.

Robot justru memulai dengan occupancy map yang seluruh cell-nya masih:

```text
UNKNOWN
```

Kemudian robot bergerak mengikuti trajectory yang sudah ditentukan.

Pada setiap posisi, simulated LiDAR melakukan scan 360 derajat untuk mengamati lingkungan.

---

## Simulated LiDAR

Sensor LiDAR sederhana dibuat menggunakan beberapa ray yang dipancarkan dari posisi robot.

Parameter utamanya:

```text
NUM_RAYS  = 72
MAX_RANGE = 10.0
RAY_STEP  = 0.2
```

Artinya, pada setiap posisi robot terdapat 72 sinar yang tersebar mengelilingi robot.

Setiap ray bergerak menjauhi robot hingga:

- mengenai obstacle;
- mencapai jarak maksimum; atau
- keluar dari area map.

Cell yang dilewati sebelum obstacle dianggap **free**, sedangkan cell pertama yang mengenai obstacle dianggap **occupied**.

Secara konseptual:

```text
Robot
  ↓
LiDAR Ray
  ↓
Free Cell
  ↓
Free Cell
  ↓
Obstacle
```

Informasi dari seluruh ray kemudian digunakan untuk memperbarui occupancy map.

---

## Occupancy Grid

Map robot menggunakan tiga nilai:

```text
UNKNOWN  = -1
FREE     =  0
OCCUPIED =  1
```

Pada awal simulasi, hampir seluruh map berstatus `UNKNOWN`.

Semakin banyak posisi yang dikunjungi robot, semakin banyak area yang dapat diamati oleh LiDAR dan dimasukkan ke dalam map.

Dengan demikian, mapping terjadi secara bertahap:

```text
Unknown Map
    ↓
Robot bergerak
    ↓
LiDAR mengamati lingkungan
    ↓
Map diperbarui
    ↓
Lebih banyak area diketahui
```

---

## Hasil — `mapping_result.png`

Hasil visualisasi disimpan ke:

```text
results/mapping_result.png
```

Gambar ini menunjukkan occupancy grid yang berhasil dibangun berdasarkan seluruh pengamatan LiDAR selama robot bergerak.

Representasi warnanya adalah:

```text
Abu-abu → Unknown
Putih    → Free
Hitam    → Occupied
```

Area **abu-abu** menunjukkan bagian lingkungan yang belum cukup teramati oleh sensor.

Area **putih** menunjukkan cell yang telah dilalui ray LiDAR dan tidak berisi obstacle.

Area **hitam** menunjukkan cell tempat ray LiDAR pertama kali mengenai obstacle.

Selain occupancy grid, gambar juga menampilkan trajectory robot.

Trajectory tersebut menunjukkan urutan posisi robot selama proses mapping:

```text
Start
  ↓
Robot bergerak
  ↓
LiDAR scan
  ↓
Map update
  ↓
Posisi berikutnya
  ↓
...
  ↓
End
```

Posisi awal ditandai dengan marker berbentuk kotak, sedangkan posisi akhir ditandai dengan marker berbentuk bintang.

Hal penting yang perlu diperhatikan adalah bahwa map hasil tidak harus identik sempurna dengan ground-truth environment. Robot hanya mengetahui bagian lingkungan yang berhasil diamati oleh sensor sepanjang trajectory-nya.

Inilah ide dasar mapping pada robot:

> robot membangun representasi lingkungan berdasarkan hasil pengamatan sensor, bukan karena map lengkap diberikan sejak awal.

---

## Output Terminal

Selama simulasi, terminal akan menampilkan posisi robot pada setiap langkah, misalnya:

```text
Step 01 | Robot position: (3, 3)
Step 02 | Robot position: (5, 3)
Step 03 | Robot position: (7, 3)
...
```

Setiap step mewakili satu posisi robot tempat LiDAR melakukan pengamatan dan occupancy grid diperbarui.

Setelah proses selesai, visualisasi disimpan ke:

```text
results/mapping_result.png
```

---

## Inti Konsep

Hands-on ini memperlihatkan hubungan dasar antara sensing dan mapping:

```text
Environment
    ↓
LiDAR Observation
    ↓
Free / Occupied Estimation
    ↓
Occupancy Grid
    ↓
Map
```

Pada sistem robot nyata, konsep yang sama dapat dikembangkan lebih jauh dengan sensor sungguhan, probabilistic occupancy mapping, localization, dan SLAM.

---

## Bonus

Folder `Bonus/` berisi hands-on tambahan untuk mengubah **depth image** menjadi **3D point cloud**.

Contoh bonus tersebut menunjukkan bentuk representasi lingkungan lain yang tidak lagi berupa grid 2D, tetapi sekumpulan titik di ruang 3D.
