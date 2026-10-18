# Bonus Hands-on Navigation: Dynamic Obstacle

Demo ini memperluas contoh **reactive navigation** dengan menambahkan obstacle yang bergerak.

Berbeda dengan navigation sebelumnya yang hanya memiliki obstacle statis, pada demo ini robot harus terus memperbarui arah geraknya berdasarkan kondisi lingkungan yang berubah.

Robot mempertimbangkan:

```text
Goal Position
Static Obstacles
Dynamic Obstacle Position
```

Secara sederhana:

```text
Current Robot Position
        ↓
Goal Direction
        +
Static Obstacles
        +
Dynamic Obstacle
        ↓
Reactive Navigation
        ↓
Updated Robot Motion
```

---

## File

```text
Navigation/
├── dynamic_navigation.py
├── requirements.txt
├── README.md
└── results/
    ├── dynamic_navigation_result.png
    └── dynamic_navigation.gif
```

Folder `results/` akan dibuat otomatis ketika script dijalankan.

---

## Instalasi

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

---

## Menjalankan

Jalankan demo:

```bash
python dynamic_navigation.py
```

---

## Apa yang Dilakukan Script?

Robot bergerak dari posisi awal menuju goal sambil menghindari:

```text
Static Obstacle
Dynamic Obstacle
```

Dynamic obstacle bergerak naik dan turun secara vertikal.

Pada setiap simulation step, urutannya adalah:

```text
Dynamic obstacle bergerak
        ↓
Robot membaca posisi obstacle terbaru
        ↓
Attractive force dihitung
        ↓
Repulsive force dihitung
        ↓
Navigation vector diperbarui
        ↓
Robot bergerak
```

Dengan demikian, arah gerak robot tidak hanya ditentukan sekali di awal.

Robot terus melakukan **reactive update** berdasarkan posisi obstacle yang berubah.

---

## Dynamic Obstacle

Dynamic obstacle memiliki:

```text
Position
Velocity
Radius
```

Pada awal simulasi, obstacle bergerak ke satu arah.

Ketika mencapai batas tertentu, arah velocity dibalik sehingga obstacle bergerak kembali ke arah sebaliknya.

Secara konseptual:

```text
↑
│ Dynamic obstacle
│
│ bergerak naik
│
↓ batas atas

kemudian:

↓
│ Dynamic obstacle
│
│ bergerak turun
│
↑ batas bawah
```

Gerakan seperti ini menciptakan lingkungan yang berubah selama robot melakukan navigation.

---

## Reactive Navigation

Robot tetap menggunakan dua komponen utama:

```text
Attractive Force
       +
Repulsive Force
```

**Attractive force** menarik robot menuju goal.

**Repulsive force** mendorong robot menjauhi obstacle.

Perbedaannya adalah repulsive force sekarang dihitung menggunakan posisi dynamic obstacle terbaru pada setiap step.

Karena itu, trajectory robot dapat berubah ketika obstacle bergerak mendekati jalur robot.

Secara sederhana:

```text
Robot
  ↓
Goal tetap
  ↓
Obstacle berubah posisi
  ↓
Navigation vector berubah
  ↓
Robot menyesuaikan arah
```

Inilah ide dasar dari **reactive navigation**.

---

## Collision Check

Sebelum robot berpindah ke posisi berikutnya, script memeriksa apakah posisi tersebut akan bertabrakan dengan:

```text
Static Obstacles
Dynamic Obstacle
```

Collision diperiksa berdasarkan jarak antara pusat robot dan pusat obstacle.

Jika posisi berikutnya tidak aman, script mencoba beberapa arah alternatif.

Contohnya:

```text
+20°
-20°
+40°
-40°
+60°
-60°
...
```

Dari kandidat yang aman, dipilih posisi yang paling dekat dengan goal.

---

## Output Terminal

Selama simulasi, terminal akan menampilkan:

```text
Robot Position
Dynamic Obstacle Position
Distance to Goal
```

Contohnya:

```text
Step 001 | Robot: (1.00, 1.00) | Dynamic obstacle: (5.00, 1.55) | Goal distance: ...
Step 002 | Robot: (...)        | Dynamic obstacle: (...)        | Goal distance: ...
...
```

Jika robot berhasil mencapai goal, terminal akan menampilkan:

```text
Goal reached!
```

---

## Hasil 1 — `dynamic_navigation_result.png`

Visualisasi statis disimpan ke:

```text
results/dynamic_navigation_result.png
```

Gambar ini memperlihatkan keseluruhan hasil simulasi setelah navigation selesai.

Elemen utamanya adalah:

```text
Start
Goal
Static Obstacles
Dynamic Obstacle Path
Robot Trajectory
```

**Start** menunjukkan posisi awal robot.

**Goal** menunjukkan posisi tujuan.

**Static obstacles** ditampilkan sebagai lingkaran yang tidak bergerak.

**Dynamic Obstacle Path** menunjukkan lintasan yang ditempuh obstacle selama simulasi.

**Robot Trajectory** menunjukkan jalur robot dari start menuju goal.

Hal penting yang perlu diperhatikan adalah bahwa trajectory robot dapat membelok sebelum mencapai obstacle karena robot terus menghitung repulsive force berdasarkan posisi obstacle saat itu.

Dengan demikian, gambar statis membantu kita melihat hubungan antara:

```text
Robot Path
vs.
Dynamic Obstacle Path
```

Kita dapat melihat apakah robot berhasil menjaga jarak dari obstacle sambil tetap bergerak menuju goal.

---

## Hasil 2 — `dynamic_navigation.gif`

Animasi disimpan ke:

```text
results/dynamic_navigation.gif
```

GIF ini memberikan informasi yang tidak terlihat pada gambar statis.

Pada animasi, kita dapat melihat:

```text
Robot bergerak
Dynamic obstacle bergerak
Trajectory robot bertambah
Robot menyesuaikan arah
```

Setiap frame menunjukkan kondisi environment pada satu waktu tertentu.

Secara konseptual:

```text
Frame 1
Robot + Obstacle Position
        ↓
Frame 2
Robot bergerak + Obstacle bergerak
        ↓
Frame 3
Robot menyesuaikan trajectory
        ↓
...
```

GIF sangat penting pada demo ini karena dynamic obstacle memiliki dimensi waktu.

Pada gambar statis, kita hanya melihat lintasan akhirnya.

Pada GIF, kita dapat melihat **kapan** obstacle mendekati robot dan **bagaimana** robot bereaksi terhadap perubahan tersebut.

Hal yang perlu diperhatikan saat melihat animasi:

- dynamic obstacle terus bergerak selama navigation;
- robot tidak menggunakan trajectory yang sepenuhnya tetap;
- arah robot dapat berubah ketika obstacle mendekati jalurnya;
- robot tetap mencoba bergerak menuju goal setelah menghindari obstacle.

---

## Perbedaan dengan Navigation Sebelumnya

Pada navigation dengan obstacle statis:

```text
Environment
    ↓
Tidak berubah
    ↓
Robot menghindari obstacle tetap
```

Pada dynamic navigation:

```text
Environment
    ↓
Berubah setiap step
    ↓
Robot harus terus memperbarui keputusan
```

Perbedaan ini penting dalam Embodied AI karena lingkungan dunia nyata hampir selalu bersifat dinamis.

Manusia, robot lain, kendaraan, atau object yang bergerak dapat mengubah kondisi environment selama robot sedang menjalankan task.

---

## Keterbatasan Demo

Demo ini masih merupakan simulasi sederhana.

Dynamic obstacle hanya bergerak menggunakan velocity yang sudah ditentukan, dan robot belum melakukan prediction terhadap posisi obstacle di masa depan.

Robot hanya bereaksi terhadap kondisi saat ini.

Pada sistem yang lebih kompleks, navigation dapat mempertimbangkan:

```text
Obstacle Velocity
Future Position Prediction
Trajectory Planning
Time-to-Collision
Multi-Agent Interaction
```

Namun untuk hands-on pengantar, contoh ini cukup untuk memperlihatkan perbedaan antara navigation pada environment statis dan environment dinamis.

---

## Inti Konsep

Hands-on ini menunjukkan pola dasar reactive navigation:

```text
Observe Current Environment
          ↓
Update Obstacle Position
          ↓
Compute Navigation Direction
          ↓
Move Robot
          ↓
Observe Again
```

Robot tidak hanya menjalankan trajectory yang sudah ditentukan sebelumnya.

Robot terus mengamati perubahan environment dan menyesuaikan gerakannya berdasarkan kondisi terbaru.
