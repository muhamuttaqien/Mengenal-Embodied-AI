# Hands-on: Dari Rules menuju Learning-Based Systems

Mini-project ini membandingkan dua cara robot mengambil keputusan dari tiga sensor jarak: **kiri, depan, dan kanan**.

Robot menerima observation:

```text
[left_distance, front_distance, right_distance]
```

dan memilih salah satu action:

```text
LEFT
FORWARD
RIGHT
```

Tujuan hands-on ini adalah memahami bagaimana keputusan yang awalnya ditulis langsung melalui aturan dapat dipelajari kembali oleh sebuah neural network dari data.

Secara sederhana:

```text
Rule-Based Controller
        ↓
Generate Labeled Data
        ↓
Train Neural Network
        ↓
Learning-Based Policy
        ↓
Compare Decisions
```

---

## Konsep Penting

### Rule-Based Approach

Pada pendekatan rule-based, keputusan robot ditentukan melalui aturan yang ditulis langsung oleh programmer.

Contohnya:

```python
if front_distance >= SAFE_DISTANCE:
    return FORWARD

if left_distance > right_distance:
    return LEFT

return RIGHT
```

Logikanya adalah:

```text
Depan aman?
   ↓
  Ya → FORWARD
   ↓ Tidak
Bandingkan kiri dan kanan
   ↓
Kiri lebih luas → LEFT
Selain itu       → RIGHT
```

Pendekatan ini mudah dipahami karena hubungan antara observation dan action ditulis secara eksplisit.

Namun semakin kompleks lingkungan dan jumlah kondisi yang harus ditangani, semakin sulit aturan tersebut dikelola secara manual.

### Learning-Based Approach

Pada learning-based system, kita tidak menuliskan setiap keputusan melalui banyak aturan `if-else`.

Sebaliknya, model belajar dari pasangan:

```text
Observation → Action
```

Pada hands-on ini, target action masih dibuat menggunakan rule-based controller. Tujuannya adalah membuat eksperimen sederhana untuk melihat apakah neural network dapat mempelajari pola keputusan yang sebelumnya ditentukan oleh programmer.

### Neural Network sebagai Policy

Neural network menerima tiga nilai sensor:

```text
left_distance
front_distance
right_distance
```

kemudian menghasilkan tiga output yang mewakili kemungkinan action:

```text
[left, front, right]
        ↓
   Neural Network
        ↓
LEFT  FORWARD  RIGHT
```

Action dengan nilai output terbesar dipilih sebagai keputusan model.

### Training dan Testing

Dataset dibagi menjadi dua bagian:

```text
Training Data
Testing Data
```

**Training data** digunakan untuk memperbarui parameter neural network.

**Testing data** digunakan untuk mengevaluasi model pada observation yang tidak digunakan selama training.

---

## Struktur Project

```text
Rules vs Learning-Based Approach/
├── generate_data.py
├── rules.py
├── model.py
├── train.py
├── evaluate.py
├── requirements.txt
├── README.md
└── results/
    ├── train_data.npz
    ├── test_data.npz
    ├── policy_model.pt
    ├── training_loss.png
    └── comparison_result.png
```

Folder `results/` dibuat otomatis ketika script dijalankan.

---

## Penjelasan Setiap File

### `rules.py`

Berisi rule-based controller.

Controller menggunakan tiga jarak sensor:

```text
left_distance
front_distance
right_distance
```

untuk memilih salah satu action:

```text
LEFT
FORWARD
RIGHT
```

File ini merepresentasikan pendekatan ketika keputusan robot ditulis secara eksplisit oleh programmer.

### `model.py`

Mendefinisikan neural network `RobotPolicy`.

Model memiliki:

```text
3 input
 ↓
32 hidden units
 ↓
32 hidden units
 ↓
3 output
```

Tiga input berasal dari sensor jarak, sedangkan tiga output merepresentasikan action `LEFT`, `FORWARD`, dan `RIGHT`.

File ini hanya mendefinisikan arsitektur model. Proses training dilakukan pada `train.py`.

### `generate_data.py`

Script ini membuat ribuan observation sensor secara acak.

Setiap observation memiliki bentuk:

```text
[left_distance, front_distance, right_distance]
```

Kemudian `rule_based_action()` digunakan untuk memberikan target action.

Alurnya:

```text
Random Sensor Observation
          ↓
Rule-Based Controller
          ↓
Target Action
          ↓
Dataset
```

Dataset kemudian diacak dan dibagi menjadi:

```text
80% Training
20% Testing
```

Output disimpan ke:

```text
results/train_data.npz
results/test_data.npz
```

### `train.py`

Script ini membaca:

```text
results/train_data.npz
```

kemudian melatih `RobotPolicy` menggunakan:

```text
Cross-Entropy Loss
Adam Optimizer
Backpropagation
```

Pada setiap epoch:

```text
Observation
    ↓
Neural Network
    ↓
Predicted Action
    ↓
Compare with Target
    ↓
Loss
    ↓
Backpropagation
    ↓
Update Model
```

Output training disimpan ke:

```text
results/policy_model.pt
results/training_loss.png
```

### `evaluate.py`

Script ini membaca:

```text
results/test_data.npz
results/policy_model.pt
```

kemudian menjalankan inference terhadap test dataset.

Program menghitung accuracy, membandingkan beberapa contoh keputusan rule-based dan learning-based, lalu membuat confusion matrix.

Output disimpan ke:

```text
results/comparison_result.png
```

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

Hands-on ini cukup ringan dan dapat dijalankan menggunakan **CPU**.

---

## Cara Menjalankan

Jalankan script secara berurutan:

```bash
python generate_data.py
python train.py
python evaluate.py
```

Urutannya penting karena:

```text
generate_data.py
      ↓
train_data.npz + test_data.npz
      ↓
train.py
      ↓
policy_model.pt
      ↓
evaluate.py
      ↓
comparison_result.png
```

---

## Hasil 1 — Dataset

Setelah menjalankan:

```bash
python generate_data.py
```

akan terbentuk:

```text
results/train_data.npz
results/test_data.npz
```

Setiap observation berisi tiga nilai jarak sensor dan setiap target berisi satu label action.

Contohnya:

```text
Observation: [1.20, 1.50, 0.80]
Action     : FORWARD
```

Dataset ini menjadi penghubung antara rule-based controller dan learning-based policy.

---

## Hasil 2 — `training_loss.png`

Visualisasi training disimpan ke:

```text
results/training_loss.png
```

Gambar ini menunjukkan perubahan **loss** sepanjang training.

Sumbu horizontal menunjukkan:

```text
Epoch
```

sedangkan sumbu vertikal menunjukkan:

```text
Loss
```

Secara umum, jika model mulai belajar pola dari training data, loss akan cenderung turun.

```text
Loss tinggi
   ↓
Prediction masih jauh dari target

Loss menurun
   ↓
Prediction semakin sesuai dengan target
```

Namun loss yang menurun tidak otomatis berarti semua jenis action sudah dipelajari dengan sama baiknya. Karena itu, hasil evaluation tetap perlu diperiksa.

---

## Hasil 3 — `policy_model.pt`

Model hasil training disimpan ke:

```text
results/policy_model.pt
```

File ini berisi parameter neural network yang sudah diperbarui selama training.

File tersebut kemudian dimuat oleh `evaluate.py` untuk melakukan inference tanpa perlu melatih model dari awal lagi.

---

## Hasil 4 — `comparison_result.png`

Hasil evaluation disimpan ke:

```text
results/comparison_result.png
```

Gambar ini merupakan **confusion matrix** yang membandingkan:

```text
Rule-Based Target
vs.
Learning-Based Prediction
```

Baris menunjukkan action yang diberikan oleh rule-based controller.

Kolom menunjukkan action yang diprediksi oleh neural network.

Dengan tiga action, matrix memiliki bentuk:

```text
              Predicted
           LEFT FORWARD RIGHT

True LEFT
True FORWARD
True RIGHT
```

Nilai pada diagonal menunjukkan prediction yang benar:

```text
LEFT    → LEFT
FORWARD → FORWARD
RIGHT   → RIGHT
```

Sedangkan nilai di luar diagonal menunjukkan kesalahan prediction.

Contohnya:

```text
True LEFT → Predicted FORWARD
```

berarti rule-based controller memilih `LEFT`, tetapi learning-based policy memilih `FORWARD`.

Confusion matrix penting karena accuracy saja dapat menyembunyikan kelemahan model pada class tertentu.

---

## Catatan tentang Distribusi Action

Dataset pada demo ini dibuat dengan sampling jarak sensor secara uniform, tetapi rule-based controller tidak menghasilkan action dengan jumlah yang sama.

Karena aturan pertama adalah:

```python
if front_distance >= SAFE_DISTANCE:
    return FORWARD
```

banyak observation akan langsung diberi label `FORWARD`.

Akibatnya, dataset dapat memiliki lebih banyak sample `FORWARD` daripada `LEFT` dan `RIGHT`.

Ini merupakan contoh sederhana dari **class imbalance**.

Karena itu, jangan hanya melihat accuracy.

Perhatikan juga confusion matrix untuk melihat apakah model benar-benar mampu membedakan ketiga action.

---

## Rule-Based vs. Learning-Based

Hands-on ini tidak dimaksudkan untuk menunjukkan bahwa learning-based approach selalu lebih baik daripada rules.

Justru kita dapat melihat perbedaan karakter keduanya.

```text
Rule-Based
→ keputusan ditulis eksplisit
→ mudah ditelusuri
→ tidak memerlukan training

Learning-Based
→ keputusan dipelajari dari data
→ membutuhkan training
→ kualitasnya bergantung pada data dan proses belajar
```

Dalam robot nyata, kedua pendekatan juga dapat digunakan bersama tergantung kebutuhan sistem.

---

## Inti Konsep

Hands-on ini menunjukkan perubahan sederhana dari:

```text
Programmer writes decision rules
            ↓
Generate examples from those rules
            ↓
Model learns from examples
            ↓
Model predicts actions
```

Dengan kata lain, sebuah policy yang sebelumnya didefinisikan secara eksplisit dapat direpresentasikan sebagai **fungsi yang dipelajari dari data**.
