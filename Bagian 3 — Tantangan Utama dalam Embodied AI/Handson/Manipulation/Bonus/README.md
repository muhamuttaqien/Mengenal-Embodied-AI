# Bonus Hands-on Manipulation: Pick-and-Place dengan Obstacle Avoidance

Demo ini memperluas hands-on **Manipulation** utama dengan menambahkan obstacle pada workspace robot.

Pada demo sebelumnya, end-effector dapat bergerak langsung dari area object menuju area place.

Pada demo ini, robot harus melewati **safe waypoint** agar trajectory tidak membawa link robot terlalu dekat dengan obstacle.

Secara sederhana:

```text
Home
  ↓
Approach Object
  ↓
Grasp
  ↓
Lift
  ↓
Safe Waypoint
  ↓
Move to Place Area
  ↓
Place
  ↓
Release
  ↓
Safe Waypoint
  ↓
Return Home
```

Selain itu, script juga melakukan pengecekan collision sederhana antara kedua link robot dan obstacle berbentuk lingkaran.

---

## File

```text
Manipulation/
├── manipulation_obstacle_avoidance.py
├── requirements.txt
├── README.md
└── results/
    ├── manipulation_obstacle_result.png
    └── manipulation_obstacle_animation.gif
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
python manipulation_obstacle_avoidance.py
```

---

## Apa yang Dilakukan Script?

Demo menggunakan robot arm planar **2-DOF** dengan dua link.

Robot melakukan task pick-and-place dengan urutan:

```text
Reach
  ↓
Grasp
  ↓
Lift
  ↓
Safe Waypoint
  ↓
Transport
  ↓
Place
  ↓
Release
```

Perbedaannya dengan demo manipulation utama adalah adanya obstacle di tengah workspace.

Robot tidak membawa object langsung ke target, tetapi menggunakan waypoint tambahan agar trajectory lebih aman.

---

## Obstacle

Obstacle direpresentasikan sebagai lingkaran dengan:

```text
Center
Radius
```

Pada script, obstacle memiliki:

```text
OBSTACLE_CENTER
OBSTACLE_RADIUS
```

Robot juga menggunakan:

```text
SAFETY_MARGIN
```

untuk memberikan jarak tambahan antara link robot dan obstacle.

Secara sederhana:

```text
Obstacle Radius
      +
Safety Margin
      ↓
Collision Threshold
```

Dengan demikian, robot tidak hanya dianggap berbahaya ketika benar-benar menyentuh obstacle, tetapi juga ketika link terlalu dekat dengan obstacle.

---

## Safe Waypoint

Waypoint aman ditentukan menggunakan:

```text
SAFE_WAYPOINT
```

Waypoint ini ditempatkan di atas obstacle.

Setelah robot melakukan grasp dan mengangkat object, end-effector tidak bergerak langsung menuju area place.

Sebaliknya:

```text
Object Approach
      ↓
Safe Waypoint
      ↓
Place Approach
```

Hal yang sama dilakukan ketika robot kembali ke home:

```text
Place Approach
      ↓
Safe Waypoint
      ↓
Home
```

Dengan demikian, safe waypoint membantu membentuk trajectory yang melewati area yang lebih aman.

---

## Mengapa End-Effector Saja Tidak Cukup?

Pada robot manipulator, menghindari obstacle tidak cukup hanya dengan memastikan end-effector tidak menyentuh obstacle.

Robot memiliki seluruh struktur link:

```text
Base
  ↓
Link 1
  ↓
Joint
  ↓
Link 2
  ↓
End-Effector
```

Walaupun end-effector berada jauh dari obstacle, salah satu link masih dapat bertabrakan dengan obstacle.

Karena itu, demo ini melakukan collision checking terhadap:

```text
Link 1
Link 2
```

bukan hanya terhadap posisi end-effector.

---

## Collision Checking

Untuk memeriksa collision, script menghitung jarak obstacle terhadap masing-masing segment robot.

Link pertama direpresentasikan sebagai:

```text
Base → Joint 2
```

Link kedua direpresentasikan sebagai:

```text
Joint 2 → End-Effector
```

Kemudian dihitung jarak minimum dari pusat obstacle ke masing-masing segment.

Secara sederhana:

```text
Obstacle Center
      ↓
Distance to Link Segment
      ↓
Compare with:
Obstacle Radius + Safety Margin
      ↓
Safe / Collision Risk
```

Jika jaraknya lebih kecil dari batas aman, script menandainya sebagai collision risk.

---

## Point-to-Segment Distance

Untuk mengetahui jarak obstacle terhadap link robot, script menggunakan perhitungan **point-to-segment distance**.

Obstacle dianggap sebagai sebuah point pada pusat lingkaran:

```text
OBSTACLE_CENTER
```

sedangkan link robot dianggap sebagai line segment.

Algoritma mencari titik terdekat pada segment terhadap pusat obstacle.

Secara konseptual:

```text
Obstacle Center
      ●
      |
      | shortest distance
      |
------●---------- Link
```

Jika titik proyeksi berada di luar segment, titik terdekat dibatasi pada salah satu ujung segment.

Pendekatan ini sederhana tetapi cukup untuk mendemonstrasikan collision checking pada robot planar.

---

## Inverse Kinematics dan Forward Kinematics

Seperti hands-on Manipulation utama, trajectory ditentukan dalam ruang Cartesian:

```text
[x, y]
```

Inverse kinematics digunakan untuk mengubah target tersebut menjadi:

```text
[q1, q2]
```

Kemudian forward kinematics digunakan untuk menghitung:

```text
Base Position
Joint Position
End-Effector Position
```

Posisi tersebut diperlukan untuk menggambar robot dan memeriksa collision antara setiap link dengan obstacle.

Secara sederhana:

```text
Target Cartesian
      ↓
Inverse Kinematics
      ↓
Joint Angles
      ↓
Forward Kinematics
      ↓
Robot Geometry
      ↓
Collision Check
```

---

## Grasp dan Release

Ketika end-effector mencapai posisi object:

```text
holding_object = True
```

dan object mulai mengikuti posisi end-effector.

Terminal akan menampilkan:

```text
Object grasped.
```

Ketika robot mencapai posisi place:

```text
holding_object = False
```

dan object berhenti mengikuti robot.

Terminal akan menampilkan:

```text
Object released.
```

Setelah itu robot kembali menuju home melalui safe waypoint.

---

## Output Terminal

Selama program berjalan, terminal dapat menampilkan:

```text
Object grasped.
Object released.
Manipulation task completed.
```

Jika tidak ada collision yang terdeteksi, terminal juga menampilkan:

```text
Trajectory completed without detected link-obstacle collision.
```

Jika salah satu konfigurasi robot terlalu dekat dengan obstacle, akan muncul peringatan seperti:

```text
Warning: collision risk at step ...
```

Peringatan tersebut membantu kita mengecek apakah waypoint yang digunakan benar-benar menghasilkan trajectory yang aman.

---

## Hasil 1 — `manipulation_obstacle_result.png`

Visualisasi statis disimpan ke:

```text
results/manipulation_obstacle_result.png
```

Gambar ini merangkum keseluruhan task pick-and-place dengan obstacle avoidance.

Elemen utama yang ditampilkan adalah:

```text
Obstacle
End-Effector Trajectory
Object Start
Place Target
Safe Waypoint
Robot Arm
Placed Object
```

### Obstacle

Lingkaran pada workspace menunjukkan obstacle yang harus dihindari.

Obstacle ini berada di antara sisi pick dan place sehingga trajectory langsung tidak selalu menjadi pilihan yang aman.

---

### End-Effector Trajectory

Garis putus-putus menunjukkan seluruh jalur end-effector selama task.

Trajectory akan bergerak:

```text
Home
  ↓
Object
  ↓
Safe Waypoint
  ↓
Place
  ↓
Safe Waypoint
  ↓
Home
```

Bagian trajectory yang naik menuju safe waypoint menunjukkan bagaimana robot sengaja mengambil jalur yang lebih tinggi untuk menghindari obstacle.

---

### Safe Waypoint

Marker berbentuk segitiga menunjukkan:

```text
Safe Waypoint
```

Waypoint ini merupakan titik perantara yang digunakan untuk membawa end-effector ke area yang lebih aman sebelum berpindah ke sisi lain workspace.

Hal penting yang perlu diperhatikan adalah bahwa safe waypoint tidak otomatis dihitung oleh algoritma planning.

Pada demo ini, posisinya ditentukan sebelumnya agar konsep obstacle avoidance mudah dipahami.

---

### Object Start

Marker kotak menunjukkan posisi awal object.

Robot bergerak menuju posisi ini untuk melakukan grasp.

---

### Place Target

Marker bintang menunjukkan posisi tujuan object.

Setelah robot membawa object melewati safe waypoint, end-effector bergerak menuju target ini dan melakukan release.

---

### Robot Arm

Robot arm yang terlihat pada gambar adalah konfigurasi akhir setelah seluruh task selesai.

Karena trajectory diakhiri dengan kembali ke home, robot pada gambar statis berada pada konfigurasi home.

---

### Placed Object

Marker `Placed Object` menunjukkan posisi akhir object.

Jika task berhasil, object berada pada target place setelah release.

---

## Hasil 2 — `manipulation_obstacle_animation.gif`

Animasi disimpan ke:

```text
results/manipulation_obstacle_animation.gif
```

GIF menunjukkan keseluruhan proses secara temporal.

Urutannya dapat diamati sebagai:

```text
Robot bergerak dari home
        ↓
Mendekati object
        ↓
Melakukan grasp
        ↓
Mengangkat object
        ↓
Bergerak ke safe waypoint
        ↓
Melewati obstacle
        ↓
Menuju place target
        ↓
Melakukan release
        ↓
Kembali melalui safe waypoint
        ↓
Home
```

---

## Cara Membaca GIF

Pada setiap frame, terdapat beberapa elemen penting.

### Robot Arm

Garis tebal menunjukkan kedua link robot.

Dengan melihat gerakannya, kita dapat memperhatikan bahwa bukan hanya end-effector yang perlu menjauhi obstacle, tetapi seluruh link robot.

---

### Obstacle

Lingkaran obstacle tetap berada pada posisi yang sama selama animasi.

Kita dapat menggunakan obstacle ini sebagai referensi untuk melihat clearance antara robot dan lingkungan.

---

### End-Effector Path

Garis putus-putus bertambah sepanjang animasi.

Garis ini menunjukkan trajectory yang sudah dilalui end-effector.

Bagian trajectory yang melalui safe waypoint memperlihatkan bagaimana waypoint mengubah jalur dari trajectory langsung menjadi trajectory yang lebih aman.

---

### Object

Marker kotak menunjukkan object.

Sebelum grasp:

```text
Object tetap di OBJECT_START
```

Setelah grasp:

```text
Object mengikuti end-effector
```

Setelah release:

```text
Object tetap di PLACE_POSITION
```

---

### Safe Waypoint

Marker segitiga tetap terlihat sepanjang animasi.

Ini membantu kita memahami bahwa trajectory pick-and-place dirancang melewati titik perantara tertentu.

---

## Perbedaan dengan Manipulation Sebelumnya

Pada hands-on sebelumnya:

```text
Pick
 ↓
Move directly toward place
 ↓
Place
```

Pada demo ini:

```text
Pick
 ↓
Lift
 ↓
Safe Waypoint
 ↓
Move around obstacle
 ↓
Place
```

Selain itu, demo sebelumnya terutama berfokus pada:

```text
IK
FK
Pick-and-Place Sequence
```

sedangkan demo ini menambahkan:

```text
Obstacle Geometry
Safety Margin
Link Collision Checking
Safe Waypoint
```

Dengan demikian, kita mulai melihat bahwa manipulation tidak hanya membutuhkan posisi target, tetapi juga harus mempertimbangkan geometry environment.

---

## Keterbatasan Demo

Obstacle avoidance pada demo ini masih sangat sederhana.

Safe waypoint:

```text
ditentukan secara manual
```

bukan dicari secara otomatis oleh motion planner.

Selain itu, collision checking hanya menggunakan satu obstacle berbentuk lingkaran dalam bidang 2D.

Belum dimodelkan:

```text
3D Obstacles
Self-Collision
Gripper Geometry
Object Geometry
Joint Limits
Velocity Limits
Acceleration Limits
Trajectory Optimization
Automatic Motion Planning
Contact Physics
```

Pada robot manipulation nyata, motion planner biasanya mencari trajectory yang collision-free secara otomatis berdasarkan model robot dan representasi environment.

---

## Inti Konsep

Hands-on ini memperlihatkan bahwa manipulation bukan hanya masalah mencapai target end-effector.

Robot juga harus memastikan bahwa **seluruh tubuh robot dapat bergerak melalui environment dengan aman**.

Secara sederhana:

```text
Target
  ↓
Inverse Kinematics
  ↓
Robot Configuration
  ↓
Collision Check
  ↓
Safe Trajectory
  ↓
Manipulation
```

Safe waypoint pada demo ini menjadi pengantar sederhana menuju konsep yang lebih besar seperti **collision-aware motion planning** pada robot manipulator.
