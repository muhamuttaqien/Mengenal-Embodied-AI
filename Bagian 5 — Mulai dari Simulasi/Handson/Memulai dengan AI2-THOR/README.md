# Bagian 5 — Memulai dengan AI2-THOR

Repository pendamping untuk subbab **Memulai dengan AI2-THOR** pada buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Repository ini mengikuti alur:

```text
AI2-THOR
   ↓
Rooms
   ↓
ManipulaTHOR
   ↓
Kitchen Pick-and-Place Setup
   ↓
Manual Arm Control
   ↓
CNN + DQN Navigation
   ↓
Training dan Evaluation
```

Bagian Reinforcement Learning pada repository ini sengaja menggunakan task **navigation** yang lebih sederhana daripada manipulation. Tujuannya agar pembaca dapat melihat pipeline RL lengkap dengan visual observation sebelum training manipulation dibahas lebih jauh pada Studi Kasus.

---

## 1. Struktur Repository

```text
Bagian_5_Memulai_dengan_AI2THOR/
├── scripts/
│   ├── 01_ai2thor_basics.py
│   ├── 02_rooms_overview.py
│   ├── 03_manipulathor_basics.py
│   ├── 04_kitchen_pick_place_setup.py
│   └── 05_manual_arm_control.py
├── rl/
│   ├── __init__.py
│   ├── ai2thor_nav_env.py
│   ├── dqn_model.py
│   ├── replay_buffer.py
│   ├── training_utils.py
│   ├── train_dqn.py
│   ├── evaluate_dqn.py
│   ├── plot_training.py
│   └── smoke_test.py
├── results/
├── checkpoints/
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 2. Instalasi

Aktifkan environment yang telah dibuat pada subbab sebelumnya:

```bash
# Linux/macOS.
source embodied-ai-env/bin/activate
```

Pada Windows:

```bat
REM Windows.
embodied-ai-env\Scripts\activate
```

Kemudian:

```bash
# Memasang dependency repository.
pip install -r requirements.txt
```

AI2-THOR pertama kali akan mengunduh Unity build yang diperlukan ketika `Controller` dijalankan.

---

# 3. Mengenal AI2-THOR

Jalankan:

```bash
python scripts/01_ai2thor_basics.py
```

Script akan:

```text
Open FloorPlan1
      ↓
Read RGB Observation
      ↓
MoveAhead
      ↓
RotateRight
      ↓
Read Metadata
      ↓
Save Image
```

Bagian utama:

```python
# Membuat controller AI2-THOR.
controller = Controller(scene="FloorPlan1")

# Menjalankan satu navigation action.
event = controller.step(action="MoveAhead")

# Membaca RGB observation.
frame = event.frame

# Membaca metadata environment.
metadata = event.metadata
```

Output image:

```text
results/ai2thor_basics.png
```

---

# 4. Mengenal Rooms

Jalankan:

```bash
python scripts/02_rooms_overview.py
```

Script membuka satu contoh dari empat kategori room:

```text
FloorPlan1   → Kitchen
FloorPlan201 → Living Room
FloorPlan301 → Bedroom
FloorPlan401 → Bathroom
```

Frame disimpan ke:

```text
results/FloorPlan1_Kitchen.png
results/FloorPlan201_LivingRoom.png
results/FloorPlan301_Bedroom.png
results/FloorPlan401_Bathroom.png
```

Ini dapat digunakan untuk memahami bagaimana satu simulator menyediakan banyak jenis environment.

---

# 5. Mengenal ManipulaTHOR

ManipulaTHOR menggunakan:

```python
agentMode="arm"
```

dan menyediakan mobile base, arm, hand camera, serta interaction actions.

Jalankan:

```bash
python scripts/03_manipulathor_basics.py
```

Script akan:

```text
Open Kitchen
    ↓
Read Arm Metadata
    ↓
MoveAgent
    ↓
RotateAgent
    ↓
MoveArm
    ↓
MoveArmBase
```

Beberapa action utama:

```python
# Menggerakkan mobile base.
controller.step(
    action="MoveAgent",
    ahead=0.10,
    right=0.0,
)

# Memutar mobile base.
controller.step(
    action="RotateAgent",
    degrees=15,
)

# Menggerakkan wrist relatif terhadap posisi sekarang.
controller.step(
    action="MoveArm",
    position={"x": 0.0, "y": 0.05, "z": 0.05},
    coordinateSpace="wrist",
)

# Mengatur tinggi arm base.
controller.step(
    action="MoveArmBase",
    y=0.6,
)
```

``

Output image:

```text
results/manipulathor_basics_view.png
```

---

# 6. Kitchen Pick-and-Place Setup

Jalankan:

```bash
python scripts/04_kitchen_pick_place_setup.py
```

Default task:

```text
Scene      : FloorPlan3
Object     : Tomato
Receptacle : Drawer
```

Script memeriksa:

- apakah object tersedia,
- apakah object pickupable,
- posisi object,
- apakah receptacle tersedia,
- posisi receptacle,
- dan metadata arm.

Pilihan dapat diganti:

```bash
python scripts/04_kitchen_pick_place_setup.py \
    --scene FloorPlan20 \
    --object-type Tomato \
    --receptacle-type Drawer
```

Pada tahap ini script **belum menyelesaikan task secara otomatis**. Tujuannya adalah memvalidasi setup sebelum membuat policy atau control sequence.

---

# 7. Manual Control untuk Arm Robot

Jalankan:

```bash
python scripts/05_manual_arm_control.py
```

Command terminal:

```text
w / s → base maju / mundur
a / d → rotate kiri / kanan

j / l → arm kiri / kanan
u / o → arm naik / turun
i / k → arm maju / mundur

r / f → arm base naik / turun

p     → PickupObject
x     → ReleaseObject

info  → tampilkan arm metadata
q     → keluar
```

Script ini membantu kita memahami hubungan:

```text
Human Command
      ↓
ManipulaTHOR Action
      ↓
Robot Motion
      ↓
New Observation
```

---

# 8. Reinforcement Learning: CNN + DQN Navigation

Untuk contoh RL, repository menggunakan agent AI2-THOR biasa dengan tiga discrete actions:

```text
0 → RotateLeft
1 → MoveAhead
2 → RotateRight
```

Policy hanya menerima:

```text
RGB Image
```

Target navigation default adalah:

```text
Fridge
```

Metadata object dan reachable positions dipakai **hanya untuk menentukan goal dan menghitung reward**. Informasi posisi target tidak masuk ke CNN.

Pipeline:

```text
RGB Observation
      ↓
CNN
      ↓
Visual Features
      ↓
DQN
      ↓
Q(Left), Q(Forward), Q(Right)
      ↓
Action
```

---

# 9. Navigation Environment

File:

```text
rl/ai2thor_nav_env.py
```
Environment menggunakan konfigurasi navigation berikut:

```text
gridSize          : 0.25 m
rotateStepDegrees : 90°
snapToGrid        : True
```

Environment melakukan:

```text
reset()
  ↓
Open FloorPlan
  ↓
Find Target Object
  ↓
GetReachablePositions
  ↓
Choose Reachable Goal Near Target
  ↓
Optional Random Start
  ↓
Return RGB State
```

Action:

```python
ACTIONS = [
    "RotateLeft",
    "MoveAhead",
    "RotateRight",
]
```

Reward sederhana:

```text
Setiap timestep       → -0.01
Action gagal          → -0.05
Progress ke goal      → positive / negative shaping
Mencapai goal         → +1.00
```

Success didefinisikan berdasarkan jarak agent terhadap reachable navigation point terdekat dengan target object.

---

# 10. CNN + DQN Model

File:

```text
rl/dqn_model.py
```

Input:

```text
3 × 84 × 84
```

Arsitektur:

```text
RGB Image
   ↓
Conv 3 → 32
   ↓
ReLU
   ↓
Conv 32 → 64
   ↓
ReLU
   ↓
Conv 64 → 64
   ↓
ReLU
   ↓
Flatten
   ↓
Linear → 512
   ↓
ReLU
   ↓
3 Q-values
```

Output:

```text
Q(RotateLeft)
Q(MoveAhead)
Q(RotateRight)
```

---

# 11. Replay Buffer

File:

```text
rl/replay_buffer.py
```

Transition:

```text
(state, action, reward, next_state, done)
```

State disimpan sebagai `uint8` untuk mengurangi penggunaan memory.

Ketika batch diambil:

```text
uint8 [0,255]
      ↓
float32 [0,1]
      ↓
CNN
```

---

# 12. Offline Smoke Test

Sebelum AI2-THOR training, jalankan:

```bash
python -m rl.smoke_test
```

Smoke test tidak membutuhkan AI2-THOR.

Ia memeriksa:

```text
CNN forward pass
Replay Buffer
Batch sampling
DQN optimization
Target network
Checkpoint save/load
```

Jika berhasil:

```text
SMOKE TEST PASSED
```

Repository yang diberikan bersama buku sudah melewati smoke test ini.

---

# 13. Training CNN + DQN

Training utama:

```bash
python -m rl.train_dqn
```

Default:

```text
Scene          : FloorPlan1
Target         : Fridge
Episodes       : 500
Max steps      : 150
Input          : RGB 84×84
Actions        : 3
Replay Buffer  : 50,000
Batch Size     : 32
Gamma          : 0.99
Learning Rate  : 1e-4
Epsilon        : 1.0 → 0.05
Random Start   : enabled
```

Contoh training lebih singkat:

```bash
python -m rl.train_dqn \
    --episodes 100 \
    --max-steps 120
```

Tanpa random starting point:

```bash
python -m rl.train_dqn \
    --no-random-start
```

Target lain:

```bash
python -m rl.train_dqn \
    --scene FloorPlan1 \
    --target-object-type Microwave
```

Output:

```text
checkpoints/dqn_best.pt
checkpoints/dqn_final.pt

results/training_log.csv
results/reward_curve.png
results/success_curve.png
```

---

# 14. Epsilon-Greedy

Pada training:

```text
epsilon tinggi
→ banyak random action

epsilon rendah
→ lebih sering memakai learned Q-values
```

Pemilihan action:

```python
# Explore.
if random.random() < epsilon:
    action = random.randrange(num_actions)

# Exploit.
else:
    action = q_values.argmax(dim=1).item()
```

---

# 15. DQN Update

Target network digunakan untuk membuat learning lebih stabil.

Bellman target:

```text
target =
reward
+
gamma × max Q_target(next_state)
```

Loss menggunakan Smooth L1 / Huber loss:

```python
loss = F.smooth_l1_loss(
    predicted_q,
    target_q,
)
```

Kemudian:

```text
zero_grad
↓
backward
↓
optimizer.step
```

---

# 16. Evaluasi

Setelah training:

```bash
python -m rl.evaluate_dqn \
    --checkpoint checkpoints/dqn_final.pt \
    --episodes 20
```

Evaluation menggunakan:

```text
epsilon = 0
```

sehingga agent selalu memilih action dengan Q-value terbesar.

Output:

```text
results/evaluation_log.csv
```

Metric utama:

```text
Success Rate
Average Reward
Average Episode Length
```

---

# 17. Merekam Evaluation Video

Gunakan:

```bash
python -m rl.evaluate_dqn \
    --checkpoint checkpoints/dqn_final.pt \
    --episodes 5 \
    --record-video
```

Episode pertama akan disimpan sebagai:

```text
results/evaluation_episode_000.mp4
```

Video membantu melihat apakah agent benar-benar belajar navigation yang masuk akal, bukan sekadar menghasilkan reward tinggi.

---

# 18. Plot Training

Jika ingin membuat ulang grafik:

```bash
python -m rl.plot_training \
    --log results/training_log.csv
```

Output:

```text
results/reward_curve.png
results/success_curve.png
```

Reward curve menunjukkan perubahan episode reward.

Success curve menggunakan moving average untuk memperlihatkan apakah agent semakin sering mencapai goal.

Repository ini bukan benchmark navigation. Tujuan utamanya adalah memahami bagaimana RGB observation, action, reward, replay buffer, CNN, dan DQN terhubung dalam satu reinforcement learning pipeline menggunakan AI2-THOR.
