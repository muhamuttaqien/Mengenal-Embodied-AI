# Hands-on Vision-Language-Action Models

Project ini memperkenalkan konsep dasar **Vision-Language-Action (VLA)** melalui dua eksperimen:

1. **Mini-VLA** yang dilatih dari demonstration data sintetis.
2. **Bonus OpenVLA-7B** untuk melihat bagaimana pretrained VLA mengubah image dan language instruction menjadi action vector.

Tujuan project ini adalah memahami perubahan dari:

```text
Vision + Language
        ↓
Semantic Understanding
```

menjadi:

```text
Vision + Language
        ↓
Robot Policy
        ↓
Action
```

Mini-VLA di repository ini bersifat **edukasional**. Model ini bukan foundation VLA besar seperti RT-2, OpenVLA, atau π0.

---

# Konsep Utama

## Vision-Language-Action

VLA menerima observation visual dan language instruction lalu menghasilkan action.

```text
RGB Image
+
Language Instruction
        ↓
    VLA Policy
        ↓
    Robot Action
```

Pada Mini-VLA:

```text
Vision Observation
+
Language Instruction
        ↓
      Mini-VLA
        ↓
Target Workspace Cell
+
Gripper Command
```

Contoh:

```text
Instruction:
pick the red block

Action:
target cell = 4
gripper = close
```

---

## Action Representation

Workspace dibagi menjadi grid `3 x 3`.

```text
0   1   2
3   4   5
6   7   8
```

Mini-VLA memprediksi:

```text
target workspace cell
+
gripper command
```

Gripper direpresentasikan sebagai:

```text
0 -> move only
1 -> pick / close gripper
```

Representasi discrete ini dibuat agar konsep VLA mudah dipahami. Robot nyata biasanya menggunakan action representation yang lebih kompleks, misalnya joint command, end-effector pose, atau action chunk.

---

## Demonstration Data

Dataset memiliki format:

```text
(image, instruction) -> action
```

Image berisi:

```text
colored target block
+
gray distractor blocks
+
robot/end-effector marker
```

Instruction dapat berupa:

```text
move to the green block
pick the blue block
```

Action target berisi target workspace cell dan gripper command.

Dataset pada hands-on ini dibuat secara sintetis. Pada sistem nyata, demonstration biasanya berasal dari teleoperation, robot demonstration, atau robot dataset dalam skala besar.

---

## Mini-VLA Architecture

Mini-VLA memiliki tiga bagian utama:

```text
Image
 ↓
Vision Encoder
 ↓
Visual Features
                  \
                   → Multimodal Fusion → Action Heads
                  /
Instruction
 ↓
Language Encoder
 ↓
Language Features
```

Output terdiri dari:

```text
Target Cell Head
+
Gripper Head
```

Target cell dilatih menggunakan **Cross-Entropy Loss**.

Gripper dilatih menggunakan **Binary Cross-Entropy Loss**.

---

# Struktur Project

```text
Vision-Language-Action Models/
├── generate_dataset.py
├── dataset.py
├── vla_model.py
├── train_vla.py
├── evaluate_vla.py
├── colab_vla_demo.ipynb
├── requirements.txt
├── README.md
├── results/
│   ├── train_vla.npz
│   ├── test_vla.npz
│   ├── mini_vla.pt
│   ├── training_history.npz
│   ├── training_loss.png
│   ├── evaluation_metrics.txt
│   └── evaluation_result.png
└── Bonus/
    ├── openvla_inference.py
    ├── visualize_action.py
    ├── colab_openvla_action.ipynb
    ├── requirements.txt
    ├── README.md
    └── results/
```

Semua output yang dihasilkan script disimpan di folder `results/`.

---

# Penjelasan Setiap File

## `generate_dataset.py`

Membuat training dan testing demonstration data sintetis.

Output:

```text
results/train_vla.npz
results/test_vla.npz
```

Terminal juga menampilkan lokasi file:

```text
Training dataset saved to: ...
Testing dataset saved to: ...
```

---

## `dataset.py`

Membaca dataset dan menyiapkan:

```text
RGB image tensor
language tokens
target workspace cell
gripper target
instruction text
```

File ini tidak menghasilkan output baru.

---

## `vla_model.py`

Mendefinisikan model `MiniVLA`.

Komponen:

```text
Vision Encoder
Language Encoder
Multimodal Fusion
Target Cell Head
Gripper Head
```

---

## `train_vla.py`

Melatih Mini-VLA dari demonstration data.

Jalankan:

```bash
python train_vla.py
```

Output:

```text
results/mini_vla.pt
results/training_history.npz
results/training_loss.png
```

`training_loss.png` disimpan sekaligus **ditampilkan** saat script selesai training.

Terminal menampilkan:

```text
Model saved to: ...
Training history saved to: ...
Training plot saved to: ...
```

---

## `evaluate_vla.py`

Mengevaluasi Mini-VLA pada testing dataset.

Metric:

```text
Target-cell accuracy
Gripper accuracy
```

Output:

```text
results/evaluation_metrics.txt
results/evaluation_result.png
```

`evaluation_result.png` membandingkan:

```text
Target Action
vs.
Predicted Action
```

pada beberapa test sample.

Gambar disimpan sekaligus **ditampilkan** ketika script dijalankan.

---

## `colab_vla_demo.ipynb`

Versi Google Colab dari workflow Mini-VLA.

Notebook menjalankan:

```text
Generate Dataset
      ↓
Inspect Mini-VLA
      ↓
Train Policy
      ↓
Evaluate Policy
      ↓
Display Training Loss
      ↓
Display Evaluation Result
```

Gunakan GPU runtime agar training lebih cepat.

---

# Instalasi Lokal

Aktifkan environment Embodied AI:

```bash
source embodied-ai-env/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

---

# Menjalankan Mini-VLA

Jalankan secara berurutan:

```bash
python generate_dataset.py
python train_vla.py
python evaluate_vla.py
```

Urutan ini penting karena:

```text
generate_dataset.py
        ↓
results/train_vla.npz
results/test_vla.npz
        ↓
train_vla.py
        ↓
results/mini_vla.pt
        ↓
evaluate_vla.py
```

Setelah seluruh workflow selesai:

```text
results/
├── train_vla.npz
├── test_vla.npz
├── mini_vla.pt
├── training_history.npz
├── training_loss.png
├── evaluation_metrics.txt
└── evaluation_result.png
```

---

# Menjalankan di Google Colab

Buka:

```text
colab_vla_demo.ipynb
```

Kemudian aktifkan:

```text
Runtime
→ Change runtime type
→ GPU
```

Notebook menggunakan workflow yang sama dengan script lokal dan menyimpan hasil ke folder `results/`.

---

# Dua Visualisasi yang Menarik untuk Buku

Dari repository ini, dua visualisasi yang paling representatif adalah:

## 1. Mini-VLA: Target vs Predicted Action

File:

```text
results/evaluation_result.png
```

Visualisasi menunjukkan beberapa scene sekaligus dengan:

```text
Language Instruction
+
Visual Observation
+
Target Action
+
Predicted Action
```

Marker target menunjukkan workspace cell yang seharusnya dipilih, sedangkan marker prediction menunjukkan action yang diprediksi Mini-VLA.

Visualisasi ini paling langsung menunjukkan konsep:

```text
Vision + Language
        ↓
Action Prediction
```

Caption yang dapat digunakan:

> **Contoh prediksi Mini-VLA.** Model menerima image dan language instruction lalu memprediksi target workspace cell serta gripper command.

---

## 2. OpenVLA: Predicted End-Effector Translation

File Bonus:

```text
Bonus/results/translation_vector.png
```

Visualisasi menunjukkan komponen translasi:

```text
Δx
Δy
Δz
```

sebagai vector 3D dari posisi end-effector saat ini menuju predicted delta.

Visualisasi ini menarik karena menunjukkan bagaimana output VLA dapat diterjemahkan menjadi **spatial robot action**, bukan hanya label atau text response.

Caption yang dapat digunakan:

> **Visualisasi translasi end-effector dari action OpenVLA.** Tiga komponen translasi action digambarkan sebagai displacement vector 3D.

Untuk detail eksperimen OpenVLA, lihat:

```text
Bonus/README.md
```

---

# Keterbatasan Mini-VLA

Hands-on ini sengaja dibuat sederhana.

Mini-VLA belum memiliki:

```text
Pretrained Vision Encoder
Large Language Model
Continuous Robot Control
Action Chunking
Temporal Observation
Real Robot Demonstrations
Generalization to Natural Images
```

Dataset juga sangat terstruktur sehingga tidak mewakili keragaman observation pada robot nyata.

Tujuannya adalah memperlihatkan secara transparan bagaimana:

```text
Vision
+
Language
+
Demonstration Data
        ↓
Learned Robot Policy
        ↓
Action
```

---

# Inti Eksperimen

Hands-on utama menunjukkan bahwa policy dapat belajar mapping:

```text
(image, instruction)
        ↓
      action
```

Bonus kemudian memperlihatkan bentuk serupa pada pretrained VLA yang jauh lebih besar:

```text
RGB Image
+
Natural-Language Instruction
        ↓
     OpenVLA
        ↓
7-DoF Robot Action
```

Perubahan dari multimodal understanding menuju action generation merupakan ide utama di balik Vision-Language-Action models.
