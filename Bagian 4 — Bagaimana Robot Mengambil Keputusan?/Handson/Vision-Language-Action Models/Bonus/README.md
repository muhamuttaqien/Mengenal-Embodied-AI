# Bonus Hands-on: OpenVLA Action Visualization

Bonus ini menggunakan **OpenVLA-7B** untuk melihat bagaimana pretrained Vision-Language-Action model menerima:

```text
RGB Image
+
Natural-Language Instruction
```

dan menghasilkan:

```text
7-DoF Robot Action
```

Eksperimen ini **tidak menjalankan simulator atau robot fisik**. Action hanya diprediksi, disimpan, dan divisualisasikan.

---

# Workflow

```text
RGB Image
+
Language Instruction
        ↓
     OpenVLA-7B
        ↓
 7-DoF Action Vector
        ↓
Save + Visualize
```

---

# 7-DoF Action

Action dibaca sebagai:

```text
[
  Δx,
  Δy,
  Δz,
  Δroll,
  Δpitch,
  Δyaw,
  gripper
]
```

Enam komponen pertama merepresentasikan perubahan pose end-effector.

Komponen terakhir merepresentasikan gripper command.

**Penting:** coordinate frame, scaling, dan gripper semantics mengikuti convention dataset/robot yang digunakan oleh model.

Action ini tidak boleh dianggap sebagai universal robot command.

---

# Action Un-normalization

OpenVLA memprediksi normalized action.

Default pada hands-on ini menggunakan:

```text
unnorm_key = bridge_orig
```

yang mengikuti statistik action BridgeData V2 pada contoh OpenVLA.

---

# Struktur Project

```text
Bonus/
├── openvla_inference.py
├── visualize_action.py
├── colab_openvla_action.ipynb
├── requirements.txt
├── README.md
└── results/
    ├── openvla_action.npy
    ├── openvla_action.json
    ├── action_summary.txt
    ├── action_bar_chart.png
    └── translation_vector.png
```

Semua hasil disimpan di folder:

```text
Bonus/results/
```

---

# `openvla_inference.py`

Script ini:

```text
1. Membaca image
2. Membaca language instruction
3. Load OpenVLA processor
4. Load OpenVLA-7B
5. Membuat prompt
6. Menjalankan predict_action()
7. Menyimpan raw 7-DoF action
8. Membuat visualisasi
9. Menyimpan seluruh hasil ke results/
```

Contoh:

```bash
python openvla_inference.py \
  --image scene.jpg \
  --instruction "pick up the red object"
```

Output:

```text
results/openvla_action.npy
results/openvla_action.json
results/action_summary.txt
results/action_bar_chart.png
results/translation_vector.png
```

Terminal memberi keterangan seperti:

```text
NumPy action saved to: ...
JSON action saved to: ...
Action bar chart saved to: ...
Translation vector saved to: ...
Action summary saved to: ...
```

Kedua visualisasi juga **ditampilkan** ketika script dijalankan.

---

# `visualize_action.py`

Script ini memungkinkan kita memvisualisasikan action tanpa menjalankan OpenVLA.

Ini berguna untuk:

```text
testing plotting pipeline
memahami 7-DoF action
membuat visualisasi tanpa mendownload model 7B
```

Jalankan demo:

```bash
python visualize_action.py --demo
```

Output:

```text
results/action_bar_chart.png
results/translation_vector.png
results/action_summary.txt
```

---

# Hasil 1: `action_bar_chart.png`

File:

```text
results/action_bar_chart.png
```

Bar chart menampilkan seluruh action:

```text
Δx
Δy
Δz
Δroll
Δpitch
Δyaw
gripper
```

Visualisasi ini membantu melihat dimensi action mana yang mempunyai magnitude paling besar.

---

# Hasil 2: `translation_vector.png`

File:

```text
results/translation_vector.png
```

Visualisasi 3D menggunakan tiga komponen:

```text
Δx
Δy
Δz
```

untuk menunjukkan arah predicted end-effector translation.

```text
Current EE
    ↓
    ●────────→ Predicted Delta
```

Visualisasi ini merupakan salah satu gambar yang paling menarik untuk ditampilkan pada buku karena menghubungkan numeric action dengan spatial robot motion.

---

# `action_summary.txt`

File:

```text
results/action_summary.txt
```

Berisi nilai action dalam format yang mudah dibaca:

```text
Δx
Δy
Δz
Δroll
Δpitch
Δyaw
gripper
```

---

# Google Colab

Buka:

```text
colab_openvla_action.ipynb
```

Aktifkan GPU:

```text
Runtime
→ Change runtime type
→ GPU
```

Notebook menjalankan:

```text
Install Dependencies
        ↓
Upload Image
        ↓
Write Instruction
        ↓
Load OpenVLA
        ↓
Run Inference
        ↓
Print Action
        ↓
Save Results
        ↓
Display Visualizations
```

Notebook telah disesuaikan agar semua raw action dan gambar disimpan ke:

```text
results/
```

---

# Hardware

OpenVLA-7B adalah model besar.

GPU dengan VRAM besar sangat disarankan. Runtime 16 GB dapat menjadi ketat karena checkpoint dan inference membutuhkan memory tambahan.

Jika hanya ingin mencoba visualisasi tanpa load model, gunakan:

```bash
python visualize_action.py --demo
```

---

# Catatan Penting

Eksperimen ini tidak mengeksekusi action pada robot.

Pipeline hanya:

```text
predict
save
visualize
```

Sebelum action digunakan pada robot nyata, kita harus memastikan:

```text
robot embodiment
coordinate frame
action scaling
gripper convention
safety constraints
control interface
```

sesuai dengan robot yang digunakan.

---

# Inti Konsep

Bonus ini menunjukkan bentuk konkret:

```text
Vision
+
Language
        ↓
Pretrained VLA
        ↓
Robot Action
```

Berbeda dari Vision-Language Model yang menghasilkan text response, OpenVLA secara langsung menghasilkan action representation yang dapat digunakan sebagai basis robot control.
