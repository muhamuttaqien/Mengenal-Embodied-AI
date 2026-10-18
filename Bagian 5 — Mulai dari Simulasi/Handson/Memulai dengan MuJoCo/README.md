# Bagian 5 — Memulai dengan MuJoCo

Repository pendamping untuk subbagian **Memulai dengan MuJoCo** pada buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Repository ini memperkenalkan MuJoCo dan robosuite melalui robot manipulator **Franka Panda**.

Alur pembelajaran:

```text
MuJoCo
   ↓
robosuite
   ↓
Franka Panda
   ↓
Pick-and-Place
   ↓
Scripted Expert
   ↓
Demonstration Data
   ↓
Inspect & Visualize
   ↓
Siap digunakan untuk Imitation Learning
```

> **Batasan subbagian ini**
>
> Repository ini **tidak melakukan training Imitation Learning**.
> Tujuannya adalah memahami simulator, robot, task, scripted expert, serta proses pengumpulan demonstration data.
>
> Training policy, inference, rollout learned policy, dan evaluasi akan dibahas lebih lengkap pada bagian **Studi Kasus**.

---

## 1. Struktur Repository

```text
Bagian_5_Memulai_dengan_MuJoCo/
├── scripts/
│   ├── 01_mujoco_basics.py
│   ├── 02_run_franka_panda.py
│   ├── 03_pick_place_setup.py
│   ├── 04_run_scripted_expert.py
│   ├── 05_collect_demonstrations.py
│   ├── 06_inspect_demonstration.py
│   └── 07_visualize_demonstration.py
│
├── src/
│   ├── expert_policy.py
│   └── observation_utils.py
│
├── data/
│   └── demonstrations/
│
├── results/
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 2. Environment

Gunakan environment utama yang sudah dibuat pada subbagian sebelumnya:

```bash
# Mengaktifkan environment pada Linux/macOS.
source embodied-ai-env/bin/activate
```

Pada Windows:

```bat
REM Mengaktifkan environment.
embodied-ai-env\Scripts\activate
```

Kemudian install dependency:

```bash
# Memasang MuJoCo, robosuite, dan library pendukung.
pip install -r requirements.txt
```

Untuk hands-on ini, versi yang sudah diuji adalah:

```text
MuJoCo    : 3.9.0
robosuite : 1.5.2
```

Karena itu, `requirements.txt` sebaiknya menggunakan versi tersebut:

```text
mujoco==3.9.0
robosuite==1.5.2
numpy
tqdm
matplotlib
```

> **Catatan**
>
> MuJoCo versi yang lebih baru dapat menimbulkan incompatibility dengan robosuite 1.5.2 pada saat robot dibuat. Karena itu, hands-on ini menggunakan MuJoCo 3.9.0 agar environment lebih reproducible.

Cek instalasi:

```bash
# Menampilkan versi MuJoCo.
python -c "import mujoco; print(mujoco.__version__)"

# Menampilkan versi robosuite.
python -c "import robosuite; print(robosuite.__version__)"
```

---

# 3. Mengenal MuJoCo

File:

```text
scripts/01_mujoco_basics.py
```

Jalankan:

```bash
python scripts/01_mujoco_basics.py
```

Script ini membuat sistem sederhana:

```text
World
  ↓
Body
  ↓
Hinge Joint
  ↓
Motor Actuator
```

Bagian penting:

```python
# Membuat model MuJoCo dari MJCF.
model = mujoco.MjModel.from_xml_string(
    MODEL_XML
)

# Membuat data simulasi.
data = mujoco.MjData(
    model
)

# Memberikan command ke motor.
data.ctrl[0] = 0.5

# Menjalankan satu physics step.
mujoco.mj_step(
    model,
    data
)
```

Dua object utama yang perlu dikenali adalah:

```text
MjModel
→ struktur body, joint, actuator, geom, dan parameter physics

MjData
→ qpos, qvel, ctrl, contact, dan state simulasi
```

Script juga membuka MuJoCo Viewer sehingga kita dapat melihat hubungan antara **control command** dan gerakan joint secara langsung.

---

# 4. Mengenal robosuite

MuJoCo merupakan physics engine.

**robosuite** menyediakan abstraction yang lebih tinggi untuk robot manipulation di atas MuJoCo.

Secara sederhana:

```text
robosuite
├── Robot
├── Gripper
├── Controller
├── Task
├── Object
└── Observation
      ↓
    MuJoCo
      ↓
Physics Simulation
```

Dengan robosuite, kita tidak perlu membangun Franka Panda, gripper, meja, controller, dan manipulation task seluruhnya dari awal menggunakan XML.

---

# 5. Menjalankan Franka Panda

File:

```text
scripts/02_run_franka_panda.py
```

Jalankan:

```bash
python scripts/02_run_franka_panda.py
```

Script membuat environment sederhana:

```python
# Membuat environment Lift dengan Franka Panda.
env = suite.make(
    env_name="Lift",
    robots="Panda",
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
)
```

Setelah environment dibuat:

```python
# Reset environment dan mengambil observation awal.
observation = env.reset()
```

Action space dapat diperiksa menggunakan:

```python
# Membaca batas minimum dan maksimum action.
action_low, action_high = env.action_spec
```

Script kemudian mengirim beberapa action sederhana agar kita dapat melihat Franka Panda bergerak.

### Gambar untuk buku

**[GAMBAR]**

**Gambar 5.5. Franka Panda yang dijalankan pada environment robosuite berbasis MuJoCo.**

---

# 6. Mempersiapkan Pick-and-Place Setup

File:

```text
scripts/03_pick_place_setup.py
```

Jalankan:

```bash
python scripts/03_pick_place_setup.py
```

Environment yang digunakan adalah:

```python
# Membuat task pick-and-place dengan satu Can.
env = suite.make(
    env_name="PickPlaceCan",
    robots="Panda",
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    reward_shaping=True,
)
```

Script menampilkan beberapa informasi penting:

```text
Action dimension
Observation keys
End-effector position
Can position
Target position
```

Kita dapat mulai melihat hubungan:

```text
Observation
     ↓
Controller
     ↓
Action
     ↓
Franka Panda
     ↓
MuJoCo Physics
```

### Gambar untuk buku

**[GAMBAR]**

**Gambar 5.6. Setup pick-and-place menggunakan Franka Panda pada robosuite, terdiri dari robot, objek yang akan diambil, dan lokasi tujuan.**

---

# 7. Membuat Scripted Expert

File utama:

```text
src/expert_policy.py
```

Script untuk menjalankannya:

```text
scripts/04_run_scripted_expert.py
```

Jalankan:

```bash
python scripts/04_run_scripted_expert.py
```

Scripted expert menggunakan **finite-state controller**:

```text
APPROACH
   ↓
DESCEND
   ↓
GRASP
   ↓
LIFT
   ↓
MOVE_TO_TARGET
   ↓
PLACE
   ↓
RELEASE
   ↓
RETREAT
```

Contoh prinsip kontrolnya:

```python
# Menghitung error posisi.
delta_position = (
    target_position
    - eef_position
)

# Mengubah error menjadi action.
action[:3] = np.clip(
    delta_position * gain,
    -1.0,
    1.0,
)
```

Untuk gripper:

```python
# Menutup gripper.
CLOSE_GRIPPER = 1.0

# Membuka gripper.
OPEN_GRIPPER = -1.0
```

Controller menggunakan **world coordinate frame** agar posisi end-effector, object, target, dan Cartesian action menggunakan reference frame yang konsisten.

Scripted expert **bukan learned policy**.

Ia merupakan program yang secara eksplisit menentukan urutan tindakan untuk menyelesaikan task.

Pada setup yang telah diuji, scripted expert dapat menyelesaikan task:

```text
PickPlaceCan
→ success = True
```

Contoh progression:

```text
APPROACH
→ DESCEND
→ GRASP
→ LIFT
→ MOVE_TO_TARGET
→ PLACE
→ RELEASE
→ RETREAT
```

---

# 8. Mengumpulkan Demonstration Data

File:

```text
scripts/05_collect_demonstrations.py
```

Untuk mengumpulkan tiga successful demonstrations dengan viewer:

```bash
python scripts/05_collect_demonstrations.py \
    --episodes 3 \
    --render
```

Tanpa viewer:

```bash
python scripts/05_collect_demonstrations.py \
    --episodes 3
```

Pada setiap timestep, kita menyimpan:

```text
observation
action
reward
```

Secara konseptual:

```text
(o0, a0)
(o1, a1)
(o2, a2)
...
(oT, aT)
```

Hanya episode yang berhasil menyelesaikan task yang disimpan.

File demonstration:

```text
data/demonstrations/demo_000.npz
data/demonstrations/demo_001.npz
data/demonstrations/demo_002.npz
...
```

Setiap file berisi:

```text
observations
actions
rewards
success
observation_keys
```

Pasangan:

```text
observation → expert action
```

inilah yang nantinya dapat digunakan sebagai dataset untuk Imitation Learning.

---

# 9. Membaca Demonstration

File:

```text
scripts/06_inspect_demonstration.py
```

Jalankan:

```bash
python scripts/06_inspect_demonstration.py \
    data/demonstrations/demo_000.npz
```

Script menampilkan:

```text
File
Timesteps
Observation shape
Action shape
Reward shape
Success
Total reward
Observation keys
First observation
First action
```

Contohnya:

```text
Observation shape : (T, observation_dim)

Action shape      : (T, 7)
```

dengan `T` merupakan jumlah timestep pada demonstration tersebut.

Script ini membantu kita memastikan bahwa demonstration yang disimpan memiliki struktur yang benar sebelum digunakan sebagai dataset pembelajaran.

---

# 10. Visualisasi Demonstration

File:

```text
scripts/07_visualize_demonstration.py
```

Jalankan:

```bash
python scripts/07_visualize_demonstration.py \
    data/demonstrations/demo_000.npz
```

Script membuat visualisasi dari demonstration yang telah dikumpulkan.

Visualisasi mencakup:

```text
Trajectory End-Effector
Trajectory Can
Perubahan Ketinggian Object
Reward sepanjang Episode
```

Hasil disimpan ke:

```text
results/demo_000_visualization.png
```

Visualisasi ini membantu kita melihat bagaimana scripted expert menyelesaikan task tanpa harus selalu menjalankan kembali simulator.

---

# 11. Observation yang Disimpan

Utility untuk mengolah observation berada pada:

```text
src/observation_utils.py
```

Beberapa numeric observation yang digunakan adalah:

```text
robot0_joint_pos
robot0_joint_vel
robot0_eef_pos
robot0_eef_quat
robot0_gripper_qpos
Can_pos
Can_quat
```

Nilai tersebut digabung menjadi satu observation vector:

```text
Joint State
+
End-Effector State
+
Gripper State
+
Object State
        ↓
Observation Vector
```

Dengan demikian, setiap timestep menghasilkan satu pasangan:

```text
Observation Vector
        +
Expert Action
```

yang dapat disimpan sebagai demonstration data.

---

# 12. Bagaimana Data Ini Digunakan untuk Imitation Learning?

Sampai tahap ini kita sudah memiliki:

```text
MuJoCo + robosuite
        ↓
Franka Panda
        ↓
Pick-and-Place
        ↓
Scripted Expert
        ↓
Successful Demonstrations
        ↓
Observation-Action Dataset
```

Nantinya sebuah robot policy dapat belajar mapping:

```text
Observation
     ↓
Learned Policy
     ↓
Predicted Action
```

Secara sederhana:

```text
πθ(o_t) → â_t
```

dan proses training mencoba membuat:

```text
â_t ≈ a_t
```

dengan `a_t` merupakan action yang sebelumnya diberikan oleh scripted expert.

Setelah training selesai:

```text
MuJoCo
   ↓
Observation
   ↓
Learned Policy
   ↓
Action
   ↓
MuJoCo
```

Scripted expert tidak lagi dibutuhkan ketika policy menjalankan task secara mandiri.

Namun **training tersebut sengaja tidak disertakan pada repository ini**.

Implementasi lengkap yang mencakup:

```text
Dataset Preparation
Training
Validation
Policy Inference
Rollout
Success Evaluation
```

akan dibahas pada bagian **Studi Kasus**.

---

# 13. Urutan Praktik yang Direkomendasikan

Jalankan script secara berurutan:

```text
01_mujoco_basics.py
        ↓
02_run_franka_panda.py
        ↓
03_pick_place_setup.py
        ↓
04_run_scripted_expert.py
        ↓
05_collect_demonstrations.py
        ↓
06_inspect_demonstration.py
        ↓
07_visualize_demonstration.py
```

Progression pembelajarannya adalah:

```text
Physics
   ↓
Robot
   ↓
Task
   ↓
Expert
   ↓
Demonstration
   ↓
Inspect
   ↓
Visualize
   ↓
Ready for Imitation Learning
```

---

# 14. Catatan Penting

Repository ini merupakan **pengenalan simulator dan robot-learning data pipeline**, bukan benchmark policy.

Tujuan utamanya adalah memahami bagaimana sebuah task robot learning dapat dipersiapkan:

```text
Simulator
    ↓
Robot
    ↓
Task
    ↓
Controller
    ↓
Scripted Expert
    ↓
Demonstrations
    ↓
Dataset
```

Beberapa warning robosuite seperti:

```text
No private macro file found
Could not import robosuite_models
Could not load the mink-based whole-body IK
```

tidak menghalangi hands-on Franka Panda pada repository ini selama environment dan task dapat berjalan dengan baik.

Hal yang lebih penting adalah memastikan versi dependency sesuai:

```text
MuJoCo 3.9.0
robosuite 1.5.2
```

dan scripted expert dapat menghasilkan successful demonstration.

Setelah memahami pipeline ini, kita akan jauh lebih siap ketika masuk ke bagian **Studi Kasus**, saat demonstration tersebut benar-benar digunakan untuk melatih dan mengevaluasi learned robot policy.
