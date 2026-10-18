# Bonus Hands-on: Image-Text Similarity dengan CLIP

Bonus ini memperkenalkan **CLIP (Contrastive Language-Image Pretraining)** sebagai contoh sederhana multimodal learning.

CLIP dapat menempatkan image dan text ke embedding space yang sama sehingga kita dapat mengukur seberapa dekat sebuah image dengan beberapa candidate description.

Contoh:

```text
Image:
seorang memakai kaos biru sambil memegang botol
```

dibandingkan dengan:

```text
"a person with blue t-shirt holding a bottle"
"a person standing near a laptop"
"a bottle on a table"
"a red car on the street"
```

CLIP kemudian menghasilkan similarity score untuk setiap candidate text.

---

## Struktur Project

```text
Bonus/
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

### Image dan Text Embedding

CLIP memiliki dua encoder utama:

```text
Image
  ↓
Image Encoder
  ↓
Image Embedding
```

dan:

```text
Text
 ↓
Text Encoder
 ↓
Text Embedding
```

Kedua embedding tersebut berada pada representation space yang sama.

Karena itu, image dan text dapat dibandingkan secara langsung.

---

## Cosine Similarity

Hands-on ini menggunakan **cosine similarity** untuk membandingkan image embedding dengan text embedding.

Secara sederhana:

```text
similarity(image, text)
```

Semakin tinggi nilainya, semakin dekat kedua representation secara semantik.

Contoh:

```text
0.31 → candidate A
0.24 → candidate B
0.08 → candidate C
```

Candidate A memiliki semantic similarity paling tinggi di antara candidate yang dibandingkan.

Similarity tersebut bukan ukuran kebenaran absolut.

Nilainya paling berguna untuk **membandingkan candidate text terhadap image yang sama**.

---

## Relative Probability

CLIP juga menghasilkan:

```text
logits_per_image
```

Script mengubah logits menjadi relative probability menggunakan:

```text
softmax()
```

Contohnya:

```text
72% | a person with blue t-shirt holding a bottle
18% | a bottle on a table
 8% | a person standing near a laptop
 2% | a red car on the street
```

Persentase ini menunjukkan distribusi relatif hanya di antara candidate text yang diberikan.

Nilainya bukan calibrated confidence probability absolut.

Jika candidate text berubah, relative probability juga dapat berubah.

---

## Zero-Shot Matching

Tidak ada training tambahan pada hands-on ini.

Pipeline langsung menggunakan pretrained CLIP:

```text
Pretrained CLIP
      ↓
Image + Text Candidates
      ↓
Similarity
```

Ini merupakan contoh **zero-shot image-text matching**.

---

# File Utama

## `clip_similarity.py`

Script melakukan:

```text
1. Membuka image
2. Membaca candidate text dari --texts-file atau --texts
3. Load pretrained CLIP
4. Membuat image embedding
5. Membuat text embeddings
6. Menghitung cosine similarity
7. Menghitung relative probability
8. Mengurutkan candidate berdasarkan cosine similarity
9. Menampilkan ranking di terminal
10. Menyimpan ranking ke file text
11. Menampilkan input image di panel kiri
12. Menampilkan similarity ranking di panel kanan
13. Menyimpan dan menampilkan visualisasi
```

---

## `sample_prompts.txt`

File ini menyediakan contoh candidate text.

Setiap baris berisi satu candidate:

```text
a person with blue t-shirt holding a bottle
a person standing near a laptop
a bottle on a table
...
```

Kamu dapat mengganti atau menambahkan candidate sendiri.

---

## `person.jpg`

Image contoh yang dapat digunakan untuk menjalankan demo.

---

## `colab_clip_similarity.ipynb`

Versi Google Colab dari workflow yang sama.

Notebook menjalankan pipeline CLIP tanpa perlu menyiapkan environment Python lokal.

Workflow-nya:

```text
Install dependency
      ↓
Upload image
      ↓
Define candidate text
      ↓
Load pretrained CLIP
      ↓
Image + Text Encoding
      ↓
Cosine Similarity
      ↓
Relative Probability
      ↓
Ranking
      ↓
Visualisasi
```

Notebook menampilkan input image dan similarity ranking, lalu menyimpan output ke folder `results/`.

---

# Instalasi Lokal

Masuk ke folder Bonus lalu install dependency:

```bash
pip install -r requirements.txt
```

---

# Menjalankan

Ada dua cara memberikan candidate text.

## Opsi 1 — Menggunakan `sample_prompts.txt`

Contoh menggunakan file yang sudah tersedia:

```bash
python clip_similarity.py \
  --image person.jpg \
  --texts-file sample_prompts.txt
```

Setiap baris pada `sample_prompts.txt` akan dianggap sebagai satu candidate text.

## Opsi 2 — Menulis Candidate Text Langsung

Candidate juga dapat diberikan langsung melalui terminal:

```bash
python clip_similarity.py \
  --image person.jpg \
  --texts \
  "a person wearing a blue shirt and holding a bottle" \
  "a person sitting in front of a laptop" \
  "a bottle being held by a person" \
  "a red car on the street"
```

Jika `--texts-file` dan `--texts` tidak diberikan, script menggunakan candidate default.

Script akan memilih:

```text
CUDA
```

jika tersedia.

Jika tidak, script menggunakan:

```text
CPU
```

Untuk satu image, CPU masih dapat digunakan tetapi inference biasanya lebih lambat daripada GPU.

---

# Menjalankan di Google Colab

Buka:

```text
colab_clip_similarity.ipynb
```

Kemudian:

```text
1. Aktifkan GPU runtime
2. Jalankan cell instalasi
3. Upload image
4. Tentukan candidate text
5. Load pretrained CLIP
6. Jalankan image dan text encoding
7. Hitung cosine similarity
8. Hitung relative probability
9. Periksa ranking
10. Lihat visualisasi
11. Simpan hasil ke results/
```

Untuk mengaktifkan GPU:

```text
Runtime
→ Change runtime type
→ GPU
```

Google Colab merupakan **alternatif** terhadap script lokal. Kamu tidak perlu menjalankan keduanya untuk memahami workflow yang sama.

Versi lokal:

```text
clip_similarity.py
```

Versi Google Colab:

```text
colab_clip_similarity.ipynb
```

Keduanya menunjukkan:

```text
Image
+
Candidate Text
      ↓
CLIP
      ↓
Cosine Similarity
+
Relative Probability
      ↓
Similarity Ranking
```

---

# Output Terminal

Terminal menampilkan hasil yang telah diurutkan berdasarkan cosine similarity.

Formatnya:

```text
Cosine Similarity
|
Relative Probability
|
Text Candidate
```

Contoh:

```text
 0.3120 | 65.20% | a person with blue t-shirt holding a bottle
 0.2410 | 21.10% | a bottle on a table
 ...
```

---

# Hasil 1 — `clip_similarity_scores.txt`

Hasil text disimpan ke:

```text
results/clip_similarity_scores.txt
```

File ini memudahkan kita menyimpan ranking candidate tanpa hanya bergantung pada output terminal.

Setiap baris berisi:

```text
Cosine Similarity
Relative Probability
Candidate Text
```

Urutan dimulai dari candidate dengan similarity tertinggi.

---

# Hasil 2 — `clip_similarity_result.png`

Visualisasi disimpan ke:

```text
results/clip_similarity_result.png
```

Gambar tersebut juga **langsung ditampilkan** ketika script dijalankan.

Visualisasi terdiri dari dua panel:

```text
┌──────────────────────┬───────────────────────────────────────┐
│                      │ CLIP Image-Text Similarity            │
│                      │                                       │
│     Input Image      │ candidate A  ███████████████  0.31   │
│                      │ candidate B  ███████████      0.24   │
│                      │ candidate C  █████             0.10   │
│                      │ candidate D  ███               0.08   │
└──────────────────────┴───────────────────────────────────────┘
```

Panel kiri menunjukkan **image yang sedang dibandingkan**.

Panel kanan menunjukkan **ranking candidate text berdasarkan cosine similarity**.

Sumbu horizontal pada bar chart menunjukkan:

```text
Cosine Similarity
```

Bar yang lebih panjang berarti candidate text memiliki semantic similarity yang lebih tinggi terhadap image.

Score numerik juga ditampilkan pada masing-masing bar.

---

## Cara Membaca Gambar

Misalnya:

```text
Image: person.jpg
```

menghasilkan:

```text
Text Candidate                    Similarity
────────────────────────────────────────────
a person standing...          ███████████  0.31
a person sitting...           █████████     0.24
a car on the road...          ███           0.11
a bowl of food...             ██            0.08
```

Maka candidate `"a person standing..."` merupakan description yang paling dekat dengan `person.jpg` dalam CLIP embedding space.

Namun kita tidak boleh langsung mengartikan:

```text
0.31 = 31% benar
```

karena **cosine similarity bukan probability**.

Visualisasi digunakan untuk **ranking dan comparison** antar-candidate text terhadap image yang sama, bukan sebagai confidence absolut.

---

## Mengapa Gambar Ditampilkan dan Disimpan?

Script melakukan dua hal:

```text
plt.savefig(...)
plt.show()
```

Dengan demikian:

```text
savefig
→ menyimpan hasil untuk dokumentasi

show
→ memungkinkan pengguna langsung memeriksa hasil saat script dijalankan
```

Setelah memeriksa gambar, tutup window Matplotlib agar script selesai.

---

# Hubungan dengan VLM

CLIP dan VLM sama-sama menghubungkan vision dan language, tetapi cara penggunaannya berbeda.

CLIP pada hands-on ini:

```text
Image
+
Candidate Text
      ↓
Similarity Score
```

Sedangkan VLM utama:

```text
Image
+
Instruction
      ↓
Generated Semantic Response
```

CLIP cocok untuk semantic matching dan retrieval.

VLM generatif dapat menghasilkan language reasoning yang lebih fleksibel.

---

## Keterbatasan Demo

Demo ini belum melakukan:

```text
Object Detection
Bounding Box Grounding
Segmentation
Robot Control
Action Generation
Fine-Tuning
```

CLIP hanya membandingkan semantic compatibility antara satu image dan beberapa candidate text.

Karena itu, similarity tinggi belum otomatis memberi tahu robot lokasi precise object atau motion yang harus dilakukan.

---

## Inti Konsep

Hands-on ini menunjukkan fondasi sederhana multimodal representation:

```text
Vision
+
Language
      ↓
Shared Embedding Space
      ↓
Semantic Similarity
```

Kemampuan menyelaraskan image dan text seperti ini merupakan salah satu fondasi penting dalam perkembangan multimodal AI modern.
