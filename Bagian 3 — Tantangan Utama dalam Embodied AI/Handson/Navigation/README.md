# Hands-on Navigation

Folder ini berisi demo sederhana **robot navigation dengan obstacle avoidance** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Tujuannya adalah memahami bagaimana robot dapat bergerak dari posisi awal menuju goal sambil menghindari obstacle.

Secara sederhana:

```text
Start
  ↓
Attractive Force menuju Goal
  +
Repulsive Force dari Obstacle
  ↓
Navigation Direction
  ↓
Collision Check
  ↓
Robot Motion
  ↓
Goal
```

---

## File

```text
Navigation/
├── navigation_demo.py
├── requirements.txt
├── README.md
└── results/
    └── navigation_result.png
```

`navigation_demo.py` mensimulasikan pergerakan robot 2D menuju goal menggunakan kombinasi **attractive force**, **repulsive force**, dan pengecekan collision.

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
python navigation_demo.py
```

---

## Apa yang Dilakukan Script?

Robot bergerak pada bidang 2D dari:

```text
START = [2.0, 2.0]
```

menuju:

```text
GOAL = [18.0, 13.0]
```

Di antara start dan goal terdapat beberapa obstacle berbentuk lingkaran.

Setiap obstacle direpresentasikan menggunakan:

```text
(center position, radius)
```

Robot sendiri juga memiliki radius sehingga collision tidak dihitung hanya dari titik pusat robot.

---

## Attractive Force

Agar robot bergerak menuju goal, script menghitung **attractive force**.

Arah attractive force selalu menunjuk dari posisi robot saat ini menuju goal.

Secara sederhana:

```text
Robot
  ↓
Direction to Goal
  ↓
Attractive Force
  ↓
Move toward Goal
```

Semakin robot bergerak, arah menuju goal terus diperbarui berdasarkan posisi terbaru.

---

## Repulsive Force

Jika robot berada cukup dekat dengan obstacle, script menghasilkan **repulsive force**.

Repulsive force mendorong robot menjauhi obstacle.

Secara konseptual:

```text
Obstacle
   ↑
Repulsive Force
   ↑
 Robot
```

Repulsive force hanya aktif jika obstacle berada dalam jarak pengaruh tertentu:

```text
INFLUENCE_DISTANCE
```

Ketika robot jauh dari obstacle, gerakan lebih banyak dipengaruhi oleh attractive force menuju goal.

Ketika robot mendekati obstacle, repulsive force menjadi lebih kuat sehingga arah gerak mulai berubah.

---

## Menggabungkan Keduanya

Arah navigation dihitung dengan menggabungkan:

```text
Attractive Force
       +
Repulsive Force
       ↓
Navigation Vector
```

Vector tersebut kemudian dinormalisasi dan digunakan untuk menentukan posisi robot berikutnya.

Dengan cara ini, robot dapat tetap bergerak menuju goal sambil membelok untuk menghindari obstacle.

---

## Collision Check

Sebelum posisi berikutnya digunakan, script memeriksa apakah robot akan bertabrakan dengan obstacle.

Collision terjadi jika jarak antara pusat robot dan pusat obstacle lebih kecil daripada:

```text
Obstacle Radius + Robot Radius
```

Jika posisi berikutnya berpotensi collision, script mencoba beberapa arah alternatif seperti:

```text
+30°
-30°
+60°
-60°
+90°
-90°
...
```

Dari kandidat yang aman, dipilih posisi yang paling dekat dengan goal.

Secara sederhana:

```text
Proposed Motion
      ↓
Collision?
   ↙      ↘
 No       Yes
 ↓         ↓
Move    Try Alternative Direction
```

---

## Output Terminal

Selama simulasi, terminal menampilkan posisi robot dan jaraknya terhadap goal.

Contohnya:

```text
Step 001 | Position: (2.00, 2.00) | Distance to goal: 19.42 m
Step 002 | Position: (...) | Distance to goal: ... m
Step 003 | Position: (...) | Distance to goal: ... m
...
```

Jika robot berhasil mencapai goal, terminal akan menampilkan:

```text
Goal reached!
```

Robot dianggap mencapai goal ketika jaraknya lebih kecil daripada nilai:

```text
GOAL_THRESHOLD
```

---

## Hasil — `navigation_result.png`

Hasil visualisasi disimpan ke:

```text
results/navigation_result.png
```

Gambar ini menampilkan beberapa elemen utama:

```text
Start
Goal
Obstacles
Robot Trajectory
Final Robot Position
```

**Start** menunjukkan posisi awal robot dan ditandai dengan marker berbentuk kotak.

**Goal** menunjukkan posisi tujuan dan ditandai dengan marker berbentuk bintang.

**Obstacle** ditampilkan sebagai lingkaran abu-abu.

**Robot Trajectory** menunjukkan jalur yang dilewati robot dari start menuju goal.

**Final Robot Position** ditampilkan sebagai lingkaran kosong yang menunjukkan ukuran robot pada posisi akhirnya.

Secara konseptual, visualisasi akan terlihat seperti:

```text
Start
     \____
        \        ○ Obstacle
         \____
              \       ○ Obstacle
               \____
                    \____ Goal
```

Trajectory tidak selalu berupa garis lurus dari start ke goal.

Ketika robot mendekati obstacle, repulsive force akan membelokkan arah geraknya sehingga trajectory menghindari area collision.

Hal yang perlu diperhatikan pada gambar adalah:

- trajectory tetap bergerak menuju goal;
- jalur robot tidak memotong obstacle;
- perubahan arah terjadi terutama ketika robot masuk ke area pengaruh obstacle;
- posisi akhir robot berada sangat dekat dengan goal.

Visualisasi ini menunjukkan ide dasar navigation:

> robot perlu memilih gerakan yang membawa dirinya menuju tujuan tanpa melanggar batas collision dengan lingkungan.

---

## Keterbatasan Demo

Metode pada hands-on ini masih sangat sederhana.

Pendekatan potential field seperti ini dapat mengalami beberapa keterbatasan, misalnya:

```text
Local Minimum
Oscillation
Dead End
```

Pada sistem robot yang lebih kompleks, navigation biasanya menggunakan kombinasi antara:

```text
Global Planning
Local Planning
Localization
Mapping
Obstacle Avoidance
```

Contohnya adalah algoritma seperti A*, Dijkstra, RRT, Dynamic Window Approach, atau navigation stack berbasis ROS 2.

Namun untuk hands-on pengantar, contoh ini cukup untuk menunjukkan bagaimana goal attraction dan obstacle avoidance dapat digabungkan menjadi perilaku navigation.

---

## Inti Konsep

Hands-on ini memperlihatkan pola dasar navigation:

```text
Current Robot Position
        ↓
Goal Direction
        +
Obstacle Information
        ↓
Navigation Decision
        ↓
Robot Motion
        ↓
New Robot Position
```

Navigation bukan hanya bergerak menuju goal, tetapi juga terus menyesuaikan arah berdasarkan kondisi lingkungan di sekitar robot.
