# Bagian 5 — Memulai dengan Isaac Sim

Repository pendamping untuk subbab **Memulai dengan Isaac Sim** pada buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Repository ini sengaja dibuat lebih sederhana dibandingkan bagian MuJoCo dan AI2-THOR.

Tujuannya mengenalkan empat hal utama:

```text
Isaac Sim
   ↓
USD Stage
   ↓
Franka Panda
   ↓
Joint Control
   ↓
Dual-Robot Coordination
```

Kita tidak melakukan machine learning, pengumpulan dataset, atau task manipulation kompleks pada bagian ini.

---

## 1. Struktur Repository

```text
Bagian_5_Memulai_dengan_Isaac_Sim/
├── scripts/
│   ├── 01_create_scene.py
│   ├── 02_load_franka.py
│   ├── 03_move_franka_joints.py
│   └── 04_dual_franka.py
├── results/
├── .gitignore
└── README.md
```

---

## 2. Environment

Gunakan environment Isaac Sim yang sudah dibuat pada subbagian **Menyiapkan Development Environment**.

Contoh:

```bash
# Mengaktifkan environment Isaac Sim.
source isaacsim-env/bin/activate
```

Kemudian pastikan Isaac Sim dapat dibuka:

```bash
# Membuka aplikasi Isaac Sim.
isaacsim
```

Repository ini telah diuji menggunakan **Isaac Sim 6.2** melalui Python package di virtual environment.

Jika Isaac Sim dipasang sebagai Python package, script dapat dijalankan dengan:

```bash
python path/to/script.py
```

Contoh:

```bash
python scripts/01_create_scene.py
```

Pada script di repository ini, `SimulationApp` dijalankan dengan opsi:

```python
"extra_args": ["--reset-user"]
```

Opsi tersebut digunakan agar script tidak terganggu oleh konfigurasi user Isaac Sim yang tersimpan sebelumnya.

---

# 3. Script 1 — Membuat Scene Sederhana

File:

```text
scripts/01_create_scene.py
```

Jalankan:

```bash
python scripts/01_create_scene.py
```

Script ini memperkenalkan:

```text
SimulationApp
      ↓
USD Stage
      ↓
Ground Plane
      ↓
Lighting
      ↓
Simulation Loop
```

Bagian pertama:

```python
# Import SimulationApp terlebih dahulu.
from isaacsim.simulation_app import SimulationApp

# Membuka Isaac Sim.
simulation_app = SimulationApp(
    {
        "headless": False,
        "width": 1280,
        "height": 720,
        "extra_args": ["--reset-user"],
    }
)
```

`headless=False` berarti graphical interface Isaac Sim akan ditampilkan.

Setelah aplikasi aktif, kita baru mengimpor API Isaac Sim lainnya:

```python
import isaacsim.core.experimental.utils.stage as stage_utils

from isaacsim.core.experimental.objects import GroundPlane
```

Kemudian membuat stage:

```python
# Membuat USD stage baru.
stage_utils.create_new_stage()

# Menambahkan ground plane.
GroundPlane(
    "/World/GroundPlane",
    positions=[
        0.0,
        0.0,
        0.0,
    ],
)
```

Scene juga diberi `DomeLight` dan `DistantLight` agar object terlihat jelas pada viewport.

Simulasi kemudian dijalankan menggunakan physics dan rendering loop.

Konsep utamanya:

```text
Scene
  ↓
Stage
  ↓
Object
  ↓
Lighting
  ↓
Physics / Rendering
```

---

# 4. Script 2 — Memasukkan Franka Panda

File:

```text
scripts/02_load_franka.py
```

Jalankan:

```bash
python scripts/02_load_franka.py
```

Script mengambil Franka Panda dari asset library Isaac Sim.

Path asset:

```text
/Isaac/Robots_Multiphysics/
FrankaRobotics/FrankaPanda/
franka/franka.usda
```

Robot kemudian direferensikan ke:

```text
/World/Franka
```

Secara sederhana:

```text
Isaac Sim Asset Library
        ↓
Franka Panda USD
        ↓
/World/Franka
```

Robot dibungkus menggunakan `Articulation`:

```python
# Membuat articulation wrapper.
franka = Articulation(
    "/World/Franka"
)
```

`Articulation` digunakan untuk membaca dan mengontrol robot yang memiliki beberapa joint.

Sebelum membaca state robot, simulation timeline dijalankan terlebih dahulu:

```python
app_utils.play()

app_utils.update_app(
    steps=30
)
```

Langkah ini diperlukan agar physics articulation aktif.

Script juga menampilkan:

```text
Number of DoFs
Joint names
Current joint positions
```

Franka Panda yang digunakan memiliki **9 DoF**:

```text
7 arm joints
+
2 finger joints
=
9 DoFs
```

Kamera juga otomatis diarahkan ke robot agar Franka langsung terlihat jelas ketika viewport terbuka.

---

# 5. Script 3 — Menggerakkan Joint Franka

File:

```text
scripts/03_move_franka_joints.py
```

Jalankan:

```bash
python scripts/03_move_franka_joints.py
```

Script ini menggerakkan joint Franka menuju pose target.

Contoh target:

```python
target_positions = np.array(
    [
        [
            0.0,
            -0.7,
            0.0,
            -2.0,
            0.0,
            1.5,
            0.8,
            0.04,
            0.04,
        ]
    ],
    dtype=np.float32,
)
```

Target dikirim melalui articulation:

```python
franka.set_dof_position_targets(
    current_target
)
```

Agar gerakan mudah diamati, target tidak diberikan sekaligus. Posisi target diinterpolasi secara bertahap dari pose awal menuju pose akhir.

Secara sederhana:

```text
Initial Joint Position
        ↓
Interpolation
        ↓
Joint Position Target
        ↓
Articulation
        ↓
Physics Simulation
        ↓
Robot Motion
```

Gerakan dibuat sekitar **10 detik** sehingga perubahan konfigurasi Franka dapat diamati dengan jelas.

Script juga mencetak progress dan posisi joint selama robot bergerak.

---

# 6. Script 4 — Dua Franka Panda

File:

```text
scripts/04_dual_franka.py
```

Jalankan:

```bash
python scripts/04_dual_franka.py
```

Script ini memperluas contoh sebelumnya dengan menambahkan **dua Franka Panda** dalam satu scene.

Kedua robot ditempatkan saling berhadapan:

```text
Franka Left   →   ←   Franka Right
```

Robot pertama ditempatkan di sisi kiri:

```text
(-0.75, 0.0, 0.0)
```

Robot kedua ditempatkan di sisi kanan:

```text
(+0.75, 0.0, 0.0)
```

Robot kanan kemudian diputar 180 derajat terhadap sumbu Z agar kedua robot saling berhadapan.

Kedua robot dapat dibungkus dalam satu articulation expression:

```python
robots = Articulation(
    "/World/Franka_.*"
)
```

Dengan demikian, posisi joint kedua robot dapat dibaca sebagai satu array:

```text
Robot 1 → 9 DoFs
Robot 2 → 9 DoFs
```

dan target keduanya dapat dikirim secara bersamaan:

```python
robots.set_dof_position_targets(
    current_target
)
```

Contoh target koordinasi:

```python
coordinated_target = np.array(
    [
        left_target,
        right_target,
    ],
    dtype=np.float32,
)
```

Secara sederhana:

```text
Franka Left State      Franka Right State
        ↓                       ↓
        └──── Coordinated Target ────┘
                     ↓
                Articulation
                     ↓
             Physics Simulation
                     ↓
          Two-Robot Coordinated Motion
```

Kedua Franka bergerak secara bersamaan menuju pose tengah, menahan pose sebentar, lalu kembali ke pose awal.

Contoh ini belum merupakan **bimanual manipulation policy** penuh karena belum terdapat shared object atau manipulation task. Namun, contoh ini memperlihatkan bagaimana Isaac Sim dapat digunakan untuk menyiapkan scene dengan beberapa robot dan menjalankan coordinated joint motion.

---

# 7. Urutan Praktik

Jalankan script secara berurutan:

```text
01_create_scene.py
        ↓
02_load_franka.py
        ↓
03_move_franka_joints.py
        ↓
04_dual_franka.py
```

Progression:

```text
Scene
  ↓
Robot
  ↓
Joint Control
  ↓
Dual-Robot Coordination
```

Dengan empat script ini, pembaca mendapatkan gambaran awal tentang bagaimana scene, robot, articulation, joint control, dan multi-robot setup digunakan di Isaac Sim.

---

# 8. Mengapa Tidak Dibuat Lebih Kompleks?

Isaac Sim memiliki banyak kemampuan lain:

```text
Camera
Depth Sensor
LiDAR
ROS 2
Synthetic Data
Robot Manipulation
Motion Planning
Reinforcement Learning
Sim-to-Real
```

Namun Isaac Sim juga memiliki API yang luas dan membutuhkan resource komputasi yang relatif besar.

Pada bagian pengantar ini, fokus kita hanya memahami pola dasar:

```text
Environment
     ↓
Robot State
     ↓
Control
     ↓
Physics
     ↓
New Robot State
```

Pada contoh dua Franka, pola tersebut diperluas menjadi:

```text
Environment
     ↓
Multiple Robot States
     ↓
Coordinated Control
     ↓
Physics
     ↓
New Robot States
```

Pembahasan yang lebih kompleks seperti inverse kinematics, motion planning, sensor simulation, reinforcement learning, atau bimanual manipulation policy dapat dilakukan pada eksperimen lanjutan.

---

# 9. Catatan Versi

Kode repository ini telah disesuaikan dan diuji menggunakan:

```text
Isaac Sim 6.2
```

Beberapa bagian menggunakan experimental API Isaac Sim, antara lain:

```text
isaacsim.core.experimental.objects
isaacsim.core.experimental.prims
isaacsim.core.experimental.utils
```

Isaac Sim berkembang cukup cepat sehingga nama module atau API dapat berubah pada versi yang lebih baru.

Jika menggunakan versi berbeda, cocokkan kode dengan dokumentasi resmi versi Isaac Sim yang terpasang.
