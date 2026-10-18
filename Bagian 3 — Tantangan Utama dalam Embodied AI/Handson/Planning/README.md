# Hands-on Planning

Folder ini berisi demo sederhana **path planning menggunakan algoritma A\*** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Tujuannya adalah memahami bagaimana robot dapat mencari jalur dari posisi awal menuju goal pada map yang sudah diketahui sambil menghindari obstacle.

Secara sederhana:

```text
Known Map
   ↓
Start + Goal
   ↓
A* Search
   ↓
Explore Candidate Nodes
   ↓
Find Valid Path
   ↓
Planned Path
```

---

## File

```text
Planning/
├── planning_demo.py
├── requirements.txt
├── README.md
└── results/
    └── planning_result.png
```

`planning_demo.py` mengimplementasikan algoritma A* pada occupancy grid 2D.

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
python planning_demo.py
```

---

## Apa yang Dilakukan Script?

Script membuat sebuah map 2D berukuran:

```text
20 × 15 cells
```

Setiap cell pada map memiliki salah satu kondisi:

```text
FREE     = 0
OCCUPIED = 1
```

Cell `FREE` dapat dilalui robot.

Cell `OCCUPIED` merupakan obstacle dan tidak boleh dilalui.

Posisi awal robot adalah:

```text
START = (1, 1)
```

sedangkan goal adalah:

```text
GOAL = (18, 13)
```

Setelah map selesai dibuat, algoritma A* mencari jalur yang menghubungkan start dan goal tanpa melewati obstacle.

---

## Gerakan Robot pada Grid

Pada demo ini, robot hanya dapat bergerak ke empat arah:

```text
Right
Left
Up
Down
```

Secara sederhana:

```text
        Up
         ↑
Left ← Robot → Right
         ↓
        Down
```

Robot belum dapat bergerak diagonal.

Karena itu, setiap node memiliki maksimal empat neighbor yang dapat diperiksa.

Sebelum sebuah neighbor digunakan, script memastikan bahwa:

```text
Neighbor masih berada di dalam map
dan
Neighbor bukan obstacle
```

---

## Cara Kerja A*

A* memilih node berdasarkan kombinasi dua nilai:

```text
f(n) = g(n) + h(n)
```

dengan:

```text
g(n) → cost sebenarnya dari start menuju node n
h(n) → estimasi cost dari node n menuju goal
f(n) → estimasi total cost melalui node n
```

A* tidak hanya melihat node yang paling dekat dengan goal.

Algoritma juga mempertimbangkan cost yang sudah dikeluarkan untuk mencapai node tersebut.

Secara konseptual:

```text
Start
  ↓
Current Node
  ↓
g(n): berapa jauh perjalanan yang sudah dilakukan?
  +
h(n): berapa jauh perkiraan menuju goal?
  ↓
f(n)
  ↓
Pilih node yang paling menjanjikan
```

---

## Manhattan Distance

Demo ini menggunakan **Manhattan distance** sebagai heuristic:

```text
h(n) = |x1 - x2| + |y1 - y2|
```

Manhattan distance sesuai untuk contoh ini karena robot hanya dapat bergerak secara horizontal atau vertikal.

Contohnya, jika robot perlu berpindah:

```text
3 cell ke kanan
+
4 cell ke atas
```

maka estimasi jaraknya adalah:

```text
3 + 4 = 7
```

Heuristic membantu A* memprioritaskan pencarian ke arah goal dibanding mengeksplorasi seluruh map secara membabi buta.

---

## Priority Queue

A* menyimpan kandidat node pada sebuah **priority queue**.

Node dengan `f_score` paling kecil akan diperiksa lebih dahulu.

Secara sederhana:

```text
Candidate Nodes
      ↓
Compare f_score
      ↓
Smallest f_score
      ↓
Explore First
```

Python menyediakan struktur `heapq` yang digunakan pada script untuk menjalankan priority queue secara efisien.

---

## Reconstruct Path

Selama pencarian, script menyimpan informasi:

```text
came_from
```

yang mencatat dari node mana sebuah node dicapai.

Ketika goal ditemukan, informasi tersebut digunakan untuk menelusuri kembali jalur:

```text
Goal
 ↓
Previous Node
 ↓
Previous Node
 ↓
...
 ↓
Start
```

Urutan tersebut kemudian dibalik sehingga menghasilkan:

```text
Start → ... → Goal
```

Inilah planned path yang akhirnya diberikan oleh A*.

---

## Output Terminal

Jika path berhasil ditemukan, terminal akan menampilkan informasi seperti:

```text
Path found!
Path length: ...
Visited nodes: ...
Planned path:
(1, 1)
(2, 1)
...
(18, 13)
```

`Path length` menunjukkan jumlah node pada jalur hasil planning.

`Visited nodes` menunjukkan berapa banyak node yang sempat dieksplorasi oleh A* selama proses pencarian.

`Planned path` menampilkan urutan koordinat yang membentuk jalur dari start menuju goal.

Jika tidak ada jalur yang valid, program akan menampilkan:

```text
No path found.
```

---

## Hasil — `planning_result.png`

Hasil visualisasi disimpan ke:

```text
results/planning_result.png
```

Gambar ini memperlihatkan keseluruhan proses planning pada occupancy grid.

Elemen utama pada gambar adalah:

```text
Free Space
Obstacle
Explored Nodes
Planned Path
Start
Goal
```

### Free Space dan Obstacle

Map menggunakan representasi:

```text
Putih → Free Space
Hitam → Obstacle
```

Area putih merupakan cell yang dapat dilalui robot.

Area hitam merupakan cell yang tidak boleh dimasuki.

Obstacle membentuk beberapa penghalang sehingga robot tidak dapat berjalan lurus begitu saja dari start menuju goal.

---

### Explored Nodes

Titik-titik transparan pada map menunjukkan:

```text
Explored Nodes
```

yaitu node yang diperiksa oleh A* selama proses pencarian.

Node-node ini bukan berarti semuanya menjadi bagian dari final path.

Mereka menunjukkan **search space yang sempat dieksplorasi** oleh algoritma.

Secara konseptual:

```text
A* Search
   ↓
Explore many candidate nodes
   ↓
Compare their costs
   ↓
Select one final path
```

Karena menggunakan heuristic, pencarian cenderung diarahkan menuju goal dan tidak harus memeriksa semua free cell pada map.

---

### Planned Path

Garis dengan marker menunjukkan:

```text
Planned Path
```

yaitu jalur akhir yang dipilih A*.

Path tersebut:

- dimulai dari `START`;
- hanya melewati free cell;
- menghindari seluruh obstacle;
- berakhir di `GOAL`.

Karena gerakan dibatasi ke empat arah, trajectory terlihat seperti rangkaian gerakan horizontal dan vertikal.

Secara sederhana:

```text
Start
  ───→
      ↑
      ↑
      ───→
          ↑
          Goal
```

---

### Start dan Goal

Posisi awal ditandai menggunakan marker berbentuk kotak.

Goal ditandai menggunakan marker berbentuk bintang.

Kedua marker tersebut membantu kita melihat masalah planning sebagai:

```text
"Bagaimana mencari urutan cell yang valid
 dari Start menuju Goal?"
```

---

## Planning Berbeda dengan Navigation

Planning dan navigation berkaitan erat, tetapi tidak identik.

Pada hands-on ini, **planning** menghasilkan jalur:

```text
Start
  ↓
A*
  ↓
Path
  ↓
Goal
```

Planning menjawab pertanyaan:

> jalur mana yang sebaiknya dilalui?

Sementara itu, navigation menangani bagaimana robot benar-benar bergerak mengikuti jalur sambil merespons kondisi lingkungan.

Secara sederhana:

```text
Planning
→ menentukan path

Navigation
→ menjalankan gerakan menuju goal
```

Pada sistem robot yang lebih lengkap, keduanya sering digunakan bersama.

---

## Keterbatasan Demo

Demo ini masih menggunakan beberapa asumsi sederhana:

```text
Map sudah diketahui
Robot berada tepat pada sebuah grid cell
Gerakan hanya 4 arah
Setiap gerakan memiliki cost yang sama
Obstacle tidak bergerak
```

Pada sistem yang lebih kompleks, planning dapat mempertimbangkan:

```text
Diagonal Motion
Different Motion Costs
Robot Size
Continuous Space
Dynamic Obstacles
Kinematic Constraints
```

Selain A*, beberapa metode planning lain yang umum digunakan antara lain:

```text
Dijkstra
RRT
RRT*
PRM
D*
```

Namun A* merupakan contoh yang baik untuk memahami konsep dasar search-based path planning.

---

## Inti Konsep

Hands-on ini menunjukkan alur dasar path planning:

```text
Map
 ↓
Start + Goal
 ↓
Search Possible States
 ↓
Evaluate Cost
 ↓
Avoid Obstacles
 ↓
Find Path
```

Planning memungkinkan robot memikirkan **urutan gerakan yang harus dilakukan sebelum benar-benar mengeksekusinya**.

Hal inilah yang membedakan planning dari sekadar gerakan reaktif menuju goal.
