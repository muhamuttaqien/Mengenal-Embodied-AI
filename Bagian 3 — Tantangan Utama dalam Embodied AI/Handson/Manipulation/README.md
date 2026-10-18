# Hands-on Manipulation

Folder ini berisi demo sederhana **pick-and-place menggunakan robot arm planar 2-DOF** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Tujuan hands-on ini adalah memahami bagaimana robot manipulator dapat menggerakkan end-effector menuju object, melakukan grasp, memindahkan object, lalu meletakkannya di posisi tujuan.

Secara sederhana:

```text
Home
  ↓
Approach Object
  ↓
Move to Object
  ↓
Grasp
  ↓
Lift Object
  ↓
Move to Place Area
  ↓
Place Object
  ↓
Release
  ↓
Return Home
```

---

## File

```text
Manipulation/
├── manipulation_demo.py
├── requirements.txt
├── README.md
└── results/
    ├── manipulation_result.png
    └── manipulation_animation.gif
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
python manipulation_demo.py
```

---

## Apa yang Dilakukan Script?

Demo menggunakan robot arm planar dengan dua joint revolute atau **2-DOF**.

Robot memiliki dua link:

```text
Link 1 = 2.0 m
Link 2 = 1.5 m
```

Posisi base robot tetap di:

```text
BASE = [0.0, 0.0]
```

Robot kemudian diminta menggerakkan end-effector melalui beberapa waypoint:

```text
HOME
OBJECT_APPROACH
OBJECT_START
PLACE_APPROACH
PLACE_POSITION
HOME
```

Waypoint tersebut membentuk satu sequence pick-and-place sederhana.

---

## Robot Arm 2-DOF

Robot memiliki dua joint angle:

```text
q1
q2
```

Secara konseptual:

```text
Base
  ●
   \  Link 1
    ● Joint 2
           \ Link 2
       ● End-Effector
```

Nilai `q1` menentukan sudut link pertama terhadap base.

Nilai `q2` menentukan sudut link kedua relatif terhadap link pertama.

Dengan dua joint tersebut, end-effector dapat bergerak pada bidang 2D.

---

## Inverse Kinematics

Trajectory pada demo ditentukan dalam ruang Cartesian:

```text
[x, y]
```

Namun robot arm bergerak menggunakan joint angle:

```text
[q1, q2]
```

Karena itu, script menggunakan **inverse kinematics** untuk mengubah target posisi end-effector menjadi joint angle.

Secara sederhana:

```text
Target End-Effector Position
          ↓
    Inverse Kinematics
          ↓
       q1, q2
```

Jika target end-effector adalah:

```text
[x, y]
```

inverse kinematics mencari kombinasi `q1` dan `q2` yang membuat ujung robot mencapai posisi tersebut.

---

## Forward Kinematics

Setelah joint angle diperoleh, script menggunakan **forward kinematics** untuk menghitung kembali posisi robot.

Secara sederhana:

```text
q1, q2
  ↓
Forward Kinematics
  ↓
Joint Position
+
End-Effector Position
```

Forward kinematics digunakan untuk mengetahui:

```text
Posisi base
Posisi joint kedua
Posisi end-effector
```

Informasi ini kemudian dipakai untuk menggambar robot pada visualisasi.

---

## Trajectory

Gerakan robot dibuat dengan interpolasi linear antara beberapa waypoint.

Urutannya:

```text
HOME
  ↓
OBJECT_APPROACH
  ↓
OBJECT_START
  ↓
OBJECT_APPROACH
  ↓
PLACE_APPROACH
  ↓
PLACE_POSITION
  ↓
PLACE_APPROACH
  ↓
HOME
```

`OBJECT_APPROACH` berada sedikit di atas object.

Robot terlebih dahulu mendekati object dari atas sebelum bergerak ke posisi grasp.

Hal yang sama dilakukan pada sisi place menggunakan:

```text
PLACE_APPROACH
```

Dengan demikian, gerakan tidak hanya berpindah langsung dari object ke target, tetapi mengikuti sequence yang menyerupai pick-and-place robot manipulator.

---

## Grasp

Ketika end-effector mencapai:

```text
OBJECT_START
```

script mengaktifkan status:

```text
holding_object = True
```

Terminal akan menampilkan:

```text
Object grasped.
```

Setelah itu, posisi object akan mengikuti posisi end-effector.

Secara konseptual:

```text
Before Grasp

End-Effector
     ↓
     ●

     ■ Object


After Grasp

End-Effector + Object
        ●■
         ↓
   bergerak bersama
```

Demo ini tidak mensimulasikan finger atau contact physics.

Grasp direpresentasikan secara sederhana dengan membuat posisi object mengikuti posisi end-effector.

---

## Release

Ketika robot mencapai:

```text
PLACE_POSITION
```

status grasp diubah menjadi:

```text
holding_object = False
```

Terminal akan menampilkan:

```text
Object released.
```

Setelah release, object tetap berada pada `PLACE_POSITION`, sedangkan end-effector bergerak kembali ke atas dan akhirnya menuju home.

Secara sederhana:

```text
Robot membawa object
        ↓
Place Position
        ↓
Release
        ↓
Object tetap
        ↓
Robot kembali Home
```

---

## Output Terminal

Ketika program dijalankan, terminal akan menampilkan tiga event utama:

```text
Object grasped.
Object released.
Manipulation task completed.
```

Setelah visualisasi disimpan, terminal juga akan menampilkan lokasi file hasil.

---

## Hasil 1 — `manipulation_result.png`

Visualisasi statis disimpan ke:

```text
results/manipulation_result.png
```

Gambar ini merangkum hasil keseluruhan task pick-and-place.

Elemen utama pada gambar adalah:

```text
End-Effector Trajectory
Object Start
Place Target
Robot Arm
Placed Object
```

### End-Effector Trajectory

Garis putus-putus menunjukkan jalur yang dilalui end-effector selama task.

Trajectory dimulai dari posisi home, bergerak menuju object, membawa object ke sisi lain workspace, lalu kembali ke home.

Dengan melihat trajectory ini, kita dapat memahami bahwa planning pada manipulation tidak hanya berkaitan dengan posisi akhir robot, tetapi juga bagaimana end-effector bergerak sepanjang task.

---

### Object Start

Marker `Object Start` menunjukkan posisi awal object sebelum grasp.

Posisi ini digunakan sebagai target utama pada fase pick.

Robot harus membawa end-effector ke posisi tersebut sebelum object mulai mengikuti gerakan robot.

---

### Place Target

Marker berbentuk bintang menunjukkan:

```text
Place Target
```

yaitu lokasi tujuan tempat object harus diletakkan.

Target ini berbeda dari `PLACE_APPROACH`.

`PLACE_APPROACH` digunakan sebagai waypoint untuk mendekati target dari atas, sedangkan `PLACE_POSITION` merupakan lokasi release object.

---

### Robot Arm

Robot arm yang terlihat pada gambar menunjukkan konfigurasi akhir setelah seluruh sequence selesai.

Karena trajectory diakhiri dengan gerakan kembali ke:

```text
HOME
```

robot pada gambar statis berada pada konfigurasi home, bukan pada konfigurasi saat grasp atau release.

Hal ini penting saat membaca hasil karena gambar statis merangkum trajectory keseluruhan tetapi hanya menampilkan satu konfigurasi robot, yaitu konfigurasi terakhir.

---

### Placed Object

Marker `Placed Object` menunjukkan posisi akhir object.

Jika task berhasil, marker tersebut berada pada:

```text
PLACE_POSITION
```

Ini menunjukkan bahwa object telah berpindah dari sisi awal workspace ke target place.

Secara keseluruhan, gambar dapat dibaca sebagai:

```text
Object Start
     ↓
Robot picks object
     ↓
End-Effector Trajectory
     ↓
Place Target
     ↓
Placed Object
```

---

## Hasil 2 — `manipulation_animation.gif`

Animasi disimpan ke:

```text
results/manipulation_animation.gif
```

GIF merupakan visualisasi yang paling penting untuk memahami demo ini karena seluruh proses manipulation berlangsung secara berurutan.

Animasi memperlihatkan:

```text
Robot bergerak dari home
        ↓
Mendekati object
        ↓
Turun ke object
        ↓
Object mulai ikut bergerak
        ↓
Robot mengangkat object
        ↓
Robot membawa object ke target
        ↓
Robot menurunkan object
        ↓
Object berhenti mengikuti robot
        ↓
Robot kembali ke home
```

---

## Cara Membaca GIF

Pada setiap frame, terdapat beberapa elemen.

### Robot Arm

Garis tebal dengan tiga titik menunjukkan:

```text
Base
Joint
End-Effector
```

Perubahan bentuk robot dari frame ke frame menunjukkan perubahan joint angle `q1` dan `q2`.

---

### End-Effector Path

Garis putus-putus yang terus bertambah menunjukkan posisi yang sebelumnya sudah dilewati end-effector.

Dengan demikian, kita dapat melihat trajectory robot terbentuk secara bertahap.

---

### Object

Marker kotak menunjukkan posisi object.

Sebelum grasp, object tetap berada di:

```text
OBJECT_START
```

Setelah grasp, marker object bergerak bersama end-effector.

Setelah release, marker berhenti di:

```text
PLACE_POSITION
```

sementara robot terus bergerak kembali menuju home.

Bagian ini secara visual memperlihatkan transisi:

```text
Not Holding
    ↓
Holding
    ↓
Not Holding
```

---

### Place Target

Marker bintang menunjukkan lokasi place.

Target ini tetap sepanjang animasi sehingga kita dapat membandingkan posisi object terhadap target selama robot bergerak.

---

## Hubungan antara IK, FK, dan Manipulation

Demo ini juga memperlihatkan hubungan penting antara beberapa konsep robotika.

```text
Desired End-Effector Position
          ↓
   Inverse Kinematics
          ↓
      Joint Angles
          ↓
   Forward Kinematics
          ↓
Actual Robot Geometry
          ↓
     Manipulation
```

Inverse kinematics digunakan untuk mencari joint angle dari target Cartesian.

Forward kinematics digunakan untuk menghitung bentuk robot berdasarkan joint angle tersebut.

Keduanya bekerja bersama untuk menghasilkan gerakan manipulator.

---

## Keterbatasan Demo

Demo ini sengaja dibuat sederhana agar fokus pada konsep dasar.

Beberapa hal yang belum dimodelkan antara lain:

```text
3D motion
Gripper fingers
Contact physics
Collision checking
Object dynamics
Joint velocity limits
Joint acceleration limits
Torque
Trajectory optimization
Perception
```

Object juga dianggap langsung berhasil digenggam ketika end-effector mencapai posisi grasp.

Pada robot nyata, pick-and-place memerlukan banyak komponen tambahan seperti:

```text
Object Detection
Pose Estimation
Motion Planning
Collision Avoidance
Gripper Control
Force / Contact Handling
Feedback Control
```

---

## Inti Konsep

Hands-on ini memperlihatkan pipeline manipulation paling sederhana:

```text
Target Position
      ↓
Inverse Kinematics
      ↓
Joint Configuration
      ↓
Robot Motion
      ↓
Grasp Object
      ↓
Transport Object
      ↓
Release Object
```

Manipulation bukan hanya memindahkan robot arm.

Tujuan akhirnya adalah membuat robot **berinteraksi dengan object di lingkungan untuk mencapai task tertentu**.
