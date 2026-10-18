# Bonus Hands-on Planning: Dynamic Replanning dengan A*

Demo ini memperluas hands-on **A* path planning** dengan menunjukkan apa yang terjadi ketika environment berubah setelah robot mulai bergerak.

Pada contoh sebelumnya, map dianggap tetap selama planning dan eksekusi.

Pada demo ini, sebuah obstacle baru muncul pada jalur yang sebelumnya direncanakan sehingga robot harus memperbarui map dan membuat path baru.

Secara sederhana:

```text
Initial Map
    ↓
A* Initial Planning
    ↓
Robot mulai bergerak
    ↓
Obstacle baru muncul
    ↓
Map berubah
    ↓
A* Replanning
    ↓
Robot mengikuti path baru
    ↓
Goal
```

---

## File

```text
Planning/
├── dynamic_replanning.py
├── requirements.txt
├── README.md
└── results/
    ├── dynamic_replanning_result.png
    └── dynamic_replanning.gif
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
python dynamic_replanning.py
```

---

## Apa yang Dilakukan Script?

Demo ini menjalankan dua proses planning.

Pertama, A* membuat path dari:

```text
START
```

menuju:

```text
GOAL
```

menggunakan map awal.

Setelah initial path ditemukan, robot tidak langsung melompat ke goal.

Robot mulai mengikuti beberapa node pada path tersebut.

Setelah sejumlah gerakan tertentu, sebuah obstacle baru muncul pada salah satu node yang masih berada di depan robot.

Urutannya adalah:

```text
1. A* membuat initial path
2. Robot mulai mengikuti path
3. Obstacle baru muncul pada original path
4. Map diperbarui
5. A* dijalankan kembali
6. Path alternatif ditemukan
7. Robot mengikuti replanned path
8. Robot mencapai goal
```

---

## Initial Planning

Pada awal program, environment masih menggunakan map awal.

A* mencari path:

```text
START → GOAL
```

dengan mempertimbangkan seluruh obstacle statis yang sudah diketahui.

Hasil ini disebut:

```text
Original Plan
```

Original plan merupakan path terbaik berdasarkan informasi environment yang tersedia pada saat planning dilakukan.

Namun path ini belum tentu tetap valid ketika environment berubah.

---

## Robot Mulai Bergerak

Setelah initial path ditemukan, robot mulai mengikuti path tersebut.

Parameter:

```text
REPLAN_AFTER_MOVES = 8
```

menentukan berapa banyak gerakan yang dilakukan robot sebelum perubahan environment diperkenalkan.

Secara konseptual:

```text
Start
  ↓
Original Plan
  ↓
Move
  ↓
Move
  ↓
Move
  ↓
...
  ↓
Environment Changes
```

Posisi robot ketika perubahan terjadi menjadi titik awal untuk proses replanning.

---

## Obstacle Baru Muncul

Script memilih sebuah node yang berada beberapa langkah di depan robot pada original path.

Node tersebut kemudian diubah menjadi:

```text
OCCUPIED
```

Dengan kata lain, jalur yang sebelumnya dianggap aman sekarang terhalang.

Secara sederhana:

```text
Original Plan:

Start ─────────────→ Goal


Setelah obstacle muncul:

Start ─────→ Robot ─── X ───→ Goal
                       ↑
                 New Obstacle
```

Robot tidak dapat lagi terus mengikuti original path karena path tersebut sekarang melewati obstacle.

---

## Map Diperbarui

Setelah obstacle baru terdeteksi, script membuat versi map yang sudah diperbarui.

Secara konseptual:

```text
Old Map
   ↓
Detect New Obstacle
   ↓
Update Occupancy Grid
   ↓
New Map
```

Perubahan map ini penting karena planning hanya dapat menghasilkan keputusan yang benar jika representasi environment juga diperbarui.

---

## Replanning

Setelah map berubah, A* dijalankan kembali.

Namun planning tidak dimulai dari `START`.

A* sekarang mencari jalur dari:

```text
Current Robot Position
```

menuju:

```text
GOAL
```

menggunakan map yang sudah memiliki obstacle baru.

Secara sederhana:

```text
Current Robot Position
        ↓
Updated Map
        ↓
A*
        ↓
Alternative Path
        ↓
Goal
```

Hasilnya disebut:

```text
Replanned Path
```

Path baru tersebut menghindari obstacle yang membuat original plan tidak lagi valid.

---

## Mengapa Tidak Merencanakan dari Start Lagi?

Ketika obstacle baru muncul, robot sudah berpindah dari posisi awal.

Karena itu, robot tidak perlu membuat ulang perjalanan dari `START`.

Planning dilakukan dari posisi aktual robot:

```text
current_position
```

Ini merupakan prinsip penting dalam replanning.

Robot memperbarui rencana berdasarkan:

```text
Current State
+
Updated Environment
+
Goal
```

bukan berdasarkan kondisi awal yang sudah tidak relevan.

---

## Output Terminal

Ketika program dijalankan, terminal akan menampilkan beberapa informasi penting.

Contohnya:

```text
Initial plan found.
Initial path length: ...

Robot reached: (...)

New obstacle detected at: (...)

Replanning successful.
New path length: ...
```

Informasi tersebut menunjukkan empat tahap utama:

```text
Initial Planning
Robot Execution
Environment Change
Replanning
```

Jika initial path tidak dapat ditemukan, program akan berhenti.

Program juga akan berhenti jika obstacle baru membuat goal benar-benar tidak dapat dicapai.

---

## Hasil 1 — `dynamic_replanning_result.png`

Visualisasi statis disimpan ke:

```text
results/dynamic_replanning_result.png
```

Gambar ini merangkum seluruh proses planning dan replanning dalam satu visualisasi.

Elemen yang ditampilkan meliputi:

```text
Initial Explored Nodes
Replanning Explored Nodes
Original Plan
Replanned Path
Robot Trajectory
Start
Goal
New Obstacle
```

### Original Plan

`Original Plan` menunjukkan path yang dibuat A* sebelum obstacle baru muncul.

Path ini masih ditampilkan setelah replanning agar kita dapat membandingkan:

```text
Rencana sebelum perubahan
vs.
Rencana setelah perubahan
```

Bagian original plan yang melewati obstacle baru menunjukkan alasan mengapa path tersebut tidak dapat terus digunakan.

---

### New Obstacle

`New Obstacle` ditandai menggunakan marker `X`.

Obstacle ini sengaja muncul pada salah satu node di original plan.

Ini membuat perubahan environment terlihat jelas:

```text
Original path
      ↓
New obstacle appears
      ↓
Original path becomes invalid
```

---

### Replanned Path

`Replanned Path` menunjukkan jalur baru yang ditemukan A* setelah map diperbarui.

Path ini dimulai dari posisi robot saat replanning dilakukan, bukan dari posisi start awal.

Karena itu, path baru hanya menggambarkan sisa perjalanan robot menuju goal.

Secara sederhana:

```text
Start
  ↓
Robot follows original plan
  ↓
Current Position
  ↓
Replanned Path
  ↓
Goal
```

---

### Robot Trajectory

`Robot Trajectory` menunjukkan jalur yang benar-benar dijalankan robot.

Trajectory aktual terdiri dari dua bagian:

```text
Bagian 1
Robot mengikuti original plan

Bagian 2
Robot mengikuti replanned path
```

Karena itu, robot trajectory merupakan gabungan antara eksekusi sebelum dan sesudah replanning.

---

### Initial Explored Nodes

`Initial Explored Nodes` menunjukkan node yang diperiksa A* ketika membuat plan pertama.

Node ini menggambarkan search space pada kondisi map awal.

---

### Replanning Explored Nodes

`Replanning Explored Nodes` menunjukkan node yang diperiksa ketika A* dijalankan kembali setelah obstacle muncul.

Node-node tersebut dapat berbeda dari initial explored nodes karena:

```text
Start planning berbeda
+
Map berbeda
```

Dengan melihat keduanya, kita dapat memahami bahwa replanning bukan sekadar menggambar ulang path lama.

Algoritma benar-benar melakukan pencarian baru berdasarkan kondisi environment terbaru.

---

## Hasil 2 — `dynamic_replanning.gif`

Animasi disimpan ke:

```text
results/dynamic_replanning.gif
```

GIF ini memperlihatkan proses replanning secara temporal.

Pada awal animasi:

```text
Original Map
+
Original Plan
+
Robot
```

ditampilkan.

Robot kemudian mulai bergerak mengikuti original plan.

Setelah jumlah langkah yang sudah ditentukan tercapai:

```text
New Obstacle Appears
```

Map langsung diperbarui.

Pada saat yang sama:

```text
Replanned Path
```

muncul pada visualisasi.

Robot kemudian melanjutkan perjalanan menggunakan path baru.

Alur animasinya dapat dibaca sebagai:

```text
Frame 1
Original plan tersedia
        ↓
Frame 2
Robot mulai bergerak
        ↓
...
        ↓
Replanning frame
Obstacle baru muncul
        ↓
Map berubah
        ↓
Replanned path muncul
        ↓
Robot mengikuti path baru
        ↓
Goal
```

GIF penting karena gambar statis hanya menunjukkan hasil akhir.

Animasi memperlihatkan **kapan environment berubah** dan **kapan robot mengganti rencananya**.

---

## Planning vs. Replanning

Pada planning biasa:

```text
Map
 ↓
Plan
 ↓
Execute
 ↓
Goal
```

Diasumsikan bahwa map tetap valid selama robot bergerak.

Pada dynamic replanning:

```text
Map
 ↓
Plan
 ↓
Execute
 ↓
Environment Changes
 ↓
Update Map
 ↓
Replan
 ↓
Continue Execution
```

Inilah perbedaan utama hands-on ini dengan contoh A* sebelumnya.

Robot tidak hanya mampu membuat rencana, tetapi juga mampu **mengubah rencana ketika asumsi awal tidak lagi berlaku**.

---

## Perbedaan dengan Dynamic Navigation

Dynamic replanning dan dynamic navigation sama-sama menangani perubahan environment, tetapi pendekatannya berbeda.

Pada dynamic navigation sebelumnya, robot menyesuaikan gerakannya secara lokal berdasarkan obstacle yang bergerak:

```text
Observe
 ↓
React
 ↓
Move
```

Pada dynamic replanning, perubahan environment menyebabkan path global dihitung ulang:

```text
Detect Change
 ↓
Update Map
 ↓
Run Planner Again
 ↓
New Global Path
```

Secara sederhana:

```text
Reactive Navigation
→ menyesuaikan gerakan lokal

Dynamic Replanning
→ memperbarui rencana global
```

Dalam sistem robot nyata, kedua pendekatan ini dapat digunakan bersama.

---

## Keterbatasan Demo

Demo ini masih menggunakan skenario yang sangat sederhana.

Obstacle baru:

```text
muncul hanya sekali
```

dan lokasinya sengaja dipilih agar berada pada original path.

Selain itu:

```text
Map berbentuk grid
Gerakan hanya 4 arah
Cost setiap gerakan sama
Robot dianggap sebagai satu grid cell
Obstacle baru langsung diketahui
```

Pada sistem yang lebih kompleks, perubahan environment dapat terjadi berkali-kali dan sensor robot mungkin hanya mengetahui obstacle setelah mendekatinya.

Metode khusus untuk replanning juga dapat digunakan, misalnya:

```text
D*
D* Lite
Lifelong Planning A*
```

Metode tersebut dirancang untuk memanfaatkan hasil pencarian sebelumnya sehingga replanning dapat lebih efisien daripada menjalankan search dari awal setiap kali map berubah.

Namun demo ini menggunakan A* kembali karena lebih sederhana untuk memperlihatkan konsep dasar replanning.

---

## Inti Konsep

Hands-on ini menunjukkan bahwa planning pada robot tidak selalu merupakan proses satu kali.

```text
Plan
 ↓
Act
 ↓
Observe Change
 ↓
Update World Representation
 ↓
Replan
 ↓
Act Again
```

Kemampuan untuk memperbarui rencana sangat penting bagi Embodied AI karena environment dunia nyata tidak selalu tetap seperti saat initial plan dibuat.
