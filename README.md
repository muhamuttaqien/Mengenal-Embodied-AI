# Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata

Repository ini merupakan materi pendamping untuk buku **Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**. Isinya mencakup gambar pendukung, kode hands-on, notebook, hasil eksperimen, serta panduan teknis yang melengkapi pembahasan di dalam buku.

> **Status:** repository dan naskah buku masih dalam tahap pengembangan.

## Tentang Buku

Buku ini memperkenalkan **Embodied AI** secara bertahap, mulai dari konsep dasar AI yang berinteraksi dengan dunia fisik, komponen robot, tantangan perception hingga manipulation, metode pengambilan keputusan, sampai penggunaan simulator untuk eksperimen robotika.

Pendekatan yang digunakan berusaha menghubungkan **teori, intuisi, dan praktik**, sehingga pembaca tidak hanya memahami konsep, tetapi juga dapat mencoba implementasinya melalui hands-on yang tersedia di repository ini.

## Isi Repository

Saat ini repository memuat lima bagian utama:

### Bagian 1 — Mengenal Embodied AI

Pengantar mengenai Embodied AI dan bagaimana kecerdasan buatan dapat berinteraksi dengan lingkungan melalui tubuh, sensor, dan action.

### Bagian 2 — Mengenal Robot dan Dunia Fisik

Pengenalan komponen robot dan elemen penting dalam interaksi dengan dunia fisik.

### Bagian 3 — Tantangan Utama dalam Embodied AI

Materi dan hands-on mengenai:

- Perception
- Localization
- Mapping
- Navigation
- Planning
- Manipulation
- Locomotion

Kode praktik tersedia di folder:

`Bagian 3 — Tantangan Utama dalam Embodied AI/Handson/`

### Bagian 4 — Bagaimana Robot Mengambil Keputusan?

Materi dan hands-on mengenai beberapa pendekatan pengambilan keputusan pada robot:

- Rules vs Learning-Based Approach
- Imitation Learning
- Reinforcement Learning
- Model-Based Learning dan World Models
- Language dan Multimodal Reasoning
- Vision-Language-Action Models

Kode dan notebook tersedia di folder:

`Bagian 4 — Bagaimana Robot Mengambil Keputusan?/Handson/`

### Bagian 5 — Mulai dari Simulasi

Bagian ini memperkenalkan workflow eksperimen Embodied AI menggunakan simulator.

Hands-on yang tersedia:

- Python Dasar untuk Embodied AI
- Menyiapkan Development Environment
- Memulai dengan MuJoCo
- Memulai dengan AI2-THOR
- Memulai dengan Isaac Sim

Materi praktik tersedia di folder:

`Bagian 5 — Mulai dari Simulasi/Handson/`

## Panduan Teknis Pendamping

Untuk pembaca yang baru memulai Python atau workflow pengembangan AI, tersedia tiga panduan teknis di folder `Assets/`:

1. **Panduan Teknis 01 — Memulai dengan Python dan Dasar Pemrograman**
2. **Panduan Teknis 02 — Virtual Environment dan Dependensi**
3. **Panduan Teknis 03 — Jupyter Notebook dan Google Colab**

Panduan tersebut membahas langkah-langkah dasar yang dibutuhkan sebelum menjalankan sebagian hands-on di repository.

## Memulai

Clone repository:

```bash
git clone https://github.com/muhamuttaqien/Mengenal-Embodied-AI.git
cd Mengenal-Embodied-AI
```

Setelah itu, masuk ke folder hands-on yang ingin dicoba. Setiap eksperimen dapat memiliki kebutuhan dependency yang berbeda, sehingga baca `README.md` dan `requirements.txt` pada folder terkait jika tersedia.

Sebagai praktik yang disarankan, gunakan **virtual environment** terpisah agar dependency dari satu eksperimen tidak mengganggu eksperimen lain.

Contoh:

```bash
python3 -m venv embodied-ai-env
source embodied-ai-env/bin/activate
python -m pip install --upgrade pip
```

Beberapa hands-on, terutama yang menggunakan simulator atau model AI berukuran besar, dapat membutuhkan GPU atau konfigurasi environment tambahan.

## Struktur Singkat

```text
Mengenal-Embodied-AI/
├── Assets/
├── Bagian 1 — Mengenal Embodied AI/
├── Bagian 2 — Mengenal Robot dan Dunia Fisik/
├── Bagian 3 — Tantangan Utama dalam Embodied AI/
│   └── Handson/
├── Bagian 4 — Bagaimana Robot Mengambil Keputusan?/
│   └── Handson/
├── Bagian 5 — Mulai dari Simulasi/
│   └── Handson/
└── Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata.docx
```

## Naskah Buku

Versi kerja naskah utama juga tersedia di repository:

**`Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata.docx`**

Karena buku masih dalam pengembangan, struktur folder, kode, gambar, dan naskah dapat terus diperbarui.

## Penulis

**Muhammad Angga Muttaqien, M.Eng.**

Fokus pada Artificial Intelligence, Embodied AI, robot learning, Vision-Language-Action models, dan world models untuk robotika.

---

Repository ini dibuat sebagai pendamping praktis agar pembaca dapat mengikuti eksperimen yang dibahas di dalam buku secara lebih langsung.
