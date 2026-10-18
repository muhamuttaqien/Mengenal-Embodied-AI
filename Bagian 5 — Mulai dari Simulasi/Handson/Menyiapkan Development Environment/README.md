# Bagian 5 — Menyiapkan Development Environment

Repository pendamping untuk subbagian **Menyiapkan Development Environment** pada buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Repository ini tidak hanya memeriksa apakah instalasi berhasil, tetapi juga memberikan **first look** singkat terhadap tiga simulator yang akan digunakan pada Bagian 5:

- **MuJoCo** untuk memahami model, state, control, physics step, dan viewer.
- **AI2-THOR** untuk memahami scene, visual observation, action, metadata, dan interaction.
- **NVIDIA Isaac Sim** untuk memahami aplikasi simulator, stage, scene, physics/render loop, dan workflow Python.

---

## 1. Struktur Repository

```text
Bagian_5_Development_Environment_v2/
├── scripts/
│   ├── 01_test_environment.py
│   ├── 02_mujoco_first_steps.py
│   ├── 03_ai2thor_first_steps.py
│   └── 04_isaacsim_first_steps.py
├── results/
├── requirements-main.txt
├── setup_main_env.sh
├── setup_isaacsim_env.sh
├── .gitignore
└── README.md
```

Folder `results/` digunakan untuk menyimpan output sederhana dari hands-on, misalnya frame RGB dari AI2-THOR.

---

# 2. Konsep Environment yang Digunakan

Pada buku ini kita sengaja menggunakan dua environment:

```text
embodied-ai-env
├── NumPy
├── Matplotlib
├── Pillow
├── PyTorch
├── MuJoCo
└── AI2-THOR

isaacsim-env
└── NVIDIA Isaac Sim
```

Secara teknis, berbagai simulator dapat saja dipasang pada satu virtual environment yang sama. Namun selama proses pembelajaran ini, environment dipisahkan untuk:

- mengurangi risiko konflik package,
- mengurangi masalah perbedaan versi Python,
- mempermudah troubleshooting,
- dan membuat tata kelola dependency lebih rapi.

---

# 3. Menyiapkan Environment Utama

Environment utama digunakan untuk Python dasar, MuJoCo, dan AI2-THOR.

## Linux / macOS

```bash
# Membuat virtual environment bernama embodied-ai-env.
python3 -m venv embodied-ai-env

# Mengaktifkan virtual environment.
source embodied-ai-env/bin/activate

# Memperbarui pip.
python -m pip install --upgrade pip

# Memasang seluruh dependency utama.
pip install -r requirements-main.txt
```

Kita juga menyediakan script otomatis:

```bash
# Membuat environment dan memasang dependency secara otomatis.
bash setup_main_env.sh
```

## Windows

```bat
REM Membuat virtual environment.
python -m venv embodied-ai-env

REM Mengaktifkan virtual environment.
embodied-ai-env\Scripts\activate

REM Memperbarui pip.
python -m pip install --upgrade pip

REM Memasang dependency utama.
pip install -r requirements-main.txt
```

Jika environment berhasil aktif, terminal biasanya menampilkan:

```text
(embodied-ai-env)
```

---

# 4. Menguji Environment Dasar

Jalankan:

```bash
# Menjalankan pemeriksaan library dasar.
python scripts/01_test_environment.py
```

Script akan menampilkan versi Python, NumPy, PyTorch, Pillow, Matplotlib, dan status CUDA.

Contoh output:

```text
Python         : 3.x.x
NumPy          : ...
PyTorch        : ...
Pillow         : ...
Matplotlib     : ...
CUDA available : False

Environment ready!
```

`CUDA available: False` tidak menjadi masalah pada tahap ini. MuJoCo dasar dan Python hands-on tidak membutuhkan CUDA.

---

# 5. First Look: MuJoCo

MuJoCo adalah simulator yang sangat kuat untuk **physics, dynamics, control, dan robot manipulation**.

Pada first look ini kita akan melihat empat konsep penting:

```text
Model
  ↓
Data / State
  ↓
Control
  ↓
mj_step()
  ↓
Viewer
```

Jalankan:

```bash
# Menjalankan contoh MuJoCo pertama.
python scripts/02_mujoco_first_steps.py
```

Script membuat pendulum sederhana dengan:

- satu body,
- satu hinge joint,
- satu motor actuator,
- dan viewer interaktif.

Beberapa baris penting:

```python
# Mengubah XML menjadi model MuJoCo.
model = mujoco.MjModel.from_xml_string(MODEL_XML)

# Membuat state runtime dari model.
data = mujoco.MjData(model)

# Memberikan control ke actuator pertama.
data.ctrl[0] = 0.5

# Memajukan simulasi satu physics step.
mujoco.mj_step(model, data)
```

Konsep yang perlu diperhatikan:

- `MjModel` menyimpan struktur model dan parameter simulator.
- `MjData` menyimpan state yang berubah selama simulasi.
- `data.qpos` berisi posisi joint.
- `data.qvel` berisi velocity joint.
- `data.ctrl` berisi control input.
- `mujoco.mj_step()` memajukan physics simulation satu timestep.

MuJoCo juga menyediakan viewer bawaan:

```bash
# Membuka MuJoCo interactive viewer.
python -m mujoco.viewer
```

> **Untuk screenshot buku:** jalankan viewer atau script first look, lalu ambil gambar window MuJoCo.

---

# 6. First Look: AI2-THOR

AI2-THOR berbeda dari MuJoCo. Simulator ini berfokus pada **agent yang berinteraksi dengan lingkungan rumah virtual**.

Konsep dasarnya:

```text
Scene
  ↓
Controller
  ↓
Action
  ↓
Event
  ├── RGB Observation
  └── Metadata
```

Jalankan:

```bash
# Membuka FloorPlan1 dan menjalankan beberapa action.
python scripts/03_ai2thor_first_steps.py
```

Script melakukan beberapa hal:

1. Membuka `FloorPlan1`.
2. Membaca posisi agent.
3. Menyimpan RGB observation awal.
4. Menjalankan `MoveAhead`.
5. Menjalankan `RotateRight`.
6. Membaca metadata.
7. Menampilkan beberapa objek yang terlihat.
8. Menyimpan RGB observation akhir.

Baris utama:

```python
# Membuat controller dan membuka scene.
controller = Controller(scene="FloorPlan1")

# Mengirim action ke agent.
event = controller.step(action="MoveAhead")

# Mengambil RGB observation.
frame = event.frame

# Membaca metadata environment.
metadata = event.metadata
```

Output image disimpan ke:

```text
results/ai2thor_before.png
results/ai2thor_after.png
```

Konsep penting:

- `Controller` adalah antarmuka utama ke simulator.
- `scene` menentukan environment yang dibuka.
- `step()` mengirim action.
- `event.frame` berisi RGB observation.
- `event.metadata` berisi informasi state environment.

Saat pertama kali digunakan, AI2-THOR dapat mengunduh build simulator yang diperlukan.

> **Untuk screenshot buku:** gunakan scene AI2-THOR yang terbuka ketika script berjalan.

---

# 7. Menyiapkan NVIDIA Isaac Sim

Isaac Sim memiliki dependency dan runtime yang lebih kompleks, sehingga pada buku ini kita menempatkannya pada environment terpisah.

Untuk instalasi Python-package workflow, gunakan Python yang kompatibel dengan versi Isaac Sim yang sedang dipakai. Dokumentasi Isaac Sim terbaru menggunakan Python 3.12 untuk instalasi Python-package.

Contoh:

```bash
# Membuat environment khusus Isaac Sim.
python3.12 -m venv isaacsim-env

# Mengaktifkan environment.
source isaacsim-env/bin/activate

# Memperbarui pip.
python -m pip install --upgrade pip

# Memasang Isaac Sim dan extension cache dari NVIDIA PyPI.
pip install "isaacsim[all,extscache]" --extra-index-url https://pypi.nvidia.com
```

Atau jalankan:

```bash
# Membuat environment Isaac Sim secara otomatis.
bash setup_isaacsim_env.sh
```

Setelah instalasi:

```bash
# Membuka aplikasi Isaac Sim.
isaacsim
```

---

# 8. First Look: Isaac Sim

Isaac Sim menggunakan konsep **SimulationApp** dan **stage** dari Omniverse.

Workflow dasarnya:

```text
SimulationApp
      ↓
Stage
      ↓
Scene Object
      ↓
Physics / Rendering Step
      ↓
SimulationApp.close()
```

Jalankan dari environment Isaac Sim:

```bash
# Menjalankan contoh Isaac Sim pertama.
python scripts/04_isaacsim_first_steps.py
```

Pada standalone installation, script juga dapat dijalankan menggunakan Python bawaan Isaac Sim:

```bash
# Linux: gunakan Python environment bawaan Isaac Sim.
./python.sh scripts/04_isaacsim_first_steps.py
```

Script akan:

- membuka `SimulationApp`,
- membuat stage baru,
- menambahkan ground plane,
- menjalankan beberapa simulation/rendering step,
- lalu menutup aplikasi.

Baris penting:

```python
# Meluncurkan aplikasi Isaac Sim.
simulation_app = SimulationApp({"headless": False})

# Membuat stage kosong.
stage_utils.create_new_stage()

# Menambahkan ground plane ke scene.
GroundPlane("/World/GroundPlane", positions=[0, 0, 0])

# Memajukan physics simulation.
SimulationManager.step()

# Merender frame.
RenderingManager.render()

# Memperbarui aplikasi.
simulation_app.update()
```

Hal yang penting: berbagai import yang berasal dari extension Omniverse dilakukan **setelah `SimulationApp` dibuat**, karena extension tersebut membutuhkan runtime Omniverse yang aktif.

> **Untuk screenshot buku:** jalankan `isaacsim` atau script first look, lalu ambil gambar window Isaac Sim.

---

# 9. Urutan yang Direkomendasikan

Setelah instalasi selesai, jalankan script dengan urutan:

```text
01_test_environment.py
        ↓
02_mujoco_first_steps.py
        ↓
03_ai2thor_first_steps.py
        ↓
04_isaacsim_first_steps.py
```

Tujuannya bukan langsung mempelajari seluruh simulator. Kita hanya ingin memastikan bahwa:

```text
Python environment bekerja
        ↓
MuJoCo dapat menjalankan physics
        ↓
AI2-THOR dapat menghasilkan observation dan action
        ↓
Isaac Sim dapat membuka simulation application
```

Pembahasan lebih lengkap untuk setiap simulator akan dilakukan pada subbagian tersendiri.

---

# 10. Troubleshooting Singkat

### `ModuleNotFoundError`

Pastikan virtual environment sudah aktif:

```bash
# Linux/macOS.
source embodied-ai-env/bin/activate
```

Kemudian install ulang dependency:

```bash
# Memasang dependency dari requirements file.
pip install -r requirements-main.txt
```

### AI2-THOR tidak membuka window

Pastikan sistem memiliki graphical display yang aktif. Pada server/headless environment diperlukan konfigurasi rendering yang berbeda.

### Isaac Sim tidak berjalan

Periksa:

- NVIDIA GPU,
- NVIDIA driver,
- VRAM,
- versi Python,
- dan compatibility requirement versi Isaac Sim yang digunakan.

Isaac Sim jauh lebih berat dibanding MuJoCo dan AI2-THOR, sehingga masalah hardware/driver lebih mungkin muncul pada tahap ini.

---

# 11. Catatan untuk Pembaca

Repository ini sengaja dibuat sederhana. Script-script pada tahap ini hanya bertujuan untuk:

```text
install
→ verify
→ first look
```

Kita belum melakukan robot control yang kompleks. Pada subbagian berikutnya, setiap simulator akan digunakan dalam hands-on yang lebih terarah.
