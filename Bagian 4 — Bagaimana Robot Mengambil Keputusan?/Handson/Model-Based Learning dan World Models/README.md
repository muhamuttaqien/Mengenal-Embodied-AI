# Hands-on Model-Based Learning dan World Models

Folder ini berisi hands-on sederhana **Model-Based Learning dan World Models** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Tujuannya adalah memahami bagaimana agent dapat mempelajari model internal dari environment, menggunakan model tersebut untuk memprediksi perubahan state, lalu melakukan planning dengan membayangkan beberapa kemungkinan masa depan sebelum memilih action.

Secara sederhana:

```text
Environment
    ↓
Collect Transitions
    ↓
Train World Model
    ↓
Predict Next State
    ↓
Imagine Future Rollouts
    ↓
Choose Action
    ↓
Execute in Environment
```

---

## Struktur Project

```text
Model-Based Learning dan World Models/
├── environment.py
├── collect_data.py
├── world_model.py
├── train_world_model.py
├── evaluate_model.py
├── plan_with_model.py
├── requirements.txt
├── README.md
└── results/
    ├── train_transitions.npz
    ├── test_transitions.npz
    ├── world_model.pt
    ├── training_loss.png
    ├── evaluation_result.txt
    └── planning_result.png
```

Folder `results/` akan dibuat otomatis oleh script yang menghasilkan output.

---

## Konsep Utama

### State

Agent bergerak pada environment 2D dengan state:

```text
state = [x, y]
```

Nilai `x` dan `y` berada pada rentang:

```text
0.0 sampai 1.0
```

### Action

Action memiliki dua komponen:

```text
action = [ax, ay]
```

Keduanya berada pada rentang:

```text
-1.0 sampai 1.0
```

Action menentukan arah dan besar gerakan agent.

### True Dynamics

Environment memiliki dynamics sebenarnya yang menentukan:

```text
(state, action)
      ↓
 next_state
```

Selain pengaruh action, environment memiliki sedikit **state-dependent drift**. Karena itu, perubahan state tidak hanya berupa `state + action`.

Dynamics sebenarnya digunakan untuk menghasilkan data training dan untuk mengeksekusi action saat planning.

---

## World Model

World model pada project ini adalah neural network yang belajar dynamics environment dari data.

Input model:

```text
[x, y, ax, ay]
```

Model tidak langsung memprediksi seluruh next state. Model memprediksi:

```text
delta_state = [dx, dy]
```

Kemudian:

```text
predicted_next_state
=
state + predicted_delta
```

Dengan pendekatan ini, model belajar menjawab pertanyaan:

```text
"Jika agent berada pada state ini
 dan melakukan action ini,
 bagaimana state akan berubah?"
```

---

## 1. `environment.py`

Script ini mendefinisikan `PointWorld`, yaitu environment 2D sederhana.

Environment memiliki:

```text
Start Position
Goal Position
Action Scale
State-Dependent Drift
Goal Threshold
Maximum Steps
```

Method utama:

```text
reset()
transition(state, action)
step(action)
```

`transition()` merepresentasikan dynamics environment yang sebenarnya.

`step()` menggunakan dynamics tersebut untuk memperbarui state agent dan menghitung reward.

---

## 2. `collect_data.py`

Script ini membuat transition dataset dari environment.

Jalankan:

```bash
python collect_data.py
```

Script membuat banyak pasangan state dan action secara acak:

```text
state
+
action
↓
true environment dynamics
↓
next_state
```

Setiap transition berisi:

```text
state
action
next_state
```

Dataset kemudian diacak dan dibagi menjadi training dan testing data.

Output:

```text
results/train_transitions.npz
results/test_transitions.npz
```

Dengan konfigurasi default:

```text
Total transitions    : 8000
Training transitions : 6400
Testing transitions  : 1600
```

---

## 3. `world_model.py`

Script ini mendefinisikan neural network `DynamicsModel`.

Arsitektur sederhananya:

```text
State + Action
      ↓
4 inputs
      ↓
Linear 64
      ↓
ReLU
      ↓
Linear 64
      ↓
ReLU
      ↓
Linear 2
      ↓
Predicted Delta State
```

Output berupa:

```text
[dx, dy]
```

Method:

```text
predict_next_state()
```

mengubah predicted delta menjadi predicted next state.

---

## 4. `train_world_model.py`

Script ini melatih world model menggunakan transition dataset.

Jalankan:

```bash
python train_world_model.py
```

Target training dihitung sebagai:

```text
target_delta
=
next_state - state
```

Model kemudian belajar memprediksi `target_delta` menggunakan **Mean Squared Error (MSE)**.

Alur training:

```text
Training Transitions
      ↓
State + Action
      ↓
Dynamics Model
      ↓
Predicted Delta
      ↓
Compare with True Delta
      ↓
MSE Loss
      ↓
Backpropagation
```

Output:

```text
results/world_model.pt
results/training_loss.png
```

`world_model.pt` menyimpan parameter trained dynamics model.

---

## Hasil — `training_loss.png`

Grafik disimpan ke:

```text
results/training_loss.png
```

Script juga **menampilkan grafik menggunakan Matplotlib** ketika training selesai.

Sumbu horizontal menunjukkan:

```text
Epoch
```

Sumbu vertikal menunjukkan:

```text
MSE Loss
```

Jika model belajar dengan baik, loss seharusnya turun selama training.

Secara konseptual:

```text
High Loss
   \
    \
     \
      \____ Low Loss
```

Penurunan loss menunjukkan bahwa predicted state change semakin dekat dengan state change sebenarnya pada transition dataset.

Setelah melihat grafik, tutup window Matplotlib agar script selesai.

---

## 5. `evaluate_model.py`

Script ini mengevaluasi world model pada testing data yang tidak digunakan saat training.

Jalankan:

```bash
python evaluate_model.py
```

Model menerima:

```text
Test State + Test Action
```

kemudian menghasilkan:

```text
Predicted Next State
```

Prediction dibandingkan dengan:

```text
True Next State
```

Metric utama adalah:

```text
Test Next-State MSE
```

Semakin kecil MSE, semakin dekat prediction model dengan dynamics sebenarnya.

Script juga menampilkan beberapa contoh:

```text
State
Action
True Next State
Predicted Next State
```

Hasil evaluasi disimpan sebagai:

```text
results/evaluation_result.txt
```

Dengan demikian, hasil evaluasi tetap tersedia setelah terminal ditutup.

---

## 6. `plan_with_model.py`

Script ini menggunakan trained world model untuk planning menuju goal.

Jalankan:

```bash
python plan_with_model.py
```

Planner menggunakan metode sederhana **random shooting**.

Pada setiap timestep:

```text
Current State
     ↓
Generate Many Candidate Action Sequences
     ↓
Imagine Their Futures with World Model
     ↓
Calculate Cost to Goal
     ↓
Choose Best Sequence
     ↓
Execute Only First Action
     ↓
Observe New State
     ↓
Plan Again
```

Pendekatan ini merupakan bentuk sederhana **Model Predictive Control (MPC)**.

---

## Imagined Rollout

Hal penting pada planning adalah agent tidak langsung mencoba seluruh candidate sequence pada environment sebenarnya.

Sebaliknya, agent menggunakan learned world model untuk membayangkan:

```text
Current State
    ↓
Candidate Action 1
    ↓
Predicted State 1
    ↓
Candidate Action 2
    ↓
Predicted State 2
    ↓
...
```

Ini disebut **imagined rollout**.

Dengan imagined rollout, agent dapat membandingkan banyak kemungkinan masa depan sebelum memilih action yang benar-benar dieksekusi.

---

## Random Shooting

Planner membuat sejumlah candidate action sequences secara acak.

Parameter utamanya:

```text
HORIZON = 8
NUM_CANDIDATES = 512
```

Artinya, pada setiap planning step terdapat 512 candidate sequence dan masing-masing dibayangkan sampai 8 langkah ke depan.

Untuk setiap candidate, planner menghitung cumulative distance menuju goal.

Candidate dengan cost terkecil dipilih.

Namun hanya action pertama yang dijalankan pada environment sebenarnya.

Setelah state aktual berubah, planning dilakukan kembali.

---

## Hasil — `planning_result.png`

Visualisasi planning disimpan ke:

```text
results/planning_result.png
```

Script juga **menampilkan gambar menggunakan Matplotlib** ketika planning selesai.

Elemen utama pada gambar adalah:

```text
Start
Goal
Executed Trajectory
```

### Start

Marker kotak menunjukkan posisi awal agent.

### Goal

Marker bintang menunjukkan posisi tujuan.

### Executed Trajectory

Garis dengan marker menunjukkan state yang benar-benar dilalui agent pada environment sebenarnya.

Trajectory ini bukan hanya rollout yang dibayangkan oleh model.

Ini adalah hasil dari proses berulang:

```text
Imagine
  ↓
Choose Action
  ↓
Execute
  ↓
Observe Actual State
  ↓
Imagine Again
```

Jika planning berhasil, trajectory akan berakhir cukup dekat dengan goal sehingga memenuhi `goal_threshold`.

Setelah melihat visualisasi, tutup window Matplotlib agar script selesai.

---

## World Model vs. Environment Sebenarnya

Project ini sengaja membedakan dua komponen:

```text
True Environment Dynamics
vs.
Learned World Model
```

Environment sebenarnya menentukan apa yang benar-benar terjadi ketika action dieksekusi.

World model hanya mencoba memprediksi apa yang akan terjadi.

Karena world model tidak sempurna:

```text
Predicted Future
≠
Actual Future
```

secara persis.

Inilah alasan mengapa planner melakukan planning ulang setelah setiap action.

---

## Model-Based vs. Model-Free

Secara sederhana, model-free learning mencoba mempelajari:

```text
State
 ↓
Which Action Should I Take?
```

Sementara model-based learning juga mempelajari:

```text
State + Action
      ↓
What Will Happen Next?
```

World model memberi agent kemampuan untuk melakukan prediction sebelum bertindak.

---

## Menjalankan Seluruh Workflow

Install dependency:

```bash
pip install -r requirements.txt
```

Kemudian jalankan secara berurutan:

```bash
python collect_data.py
python train_world_model.py
python evaluate_model.py
python plan_with_model.py
```

Project ini cukup ringan dan dapat dijalankan menggunakan CPU.

Setelah seluruh workflow selesai, folder hasil akan berisi:

```text
results/
├── train_transitions.npz
├── test_transitions.npz
├── world_model.pt
├── training_loss.png
├── evaluation_result.txt
└── planning_result.png
```

---

## Keterbatasan Demo

World model pada hands-on ini masih sangat sederhana.

Model hanya memprediksi:

```text
2D State Dynamics
```

Belum ada:

```text
Image Observation
Latent Representation
Reward Model
Termination Model
Uncertainty Estimation
Stochastic Dynamics
Long-Horizon Latent Prediction
```

World model modern pada Embodied AI dapat mempelajari representasi yang jauh lebih kompleks dari camera, robot state, language, dan action.

---

## Inti Konsep

Hands-on ini memperlihatkan pipeline dasar Model-Based Learning:

```text
Experience
   ↓
Learn Dynamics
   ↓
Predict Future
   ↓
Compare Possible Actions
   ↓
Plan
   ↓
Act
```

Ide utamanya adalah bahwa agent tidak hanya belajar **apa yang harus dilakukan**, tetapi juga membangun model internal tentang **apa yang mungkin terjadi jika suatu action dilakukan**.
