# Hands-on Localization

Folder ini berisi contoh sederhana **localization 2D** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Tujuannya adalah memahami perbedaan antara **ground-truth pose** dan **estimated pose** ketika robot hanya mengandalkan odometry yang mengandung noise.

Secara sederhana:

```text
Robot Motion
    ↓
Ground-Truth Pose
    ↓
Noisy Odometry
    ↓
Estimated Pose
```

---

## File

```text
Localization/
├── localization_demo.py
├── requirements.txt
├── README.md
└── results/
    └── localization_result.png
```

`localization_demo.py` mensimulasikan pergerakan robot 2D dan membandingkan posisi sebenarnya dengan posisi hasil estimasi.

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
python localization_demo.py
```

---

## Apa yang Dilakukan Script?

Robot direpresentasikan menggunakan pose:

```text
[x, y, yaw]
```

dengan:

```text
x   → posisi horizontal
y   → posisi vertikal
yaw → orientasi robot
```

Script menyimpan dua pose secara bersamaan:

```text
Ground-Truth Pose
Estimated Pose
```

**Ground-truth pose** dianggap sebagai posisi robot yang sebenarnya.

Sementara itu, **estimated pose** dihitung dari odometry yang diberi noise.

---

## Gerakan Robot

Robot menjalankan beberapa aksi sederhana:

```text
forward
rotate_left
rotate_right
```

Gerakan maju mengubah posisi berdasarkan orientasi robot saat itu.

Secara sederhana:

```text
x_new = x + distance × cos(yaw)
y_new = y + distance × sin(yaw)
```

Sementara itu, aksi rotasi mengubah nilai `yaw`.

Urutan beberapa gerakan tersebut membentuk trajectory robot di bidang 2D.

---

## Noise pada Odometry

Pada sistem nyata, odometry tidak pernah benar-benar sempurna.

Pergerakan roda, slip, ketidakakuratan sensor, dan berbagai faktor lain dapat menyebabkan estimasi pose sedikit berbeda dari posisi sebenarnya.

Pada demo ini, noise ditambahkan pada:

```text
Forward distance
Rotation angle
```

Contohnya:

```text
Ground truth movement
      ↓
Add small random noise
      ↓
Estimated movement
```

Karena noise terus terakumulasi selama robot bergerak, trajectory hasil estimasi perlahan dapat menyimpang dari ground truth.

Konsep ini disebut **odometry drift**.

---

## Output Terminal

Setelah simulasi selesai, terminal akan menampilkan pose akhir robot.

Contohnya:

```text
Ground Truth Pose
x   : ...
y   : ...
yaw : ... degree

Estimated Pose
x   : ...
y   : ...
yaw : ... degree
```

Perbedaan antara kedua nilai tersebut menunjukkan error localization yang muncul akibat noise pada odometry.

---

## Hasil — `localization_result.png`

Hasil visualisasi disimpan ke:

```text
results/localization_result.png
```

Gambar ini menampilkan dua trajectory:

```text
Ground Truth
Estimated Position
```

Trajectory **Ground Truth** menunjukkan jalur yang benar-benar dijalani robot pada simulasi.

Trajectory **Estimated Position** menunjukkan jalur yang diperkirakan berdasarkan noisy odometry.

Pada awal gerakan, kedua trajectory biasanya masih sangat berdekatan.

Namun setelah beberapa gerakan maju dan rotasi, perbedaan kecil pada odometry mulai terakumulasi sehingga trajectory estimasi dapat bergeser dari trajectory sebenarnya.

Secara konseptual:

```text
Start
  ↓
Ground Truth ───────────────→
       \
        \ sedikit menyimpang
         \
          ───────────────→ Estimated
```

Panah pada titik akhir menunjukkan orientasi robot.

Dengan demikian, gambar tidak hanya memperlihatkan error pada posisi:

```text
x, y
```

tetapi juga membantu membandingkan orientasi akhir:

```text
yaw
```

Hal penting yang perlu diperhatikan adalah bahwa localization tidak selalu berarti robot mengetahui posisinya secara sempurna.

Dalam praktiknya, robot biasanya hanya memiliki **estimasi pose** yang diperbarui berdasarkan sensor dan model gerak.

---

## Mengapa Hasil Bisa Berbeda Setiap Kali?

Noise pada odometry dibuat menggunakan random sampling.

Karena itu, trajectory `Estimated Position` dapat sedikit berbeda setiap kali script dijalankan.

Ground-truth trajectory tetap sama, tetapi estimated trajectory dapat berubah karena nilai noise yang berbeda.

Ini membantu menunjukkan bahwa error sensor bersifat tidak pasti dan dapat menghasilkan estimasi pose yang berbeda.

---

## Inti Konsep

Hands-on ini memperlihatkan masalah dasar localization:

```text
Robot bergerak
    ↓
Sensor / Odometry
    ↓
Pose Estimation
    ↓
Estimated Robot State
```

Jika hanya mengandalkan odometry, error kecil dapat terakumulasi menjadi drift.

Pada sistem robot yang lebih kompleks, odometry biasanya dikombinasikan dengan sensor lain seperti camera, LiDAR, IMU, atau landmark observation untuk menghasilkan estimasi pose yang lebih akurat.
