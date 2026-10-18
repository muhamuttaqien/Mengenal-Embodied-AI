# Bonus Hands-on Reinforcement Learning: Deep Q-Network

Bonus ini memperluas hands-on Q-Learning sebelumnya menjadi **Deep Reinforcement Learning menggunakan Deep Q-Network (DQN)**.

Pada tabular Q-Learning, setiap nilai disimpan langsung pada:

```text
Q-Table
```

Pada DQN, Q-value diperkirakan menggunakan neural network:

```text
State
  ↓
Q-Network
  ↓
Q(UP), Q(RIGHT), Q(DOWN), Q(LEFT)
```

Environment tetap berupa GridWorld sehingga fokus hands-on berada pada perubahan dari **tabular value representation** menjadi **function approximation**.

---

## Struktur Project

```text
Bonus/
├── gridworld.py
├── dqn_agent.py
├── train_dqn.py
├── evaluate_dqn.py
├── requirements.txt
├── README.md
└── results/
    ├── dqn_policy.pt
    ├── training_history.npz
    ├── training_reward.png
    └── evaluation_result.png
```

Folder `results/` dibuat otomatis oleh script.

---

## State untuk Neural Network

State asli GridWorld adalah:

```text
(row, column)
```

Pada bonus ini state dinormalisasi menjadi dua nilai floating-point sekitar rentang 0 sampai 1.

Secara sederhana:

```text
Grid Position
     ↓
Normalization
     ↓
[row_norm, col_norm]
     ↓
Neural Network
```

Normalisasi membuat input neural network berada pada skala yang lebih teratur.

---

## Q-Network

`QNetwork` menggunakan multilayer perceptron sederhana:

```text
2-D State
   ↓
Linear 64
   ↓
ReLU
   ↓
Linear 64
   ↓
ReLU
   ↓
4 Q-Values
```

Empat output mewakili:

```text
UP
RIGHT
DOWN
LEFT
```

Saat exploitation, action dengan Q-value terbesar dipilih.

---

## Experience Replay

Setiap transition disimpan sebagai:

```text
(state, action, reward, next_state, done)
```

ke dalam **Replay Buffer**.

Training kemudian mengambil mini-batch secara acak dari pengalaman yang sudah tersimpan.

Secara sederhana:

```text
Environment Interaction
        ↓
Replay Buffer
        ↓
Random Mini-Batch
        ↓
DQN Update
```

Ini membantu mengurangi korelasi kuat antara pengalaman yang berurutan.

---

## Target Network

DQN menggunakan dua network:

```text
Online Network
Target Network
```

Online Network diperbarui pada setiap training step.

Target Network tidak diperbarui setiap step. Parameternya disalin dari Online Network secara berkala.

Tujuannya adalah membuat target Q-value lebih stabil selama training.

---

## Penjelasan File

### `gridworld.py`

Mendefinisikan GridWorld yang sama dengan hands-on utama, tetapi state dikembalikan dalam bentuk normalized vector agar dapat diberikan ke neural network.

### `dqn_agent.py`

Berisi:

```text
QNetwork
ReplayBuffer
DQNAgent
Epsilon-Greedy
Online Network Update
Target Network Update
```

### `train_dqn.py`

Menjalankan interaction loop DQN:

```text
State
 ↓
Choose Action
 ↓
Environment Step
 ↓
Store Transition
 ↓
Sample Replay Buffer
 ↓
Train Online Network
 ↓
Periodically Update Target Network
```

Output:

```text
results/dqn_policy.pt
results/training_history.npz
results/training_reward.png
```

### `evaluate_dqn.py`

Memuat trained network dan menjalankan greedy rollout tanpa exploration.

Output:

```text
results/evaluation_result.png
```

---

## Instalasi

Install dependency:

```bash
pip install -r requirements.txt
```

Dependency utama:

```text
numpy
matplotlib
torch
```

Training dapat dijalankan menggunakan CPU.

---

## Menjalankan Training

Jalankan:

```bash
python train_dqn.py
```

Terminal menampilkan:

```text
Episode
Reward
Epsilon
Recent Success
```

Selama training, epsilon semakin kecil sehingga agent secara bertahap berpindah dari exploration menuju exploitation.

---


## Menampilkan Hasil Visualisasi

Setiap script yang menghasilkan gambar melakukan dua hal:

1. menyimpan gambar ke folder `results/`;
2. menampilkan gambar menggunakan Matplotlib ketika script dijalankan.

Contohnya:

```python
plt.savefig(
    OUTPUT_PATH,
    dpi=200,
)

plt.show()
```

Setelah memeriksa gambar, tutup window Matplotlib agar script dapat selesai atau melanjutkan proses berikutnya.

## Hasil 1 — `training_reward.png`

Grafik disimpan ke:

```text
results/training_reward.png
```

Gambar memperlihatkan reward setiap episode dan 50-episode moving average.

Pada awal training, neural network belum memiliki estimasi Q-value yang baik sehingga reward dapat rendah dan tidak stabil.

Jika DQN belajar dengan baik, moving average akan meningkat dan menjadi lebih stabil.

---

## `dqn_policy.pt`

File ini menyimpan parameter trained Online Network.

Berbeda dari Q-Learning utama yang menyimpan:

```text
q_table.npy
```

DQN menyimpan:

```text
Neural Network Weights
```

Inilah perubahan utama dari tabular RL menuju Deep RL.

---

## `training_history.npz`

File ini menyimpan:

```text
rewards
success
losses
```

`losses` menunjukkan error antara predicted Q-value dan target Q-value selama training.

---

## Menjalankan Evaluation

Setelah training selesai, jalankan:

```bash
python evaluate_dqn.py
```

Terminal menampilkan:

```text
Evaluation success
Total reward
Trajectory length
```

---

## Hasil 2 — `evaluation_result.png`

Hasil evaluation disimpan ke:

```text
results/evaluation_result.png
```

Gambar menampilkan:

```text
Obstacles
Start
Goal
DQN Rollout
```

Garis `DQN Rollout` adalah trajectory yang dihasilkan ketika agent selalu memilih action dengan Q-value tertinggi dari neural network.

Jika training berhasil, trajectory harus bergerak dari Start menuju Goal tanpa melewati obstacle.

---

## Q-Learning vs DQN

Perbandingan paling sederhana:

```text
Q-Learning
State → Q-Table → Q-Values

DQN
State → Neural Network → Q-Values
```

Q-table sangat cocok untuk state space kecil dan diskrit.

Neural network lebih fleksibel ketika state menjadi besar, kontinu, atau memiliki dimensi tinggi.

Namun DQN juga menambahkan kompleksitas training seperti Replay Buffer dan Target Network.

---

## Keterbatasan Demo

GridWorld ini masih sangat sederhana.

State hanya terdiri dari dua nilai posisi dan action space hanya memiliki empat pilihan diskrit.

Pada robot nyata, state dapat mencakup:

```text
Camera Image
Joint State
Robot Velocity
Object State
Sensor Reading
```

dan action dapat berupa command motor atau joint secara kontinu.

Karena itu, bonus ini sebaiknya dipahami sebagai pengantar menuju Deep Reinforcement Learning, bukan representasi lengkap robot learning modern.

---

## Inti Konsep

Perubahan terpenting adalah:

```text
Tabular Q-Learning
      ↓
Replace Q-Table
      ↓
Neural Network Q-Function
      ↓
Deep Q-Network
```

DQN menunjukkan bagaimana konsep value-based Reinforcement Learning dapat diperluas menggunakan neural network sebagai function approximator.
