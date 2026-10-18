# Hands-on Imitation Learning

Folder ini berisi mini-project sederhana untuk memperkenalkan **Imitation Learning** melalui metode **Behavior Cloning** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Robot berada pada environment 2D dan harus bergerak dari suatu posisi menuju target. Sebuah **expert policy** terlebih dahulu menghasilkan demonstration data. Neural network kemudian dilatih untuk meniru action expert tersebut.

Secara sederhana:

```text
Expert Policy
     ↓
Demonstration Data
     ↓
Behavior Cloning Training
     ↓
Learned Policy
     ↓
Robot Rollout
```

---

## Struktur Project

```text
Imitation Learning/
├── expert_policy.py
├── generate_demonstrations.py
├── dataset.py
├── policy.py
├── train.py
├── evaluate.py
├── requirements.txt
├── README.md
└── results/
    ├── train_demonstrations.npz
    ├── test_demonstrations.npz
    ├── behavior_cloning_policy.pt
    ├── training_loss.png
    └── evaluation_result.png
```

Folder `results/` akan dibuat otomatis ketika script dijalankan.

---

## Konsep Imitation Learning

Imitation Learning membuat policy belajar dari contoh perilaku expert.

Data demonstration biasanya terdiri dari pasangan:

```text
Observation → Action
```

Pada demo ini, observation adalah:

```text
[robot_x, robot_y, target_x, target_y]
```

sedangkan action adalah velocity 2D:

```text
[vx, vy]
```

Dengan demikian, policy belajar menjawab pertanyaan sederhana:

```text
"Jika robot berada di posisi ini
 dan target berada di posisi itu,
 velocity apa yang seharusnya diberikan?"
```

---

## Demonstration Data

Demonstration data adalah contoh observation-action yang diberikan oleh expert.

Pada robot nyata, demonstration dapat dikumpulkan dari manusia menggunakan teleoperation.

Pada hands-on ini, demonstration dibuat secara otomatis oleh:

```text
expert_policy.py
```

Expert selalu menghasilkan velocity yang mengarah dari posisi robot menuju target.

Secara sederhana:

```text
Robot Position
      +
Target Position
      ↓
Expert Policy
      ↓
Velocity toward Target
```

---

## Behavior Cloning

Behavior Cloning memperlakukan Imitation Learning sebagai **supervised learning**.

Neural network menerima observation dan menghasilkan predicted action.

```text
Observation
    ↓
Neural Network Policy
    ↓
Predicted Action
```

Selama training, predicted action dibandingkan dengan expert action:

```text
Predicted Action
       vs.
Expert Action
       ↓
MSE Loss
```

Model kemudian diperbarui menggunakan backpropagation agar predicted action semakin mendekati expert action.

---

## Penjelasan Setiap File

### `expert_policy.py`

File ini mendefinisikan expert sederhana.

Expert membaca:

```text
robot position
+
target position
```

kemudian menghitung arah menuju target dan menghasilkan velocity maksimum sebesar `1.0`.

Expert ini berperan sebagai demonstrator yang menyediakan label action untuk demonstration dataset.

---

### `generate_demonstrations.py`

Script ini membuat ribuan pasangan observation-action.

Posisi robot dan target dibuat secara acak di environment 2D:

```text
0.0 ≤ x ≤ 10.0
0.0 ≤ y ≤ 10.0
```

Untuk setiap kondisi:

```text
Random Robot Position
        +
Random Target Position
        ↓
Expert Policy
        ↓
Expert Action
```

Dataset kemudian diacak dan dibagi menjadi:

```text
80% Training Data
20% Testing Data
```

Output disimpan ke:

```text
results/train_demonstrations.npz
results/test_demonstrations.npz
```

Masing-masing file berisi:

```text
observations
actions
```

---

### `dataset.py`

File ini mendefinisikan `DemonstrationDataset`.

Class tersebut membaca demonstration file dan mengubah NumPy array menjadi PyTorch tensor.

Setiap sample yang diberikan kepada training loop berbentuk:

```text
observation, expert_action
```

Dengan demikian, `DataLoader` dapat mengambil demonstration secara batch selama training.

---

### `policy.py`

File ini mendefinisikan neural network:

```text
BehaviorCloningPolicy
```

Arsitekturnya:

```text
4 Inputs
   ↓
64 Hidden Units
   ↓
ReLU
   ↓
64 Hidden Units
   ↓
ReLU
   ↓
2 Action Outputs
   ↓
Tanh
```

Empat input adalah:

```text
robot_x
robot_y
target_x
target_y
```

Dua output adalah:

```text
vx
vy
```

Layer `Tanh` membatasi masing-masing output pada rentang sekitar:

```text
-1 sampai 1
```

sesuai dengan skala action expert pada demo ini.

---

### `train.py`

Script ini melatih `BehaviorCloningPolicy` menggunakan training demonstrations.

Alur training:

```text
Observation Batch
      ↓
Policy
      ↓
Predicted Action
      ↓
Compare with Expert Action
      ↓
MSE Loss
      ↓
Backpropagation
      ↓
Update Policy
```

Model menggunakan:

```text
Loss      : Mean Squared Error
Optimizer : Adam
Epochs    : 80
Batch     : 128
```

Setelah training, output disimpan ke:

```text
results/behavior_cloning_policy.pt
results/training_loss.png
```

---

## Hasil 1 — `training_loss.png`

Grafik training disimpan ke:

```text
results/training_loss.png
```

Sumbu horizontal menunjukkan:

```text
Epoch
```

sedangkan sumbu vertikal menunjukkan:

```text
MSE Loss
```

Jika training berjalan dengan baik, loss secara umum akan turun seiring bertambahnya epoch.

Secara konseptual:

```text
High Loss
   ↓
Policy masih jauh dari expert

Low Loss
   ↓
Policy semakin mendekati expert action
```

Loss tidak harus turun secara sempurna pada setiap step. Hal utama yang diperhatikan adalah kecenderungan keseluruhan selama training.

---

### `evaluate.py`

Script ini melakukan dua jenis evaluasi.

Pertama, policy diuji pada testing demonstrations yang tidak digunakan untuk training.

Predicted actions dibandingkan dengan expert actions menggunakan:

```text
Test MSE
```

Semakin kecil MSE, semakin dekat action policy terhadap expert pada data testing.

Kedua, script melakukan rollout dari:

```text
Start = [1.0, 1.0]
```

menuju:

```text
Target = [8.5, 7.5]
```

Rollout dijalankan dua kali:

```text
Expert Policy
Learned Policy
```

Hasilnya kemudian dibandingkan pada satu visualisasi.

Output disimpan ke:

```text
results/evaluation_result.png
```

---

## Hasil 2 — `evaluation_result.png`

Gambar ini membandingkan:

```text
Expert Demonstration
vs.
Learned Policy
```

Elemen utama pada gambar adalah:

```text
Start
Target
Expert Trajectory
Learned Trajectory
```

### Expert Trajectory

Garis expert menunjukkan trajectory yang dihasilkan langsung oleh `expert_policy.py`.

Karena expert selalu memberikan velocity menuju target, trajectory bergerak hampir langsung dari start menuju target.

### Learned Trajectory

Garis learned policy menunjukkan trajectory yang dihasilkan neural network setelah Behavior Cloning training.

Policy ini tidak memanggil expert lagi.

Action sepenuhnya berasal dari:

```text
Observation
    ↓
Learned Neural Network
    ↓
[vx, vy]
```

Jika imitation learning berhasil, learned trajectory seharusnya mengikuti arah yang sangat mirip dengan expert trajectory dan berakhir dekat dengan target.

### Start dan Target

Marker kotak menunjukkan posisi awal robot.

Marker bintang menunjukkan target yang harus dicapai.

Dengan melihat kedua trajectory, kita dapat membandingkan secara visual apakah policy hasil belajar benar-benar meniru perilaku expert ketika digunakan secara berulang dalam rollout.

---

## Test MSE vs. Rollout

Test MSE dan rollout mengukur dua hal yang berbeda.

Test MSE mengevaluasi:

```text
"Apakah action policy mirip dengan action expert
 pada observation dalam dataset?"
```

Sedangkan rollout mengevaluasi:

```text
"Jika action policy digunakan berulang kali,
 apakah robot tetap dapat bergerak menuju target?"
```

Perbedaan ini penting dalam Imitation Learning.

Error kecil pada satu action dapat mengubah posisi robot. Posisi baru tersebut kemudian menjadi observation berikutnya, sehingga error dapat terakumulasi sepanjang rollout.

Fenomena ini merupakan pengantar sederhana menuju masalah **distribution shift** atau **covariate shift** pada Behavior Cloning.

---

## Instalasi

Buat virtual environment:

```bash
python -m venv embodied-ai
source embodied-ai/bin/activate
```

Untuk Windows:

```bash
embodied-ai\Scripts\activate
```

Install dependency:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Project ini ringan dan dapat dijalankan menggunakan CPU.

---

## Cara Menjalankan

Jalankan secara berurutan:

```bash
python generate_demonstrations.py
python train.py
python evaluate.py
```

Workflow lengkapnya:

```text
Generate Demonstrations
        ↓
Save Train/Test Data
        ↓
Train Behavior Cloning Policy
        ↓
Save Model + Training Loss
        ↓
Evaluate on Test Data
        ↓
Expert vs Learned Rollout
        ↓
Save Evaluation Result
```

Setelah seluruh script selesai, folder `results/` akan berisi:

```text
results/
├── train_demonstrations.npz
├── test_demonstrations.npz
├── behavior_cloning_policy.pt
├── training_loss.png
└── evaluation_result.png
```

---

## Keterbatasan Demo

Demo ini sengaja dibuat sederhana.

Beberapa hal yang belum dimodelkan antara lain:

```text
Camera Observation
Robot Dynamics
Obstacle
Collision
Control Delay
Noisy Sensor
Human Demonstration
High-Dimensional Action
```

Expert juga sangat sederhana karena selalu mengetahui posisi robot dan target secara langsung.

Pada robot nyata, Behavior Cloning dapat belajar dari observation yang jauh lebih kompleks seperti image, proprioception, atau multimodal sensor data.

---

## Inti Konsep

Hands-on ini menunjukkan pipeline dasar Imitation Learning:

```text
Expert
  ↓
Demonstrations
  ↓
Supervised Learning
  ↓
Learned Policy
  ↓
Autonomous Rollout
```

Berbeda dari rule-based programming, kita tidak menuliskan seluruh keputusan robot satu per satu.

Policy belajar hubungan antara **observation dan action** dari contoh perilaku expert.
