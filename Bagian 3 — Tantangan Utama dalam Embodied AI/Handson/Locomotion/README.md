# Hands-on Locomotion

Folder ini berisi demo sederhana **biped locomotion berbasis kinematic gait** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Tujuan hands-on ini adalah memahami bagaimana koordinasi gerakan hip dan knee pada kaki kiri dan kanan dapat menghasilkan pola berjalan sederhana.

Secara garis besar:

```text
Walking Parameters
      ↓
Periodic Gait
      ↓
Hip + Knee Angles
      ↓
Leg Forward Kinematics
      ↓
Foot Motion
      ↓
Biped Walking
```

---

## File

```text
Locomotion/
├── locomotion_demo.py
├── requirements.txt
├── README.md
└── results/
    ├── locomotion_result.png
    └── locomotion_animation.gif
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
python locomotion_demo.py
```

---

## Apa yang Dilakukan Script?

Demo mensimulasikan robot biped sederhana dengan dua kaki.

Masing-masing kaki memiliki:

```text
Hip Joint
Knee Joint
Thigh
Shank
Foot Position
```

Panjang segment kaki ditentukan melalui:

```text
THIGH_LENGTH
SHANK_LENGTH
```

Body robot kemudian digerakkan maju dengan kecepatan konstan menggunakan:

```text
WALKING_SPEED
```

Sementara itu, posisi pelvis memiliki sedikit gerakan vertikal untuk membuat pola berjalan terlihat lebih alami.

---

## Time Step dan Durasi

Simulasi menggunakan:

```text
DT = 0.05
DURATION = 8.0
```

`DT` menentukan interval waktu antara dua state simulasi.

Semakin kecil `DT`, semakin banyak frame yang dihitung selama durasi simulasi.

Time vector dibentuk dari:

```text
0 → DURATION
```

dengan interval sebesar:

```text
DT
```

Setiap elemen waktu kemudian digunakan untuk menghitung joint angle dan posisi kaki.

---

## Walking Speed

Posisi pelvis pada sumbu horizontal dihitung dari:

```text
pelvis_x = WALKING_SPEED × time
```

Artinya, pelvis bergerak maju dengan kecepatan konstan.

Jika:

```text
WALKING_SPEED = 0.35 m/s
```

maka selama simulasi berlangsung pelvis akan terus berpindah ke arah positif sumbu X.

Jarak total yang ditempuh dihitung dari perubahan posisi pelvis dari awal hingga akhir simulasi.

---

## Gait Periodik

Gerakan berjalan dibuat menggunakan pola sinusoidal.

Pertama, script menghitung:

```text
phase
```

berdasarkan:

```text
STEP_FREQUENCY
```

dan waktu.

Secara sederhana:

```text
Time
 ↓
Phase
 ↓
Sinusoidal Joint Motion
```

Hip dan knee kemudian mengikuti pola periodik berdasarkan phase tersebut.

---

## Koordinasi Kaki Kiri dan Kanan

Salah satu konsep penting pada demo ini adalah perbedaan fase antara kaki kiri dan kanan.

Hip kiri menggunakan:

```text
sin(phase)
```

sedangkan hip kanan menggunakan:

```text
sin(phase + π)
```

Tambahan:

```text
π radian = 180°
```

membuat kedua kaki berada pada fase berlawanan.

Secara sederhana:

```text
Left Leg Forward
      ↓
Right Leg Backward

kemudian:

Right Leg Forward
      ↓
Left Leg Backward
```

Pola seperti ini membuat kedua kaki bergerak bergantian seperti pola berjalan bipedal sederhana.

---

## Hip Motion

Sudut hip dikontrol oleh:

```text
HIP_AMPLITUDE
```

Nilai ini menentukan seberapa besar kaki berayun ke depan dan ke belakang.

Secara konseptual:

```text
Negative Hip Angle
        ↓
Leg swings backward

Positive Hip Angle
        ↓
Leg swings forward
```

Kaki kiri dan kanan menggunakan amplitude yang sama tetapi berbeda fase.

---

## Knee Motion

Gerakan knee menggunakan dua parameter:

```text
KNEE_BASE
KNEE_AMPLITUDE
```

`KNEE_BASE` memberikan sudut dasar pada knee.

`KNEE_AMPLITUDE` menentukan seberapa besar knee menekuk selama gait.

Gerakan knee dibuat periodik sehingga knee terus berubah antara kondisi lebih lurus dan lebih menekuk.

Secara sederhana:

```text
Walking Cycle
    ↓
Knee extends
    ↓
Knee bends
    ↓
Knee extends
    ↓
Repeat
```

---

## Pelvis Motion

Pelvis bergerak pada dua arah.

Pada sumbu X:

```text
Forward Translation
```

Pada sumbu Y:

```text
Small Vertical Oscillation
```

Gerakan vertikal dibuat menggunakan fungsi sinusoidal.

Secara sederhana:

```text
Pelvis
   ↗
    ↘
     ↗
      ↘
```

Gerakan ini membuat body tidak hanya bergeser secara horizontal secara kaku.

---

## Forward Kinematics Kaki

Untuk setiap frame, script menggunakan **forward kinematics** untuk menghitung posisi knee dan foot dari:

```text
Hip Position
Hip Angle
Knee Angle
```

Alurnya:

```text
Hip Position
     +
Hip Angle
     ↓
Knee Position
     +
Knee Angle
     ↓
Foot Position
```

Pertama, posisi knee dihitung menggunakan panjang thigh.

Kemudian posisi foot dihitung dari posisi knee menggunakan panjang shank.

Dengan cara ini, perubahan joint angle dapat diterjemahkan menjadi posisi geometris kaki.

---

## Mengapa Forward Kinematics Penting?

Joint trajectory hanya memberi tahu kita nilai:

```text
Hip Angle
Knee Angle
```

Namun untuk menggambar robot, kita membutuhkan posisi:

```text
Hip
Knee
Foot
```

Forward kinematics menghubungkan kedua representasi tersebut:

```text
Joint Space
    ↓
Forward Kinematics
    ↓
Cartesian Position
```

Ini merupakan salah satu konsep dasar locomotion dan robot kinematics.

---

## Output Terminal

Ketika simulasi selesai, terminal menampilkan informasi seperti:

```text
Walking simulation completed.
Duration: 8.0 seconds
Walking speed: 0.35 m/s
Distance travelled: ... m
```

Informasi ini memberi ringkasan gerakan body selama simulasi.

---

## Hasil 1 — `locomotion_result.png`

Grafik joint trajectory disimpan ke:

```text
results/locomotion_result.png
```

Gambar ini menunjukkan perubahan sudut empat joint terhadap waktu:

```text
Left Hip
Right Hip
Left Knee
Right Knee
```

Sumbu horizontal menunjukkan:

```text
Time (s)
```

sedangkan sumbu vertikal menunjukkan:

```text
Joint Angle (degree)
```

---

### Left Hip dan Right Hip

Kurva hip kiri dan kanan berbentuk sinusoidal.

Kedua kurva memiliki pola yang sama tetapi berbeda fase 180°.

Ketika hip kiri bergerak ke satu arah, hip kanan bergerak ke arah sebaliknya.

Ini dapat terlihat dari pola:

```text
Left Hip   /\/\/\
Right Hip  \/\/\/
```

Perbedaan fase tersebut merupakan sumber utama koordinasi antara kaki kiri dan kanan.

---

### Left Knee dan Right Knee

Kurva knee menunjukkan pola flexion dan extension selama gait.

Seperti hip, knee kiri dan kanan juga memiliki phase offset.

Ketika salah satu kaki memasuki bagian tertentu dari walking cycle, kaki lainnya berada pada bagian cycle yang berbeda.

Hal ini membantu menciptakan gerakan kaki bergantian.

---

### Cara Membaca Grafik

Hal utama yang perlu diperhatikan pada `locomotion_result.png` adalah periodicity.

Joint angle terus mengulang pola yang sama:

```text
Cycle 1
 ↓
Cycle 2
 ↓
Cycle 3
 ↓
...
```

Frekuensi pengulangan ditentukan oleh:

```text
STEP_FREQUENCY
```

Jika frekuensi dinaikkan, oscillation joint akan berlangsung lebih cepat.

Jika amplitude dinaikkan, rentang sudut joint akan menjadi lebih besar.

Dengan demikian, grafik membantu kita melihat langsung hubungan antara parameter gait dan joint trajectory.

---

## Hasil 2 — `locomotion_animation.gif`

Animasi berjalan disimpan ke:

```text
results/locomotion_animation.gif
```

GIF memperlihatkan representasi biped sederhana yang bergerak dari kiri ke kanan.

Elemen utama pada animasi adalah:

```text
Left Leg
Right Leg
Body
Head
Pelvis Trajectory
Ground
```

---

## Cara Membaca GIF

### Left Leg dan Right Leg

Kedua kaki digambar dengan style yang berbeda agar lebih mudah dibedakan.

Masing-masing kaki terdiri dari:

```text
Hip
 ↓
Knee
 ↓
Foot
```

Ketika animasi berjalan, kita dapat melihat kaki kiri dan kanan bergerak dengan fase yang berbeda.

Secara umum:

```text
Left Leg swings forward
        ↓
Right Leg swings backward
        ↓
Roles switch
        ↓
Repeat
```

Inilah pola koordinasi utama yang ingin diperlihatkan oleh hands-on ini.

---

### Body

Body ditampilkan sebagai garis vertikal yang terhubung dengan pelvis.

Karena pelvis bergerak ke depan, seluruh body juga ikut berpindah sepanjang sumbu X.

Body tidak memiliki dynamic balance pada demo ini.

Posisinya langsung mengikuti trajectory pelvis yang sudah ditentukan.

---

### Head

Head ditampilkan di atas torso.

Marker head hanya digunakan untuk membuat representasi biped lebih mudah dibaca secara visual.

Head tidak memiliki dinamika atau joint tersendiri pada demo ini.

---

### Pelvis Trajectory

Garis titik-titik menunjukkan:

```text
Pelvis Trajectory
```

Trajectory ini menunjukkan bagaimana pusat body berpindah selama simulasi.

Karena pelvis juga memiliki sedikit vertical oscillation, garis tersebut tidak sepenuhnya lurus.

Secara konseptual:

```text
Forward Motion
──────────────→

dengan sedikit:

↑ ↓ ↑ ↓ ↑ ↓
```

---

### Ground

Garis horizontal pada:

```text
y = 0
```

merepresentasikan ground.

Garis ini membantu kita melihat posisi kaki relatif terhadap permukaan tanah.

Namun perlu diperhatikan bahwa demo ini belum menggunakan contact physics.

Karena itu, foot tidak benar-benar menghasilkan ground reaction force seperti pada simulasi physics-based locomotion.

---

## Hubungan Joint Trajectory dan Animasi

Kedua output sebenarnya menunjukkan informasi yang sama dari dua perspektif berbeda.

`locomotion_result.png` menunjukkan:

```text
Joint Space
```

yaitu bagaimana sudut joint berubah terhadap waktu.

Sedangkan `locomotion_animation.gif` menunjukkan:

```text
Cartesian Space
```

yaitu bagaimana perubahan sudut tersebut menghasilkan gerakan body dan kaki di ruang 2D.

Hubungannya adalah:

```text
Joint Angles
      ↓
Forward Kinematics
      ↓
Knee + Foot Positions
      ↓
Walking Animation
```

---

## Apakah Ini Sudah Merupakan Walking Robot yang Stabil?

Belum.

Demo ini merupakan **kinematic gait**, bukan physics-based biped walking.

Artinya, joint angle dan body translation sudah ditentukan sebelumnya.

Robot belum menghitung:

```text
Balance
Gravity
Ground Reaction Force
Friction
Center of Mass
Zero Moment Point
Foot Contact
Torque
```

Karena itu, robot pada demo tidak perlu mempertahankan keseimbangan secara fisik.

Tujuannya adalah memahami pola koordinasi joint terlebih dahulu sebelum masuk ke locomotion yang lebih kompleks.

---

## Keterbatasan Demo

Beberapa penyederhanaan utama adalah:

```text
2D Motion
Preset Gait
No Physics
No Balance Control
No Ground Contact Model
No Torque Control
No Feedback Control
No Terrain Variation
```

Pada robot biped nyata, locomotion membutuhkan koordinasi antara:

```text
Perception
State Estimation
Gait Generation
Balance Control
Foot Placement
Dynamics
Feedback Control
```

Robot juga harus menyesuaikan gerakan ketika permukaan berubah atau ketika mendapat gangguan dari luar.

---

## Inti Konsep

Hands-on ini memperlihatkan hubungan dasar:

```text
Periodic Gait
      ↓
Joint Trajectory
      ↓
Forward Kinematics
      ↓
Leg Motion
      ↓
Body Translation
```

Locomotion bukan hanya membuat kaki bergerak.

Pada sistem yang lebih realistis, robot juga harus memastikan bahwa gerakan tersebut **stabil, seimbang, dan sesuai dengan kondisi lingkungan**.
