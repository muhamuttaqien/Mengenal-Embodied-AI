# Hands-on Reinforcement Learning

Folder ini berisi hands-on **Reinforcement Learning menggunakan Q-Learning** untuk buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Tujuannya adalah memahami bagaimana agent dapat belajar mengambil keputusan melalui interaksi langsung dengan environment, tanpa demonstration data atau label action yang benar.

Secara sederhana:

```text
State
  ↓
Choose Action
  ↓
Environment
  ↓
Reward + Next State
  ↓
Update Q-Value
  ↓
Repeat
```

---

## Struktur Project

```text
Reinforcement Learning/
├── gridworld.py
├── q_agent.py
├── train.py
├── evaluate.py
├── requirements.txt
├── README.md
├── results/
│   ├── q_table.npy
│   ├── training_history.npz
│   ├── training_reward.png
│   └── evaluation_result.png
└── Bonus/
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

## Environment GridWorld

Environment berupa grid 2D berukuran:

```text
6 × 6
```

Agent memiliki empat action:

```text
0 = UP
1 = RIGHT
2 = DOWN
3 = LEFT
```

State direpresentasikan sebagai:

```text
(row, column)
```

Environment memiliki posisi `Start`, `Goal`, dan beberapa obstacle.

Reward yang digunakan:

```text
Mencapai goal      → +1.00
Langkah biasa      → -0.02
Menabrak dinding   → -0.15
Menabrak obstacle  → -0.25
```

Biaya kecil untuk setiap langkah mendorong agent menemukan jalur yang lebih pendek dan efisien.

---

## Q-Learning

Agent mempelajari nilai:

```text
Q(state, action)
```

Q-value menyatakan seberapa baik suatu action jika dilakukan pada state tertentu.

Update utamanya adalah:

```text
Q(s,a) ← Q(s,a) + α [target - Q(s,a)]
```

Untuk state non-terminal:

```text
target = reward + γ max Q(s', a')
```

Dengan demikian, reward saat ini digabung dengan estimasi reward masa depan.

---

## Exploration dan Exploitation

Agent menggunakan **epsilon-greedy policy**.

Pada awal training:

```text
epsilon tinggi
→ lebih banyak exploration
```

Seiring training:

```text
epsilon turun
→ lebih banyak exploitation
```

Exploration membantu agent mencoba action yang berbeda, sedangkan exploitation menggunakan pengetahuan yang sudah tersimpan pada Q-table.

---

## Penjelasan File

### `gridworld.py`

Mendefinisikan environment, termasuk:

```text
Grid size
Start
Goal
Obstacles
Actions
Rewards
Episode termination
```

Fungsi utama adalah `reset()` dan `step()`.

### `q_agent.py`

Mendefinisikan `QLearningAgent` yang memiliki:

```text
Q-table
Epsilon-greedy action selection
Q-value update
Epsilon decay
```

### `train.py`

Menjalankan ribuan episode interaksi agent dengan environment.

Alurnya:

```text
Reset Environment
      ↓
Select Action
      ↓
Environment Step
      ↓
Receive Reward
      ↓
Update Q-Table
      ↓
Repeat Until Episode Ends
```

Script menghasilkan:

```text
results/q_table.npy
results/training_history.npz
results/training_reward.png
```

### `evaluate.py`

Memuat Q-table hasil training dan menjalankan **greedy rollout** tanpa exploration.

Script juga menampilkan action terbaik untuk hampir setiap cell sebagai panah.

Output:

```text
results/evaluation_result.png
```

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

Install dependency:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Hands-on Q-Learning ini dapat dijalankan menggunakan CPU.

---

## Menjalankan Training

Jalankan:

```bash
python train.py
```

Selama training, terminal menampilkan:

```text
Episode
Total Reward
Epsilon
Recent Success
```

Contohnya:

```text
Episode 0200 | Reward: ... | Epsilon: ... | Recent success: ...%
```

`Recent success` menunjukkan persentase keberhasilan pada 100 episode terakhir.

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

Gambar memperlihatkan dua kurva:

```text
Episode Reward
50-Episode Moving Average
```

### Episode Reward

Kurva tipis menunjukkan total reward setiap episode.

Pada awal training, reward dapat sangat rendah karena agent masih banyak melakukan exploration, menabrak obstacle, atau gagal mencapai goal.

### Moving Average

Kurva moving average membantu melihat tren training dengan lebih jelas.

Jika agent belajar dengan baik, secara umum kita mengharapkan:

```text
Reward rendah dan tidak stabil
        ↓
Reward meningkat
        ↓
Reward lebih stabil
```

Peningkatan reward menunjukkan bahwa agent mulai memilih action yang menghasilkan konsekuensi jangka panjang yang lebih baik.

---

## `q_table.npy`

File ini menyimpan Q-table hasil training.

Bentuknya secara konseptual:

```text
[row, column, action]
```

Untuk setiap state pada grid, terdapat empat Q-value:

```text
Q(UP)
Q(RIGHT)
Q(DOWN)
Q(LEFT)
```

Action dengan nilai terbesar digunakan sebagai action greedy saat evaluation.

---

## `training_history.npz`

File ini menyimpan riwayat:

```text
rewards
lengths
success
```

Data tersebut dapat digunakan untuk analisis training lebih lanjut tanpa harus menjalankan training ulang.

---

## Menjalankan Evaluation

Setelah training selesai, jalankan:

```bash
python evaluate.py
```

Terminal menampilkan:

```text
Evaluation success
Total reward
Trajectory length
```

Evaluation menggunakan policy greedy sehingga epsilon tidak lagi digunakan untuk memilih action acak.

---

## Hasil 2 — `evaluation_result.png`

Hasil disimpan ke:

```text
results/evaluation_result.png
```

Gambar memperlihatkan:

```text
Start
Goal
Obstacles
Learned Policy
Greedy Rollout
```

### Learned Policy

Setiap cell bebas menampilkan panah:

```text
↑  →  ↓  ←
```

Panah menunjukkan action dengan Q-value terbesar pada state tersebut.

Dengan melihat seluruh panah, kita sebenarnya sedang melihat **policy yang dipelajari agent**.

### Greedy Rollout

Garis dengan marker menunjukkan trajectory ketika agent mengikuti learned policy dari Start tanpa exploration.

Jika training berhasil, trajectory akan:

```text
Start
  ↓
Avoid Obstacles
  ↓
Goal
```

Trajectory evaluation lebih penting daripada hanya melihat Q-value karena menunjukkan bagaimana policy benar-benar berperilaku ketika dijalankan.

---

## Perbedaan dengan Imitation Learning

Pada Imitation Learning sebelumnya:

```text
Expert Demonstrations
      ↓
Supervised Learning
      ↓
Learned Policy
```

Agent belajar meniru action expert.

Pada Reinforcement Learning:

```text
Agent
  ↓
Action
  ↓
Environment
  ↓
Reward
  ↓
Learning
```

Tidak ada label yang mengatakan action mana yang benar.

Agent harus menemukan policy melalui trial and error.

---

## Bonus — Deep Q-Network

Folder `Bonus/` memperluas contoh ini dari tabular Q-Learning menjadi **Deep Q-Network (DQN)**.

Perubahan utamanya:

```text
Q-Table
   ↓
Neural Network
```

Bonus juga memperkenalkan:

```text
Experience Replay
Target Network
Mini-Batch Training
```

Baca `Bonus/README.md` untuk penjelasan dan cara menjalankannya.

---

## Inti Konsep

Hands-on ini memperlihatkan ide dasar Reinforcement Learning:

```text
Observe
  ↓
Act
  ↓
Receive Reward
  ↓
Update Value
  ↓
Improve Policy
```

Robot atau agent tidak selalu perlu diberi contoh action yang benar. Dengan reward yang dirancang dengan baik, agent dapat belajar sendiri action mana yang memberikan hasil jangka panjang terbaik.
