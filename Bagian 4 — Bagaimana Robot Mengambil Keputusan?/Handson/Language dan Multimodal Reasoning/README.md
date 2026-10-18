# Hands-on Language dan Multimodal Reasoning

Project ini memperkenalkan cara sederhana menggunakan **Vision-Language Model (VLM)** untuk menggabungkan informasi visual dan instruksi bahasa pada konteks robot.

Contoh:

```text
Image:
meja dengan botol, laptop, mug, notebook, dan ponsel

Instruction:
"Ambil botol di sebelah laptop."
```

Model menerima:

```text
Image
+
Language Instruction
        ↓
Vision-Language Model
        ↓
Target Object
+
Visual Evidence
+
Suggested Robot Action
```

Hands-on utama menggunakan pretrained model:

```text
Qwen/Qwen2.5-VL-3B-Instruct
```

Model tidak dilatih dari awal. Kita menggunakan kemampuan vision-language yang sudah dipelajari sebelumnya untuk melakukan inference.

Project dapat dijalankan melalui:

```text
Google Colab
atau
Komputer lokal dengan environment Python yang sesuai
```

Untuk inference lokal, GPU yang kompatibel sangat disarankan karena model vision-language cukup besar.

---

## Struktur Project

```text
Language dan Multimodal Reasoning/
├── run_vlm.py
├── multimodal_utils.py
├── colab_multimodal_reasoning.ipynb
├── requirements.txt
├── README.md
├── scene.jpg                 # Image contoh yang ditambahkan pengguna
├── results/
│   └── vlm_response.txt
└── Bonus/
    ├── clip_similarity.py
    ├── colab_clip_similarity.ipynb
    ├── sample_prompts.txt
    ├── person.jpg
    ├── requirements.txt
    ├── README.md
    └── results/
        ├── clip_similarity_result.png
        └── clip_similarity_scores.txt
```

Folder `results/` akan dibuat otomatis ketika script dijalankan.

---

## Konsep Penting

### Vision-Language Model

Vision-Language Model menerima informasi visual dan bahasa dalam satu pipeline.

Secara sederhana:

```text
Pixels
  +
Words
  ↓
Multimodal Representation
  ↓
Semantic Interpretation
```

Model mencoba memahami hubungan antara apa yang terlihat pada image dan apa yang diminta melalui bahasa.

---

## Multimodal Input

Input utama terdiri dari dua modality:

```text
Vision
→ image

Language
→ instruction
```

Contohnya:

```text
Image:
terlihat botol dan laptop

Instruction:
"Ambil botol di sebelah laptop."
```

Model perlu memahami bahwa kata `botol` merujuk pada object tertentu yang terlihat pada image.

---

## Visual Grounding

**Grounding** adalah proses menghubungkan bahasa dengan sesuatu yang terlihat pada environment.

Contoh:

```text
"botol di sebelah laptop"
           ↓
identify visual object
           ↓
target bottle
```

Grounding penting pada Embodied AI karena instruction manusia pada akhirnya harus dikaitkan dengan object, lokasi, atau kondisi yang benar-benar ada di dunia.

---

## Semantic Reasoning

Model tidak hanya mengklasifikasikan image.

Prompt pada hands-on ini meminta model menjawab tiga hal:

```text
1. Object mana yang dimaksud?
2. Evidence visual apa yang mendukung?
3. Action sederhana apa yang sebaiknya dilakukan robot?
```

Contohnya:

```text
Target object:
Bottle

Visual evidence:
Bottle terlihat di sebelah laptop.

Suggested robot action:
Move toward the bottle and prepare a grasp.
```

Output tersebut masih berada pada **semantic level**.

Model belum secara langsung menghasilkan trajectory joint atau motor command.

---

# File Utama

## `multimodal_utils.py`

File ini berisi helper function untuk:

```text
load image
+
build robot-oriented prompt
```

Fungsi `load_image()` membuka image dan mengubahnya menjadi RGB.

Fungsi `build_robot_prompt()` mengubah natural-language instruction menjadi prompt yang meminta model melakukan visual grounding dan memberikan suggested robot action.

---

## `run_vlm.py`

Script ini menjalankan seluruh pipeline VLM dari command-line.

Alurnya:

```text
Input Image
    ↓
Input Instruction
    ↓
Build Prompt
    ↓
Load Processor
    ↓
Load Qwen2.5-VL
    ↓
Multimodal Inference
    ↓
Decode Response
    ↓
Save Response
```

Response model ditampilkan pada terminal dan juga disimpan ke:

```text
results/vlm_response.txt
```

---

## `colab_multimodal_reasoning.ipynb`

Notebook ini menjalankan workflow yang sama melalui Google Colab.

Notebook mencakup:

```text
Install dependency
Upload image
Load VLM
Create multimodal prompt
Run inference
Decode result
Display result
Save result
```

Output text disimpan ke:

```text
results/vlm_response.txt
```

---

# Instalasi Lokal

Buat environment:

```bash
python -m venv embodied-ai-env
```

Aktifkan pada Linux/macOS:

```bash
source embodied-ai-env/bin/activate
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

---

# Menjalankan VLM

Siapkan sebuah image, misalnya:

```text
scene.jpg
```

Simpan `scene.jpg` pada folder utama project, sejajar dengan `run_vlm.py`.

Kemudian jalankan:

```bash
python run_vlm.py \
  --image scene.jpg \
  --instruction "Ambil botol di sebelah laptop."
```

Untuk contoh yang lebih dekat dengan Embodied AI, kamu juga dapat menggunakan instruction:

```bash
python run_vlm.py \
  --image scene.jpg \
  --instruction "A robot is asked to pick up the bottle. Describe which object should be manipulated and its position relative to the laptop."
```

Pada pertama kali dijalankan, pretrained model perlu diunduh sehingga proses load dapat memerlukan waktu.

Terminal akan menampilkan response model, misalnya:

```text
Model response:

1. The visible bottle is the target object.
2. It is located next to the laptop.
3. Move toward the bottle and prepare a grasp.
```

Hasil yang sama juga disimpan ke:

```text
results/vlm_response.txt
```

---

# Hasil — `vlm_response.txt`

File:

```text
results/vlm_response.txt
```

berisi output semantic reasoning dari VLM.

Secara umum, kita dapat membaca output berdasarkan tiga bagian.

### Target Object

Bagian ini menunjukkan object yang dianggap paling sesuai dengan instruction.

Contoh:

```text
the bottle next to the laptop
```

Ini adalah hasil visual grounding.

---

### Visual Evidence

Bagian ini menjelaskan informasi dari image yang digunakan model untuk mendukung jawabannya.

Contohnya:

```text
the bottle is visible beside the laptop
```

Evidence membantu kita memahami hubungan antara instruction dan visual scene.

Namun perlu diingat bahwa response VLM bersifat generatif sehingga model tetap dapat menghasilkan kesalahan.

---

### Suggested Robot Action

Bagian terakhir memberikan action sederhana pada level bahasa.

Contohnya:

```text
Move toward the bottle and prepare a grasp.
```

Output ini belum merupakan low-level robot action.

Untuk robot nyata, hasil tersebut masih perlu diterjemahkan menjadi:

```text
Semantic Decision
      ↓
Task Planner / Policy
      ↓
Motion Planning
      ↓
Robot Control
```

---

# Menjalankan di Google Colab

Buka:

```text
colab_multimodal_reasoning.ipynb
```

Kemudian:

```text
1. Aktifkan GPU runtime
2. Jalankan cell instalasi
3. Upload image
4. Masukkan instruction
5. Load model
6. Jalankan inference
7. Periksa response
```

Gunakan:

```text
Runtime
→ Change runtime type
→ GPU
```

Notebook akan menampilkan image dan output model secara langsung, lalu menyimpan response ke:

```text
results/vlm_response.txt
```

Versi Google Colab menjalankan eksperimen yang sama dengan `run_vlm.py`. Perbedaannya hanya pada environment eksekusi dan cara menyediakan image.

---

# Bonus — Image-Text Similarity dengan CLIP

Folder:

```text
Bonus/
```

berisi hands-on tambahan menggunakan **CLIP**.

Berbeda dengan VLM generatif, CLIP tidak menghasilkan reasoning text panjang.

CLIP membandingkan:

```text
Image
vs.
Multiple Text Candidates
```

dan menghitung semantic similarity masing-masing pasangan.

Contoh:

```text
Image
  ↓
CLIP Image Encoder
  ↓
Image Embedding

Text Candidates
  ↓
CLIP Text Encoder
  ↓
Text Embeddings

Image Embedding
        vs.
Text Embeddings
        ↓
Cosine Similarity
```

Penjelasan lengkap tersedia pada:

```text
Bonus/README.md
```

Untuk menjalankan Bonus secara lokal:

```bash
cd Bonus

python clip_similarity.py \
  --image person.jpg \
  --texts-file sample_prompts.txt
```

Script Bonus menghasilkan:

```text
results/
├── clip_similarity_scores.txt
└── clip_similarity_result.png
```

`clip_similarity_result.png` menampilkan **input image di sisi kiri** dan **ranking cosine similarity di sisi kanan**. Visualisasi disimpan sekaligus ditampilkan ketika script berjalan.

Selain `--texts-file`, candidate text juga dapat diberikan langsung dari terminal:

```bash
python clip_similarity.py \
  --image person.jpg \
  --texts \
  "a person wearing a blue shirt and holding a bottle" \
  "a person sitting in front of a laptop" \
  "a bottle being held by a person" \
  "a red car on the street"
```

Versi Google Colab untuk Bonus tersedia pada:

```text
Bonus/colab_clip_similarity.ipynb
```

---

# Hubungan dengan Embodied AI

Hands-on ini berhenti pada language-level reasoning:

```text
Image + Language
      ↓
VLM
      ↓
Semantic Interpretation
```

Dalam sistem Embodied AI yang lengkap, output tersebut dapat menjadi input untuk komponen berikutnya:

```text
Semantic Interpretation
        ↓
Task Planning
        ↓
Motion Planning / Policy
        ↓
Low-Level Control
        ↓
Physical Action
```

Dengan demikian, VLM membantu robot memahami **apa yang dimaksud manusia dan object mana yang relevan**, sedangkan komponen robotik berikutnya menentukan **bagaimana action tersebut benar-benar dilakukan**.

---

## Inti Konsep

Hands-on ini menunjukkan hubungan:

```text
Vision
+
Language
    ↓
Multimodal Reasoning
    ↓
Grounded Semantic Decision
    ↓
Potential Robot Action
```

Kemampuan menggabungkan visual perception dan natural language merupakan salah satu fondasi penting menuju sistem seperti **Vision-Language-Action (VLA)**.
