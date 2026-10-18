# Bagian 5 — Python Dasar untuk Embodied AI

Repository pendamping untuk subbagian **Python Dasar untuk Embodied AI** pada buku:

**Mengenal Embodied AI: Dari Teori, Simulasi hingga Robot Nyata**

Repository ini memperkenalkan beberapa bentuk data yang paling sering muncul dalam Embodied AI:

```text
Array
  ↓
Robot State / Sensor Data

Image
  ↓
Visual Observation

Tensor
  ↓
Input / Output Model AI

Observation
  ↓
Policy
  ↓
Action
  ↓
Environment
```

Tujuannya bukan mempelajari seluruh Python, tetapi memahami bagian-bagian Python yang akan sering digunakan ketika mulai bekerja dengan MuJoCo, AI2-THOR, Isaac Sim, dan model AI.

---

## 1. Struktur Repository

```text
Bagian_5_Python_Dasar_Embodied_AI/
├── scripts/
│   ├── 01_array_as_state.py
│   ├── 02_image_as_observation.py
│   ├── 03_tensor_basics.py
│   └── 04_observation_action_loop.py
├── assets/
│   └── scene.jpg
├── results/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 2. Environment

Gunakan environment utama yang sudah dibuat pada subbagian sebelumnya:

```bash
# Mengaktifkan environment utama pada Linux/macOS.
source embodied-ai-env/bin/activate
```

Pada Windows:

```bat
REM Mengaktifkan environment utama.
embodied-ai-env\Scripts\activate
```

Jika dependency belum tersedia, jalankan:

```bash
# Memasang package yang diperlukan repository ini.
pip install -r requirements.txt
```

Repository ini tidak membutuhkan GPU.

---

# 3. Array sebagai Robot State

File:

```text
scripts/01_array_as_state.py
```

Jalankan:

```bash
# Menjalankan contoh array sebagai robot state.
python scripts/01_array_as_state.py
```

Contoh ini menggunakan tiga nilai sensor:

```text
LEFT
FRONT
RIGHT
```

yang direpresentasikan sebagai NumPy array:

```python
# Membuat observation dengan tiga sensor jarak.
observation = np.array([0.4, 0.8, 0.3], dtype=np.float32)
```

Kemudian kita mengambil setiap nilai:

```python
# Membaca sensor kiri.
left = observation[0]

# Membaca sensor depan.
front = observation[1]

# Membaca sensor kanan.
right = observation[2]
```

Lalu memilih arah yang paling terbuka:

```python
# Memilih index dengan nilai sensor terbesar.
action_index = np.argmax(observation)
```

Konsep utamanya:

```text
Numerical Array
      ↓
Robot / Sensor State
      ↓
Simple Decision
```

Dalam robot nyata atau simulator, array seperti ini dapat berisi:

- joint position,
- joint velocity,
- position,
- orientation,
- distance sensor,
- force sensor,
- dan data numerik lainnya.

---

# 4. Image sebagai Observation

File:

```text
scripts/02_image_as_observation.py
```

Jalankan:

```bash
# Membaca image dan memeriksa representasi array-nya.
python scripts/02_image_as_observation.py
```

Input image tersedia di:

```text
assets/scene.jpg
```

Program membukanya dengan Pillow:

```python
# Membuka image dari folder assets.
image = Image.open("assets/scene.jpg").convert("RGB")
```

Kemudian image diubah menjadi NumPy array:

```python
# Mengubah image menjadi array numerik.
image_array = np.array(image)
```

Jika image memiliki resolusi:

```text
640 × 480
```

maka shape-nya:

```text
(480, 640, 3)
```

Artinya:

```text
480 → image height
640 → image width
3   → RGB channels
```

Program juga membaca satu pixel:

```python
# Membaca pixel di bagian tengah image.
center_pixel = image_array[height // 2, width // 2]
```

Ini menunjukkan bahwa sebuah camera observation pada akhirnya tetap berupa kumpulan angka.

Program menyimpan salinan image ke:

```text
results/image_observation_copy.png
```

---

# 5. Tensor untuk Model AI

File:

```text
scripts/03_tensor_basics.py
```

Jalankan:

```bash
# Menjalankan contoh NumPy array ke PyTorch tensor.
python scripts/03_tensor_basics.py
```

Program dimulai dari NumPy array:

```python
# Membuat observation sebagai NumPy array.
observation = np.array([0.4, 0.8, 0.3], dtype=np.float32)
```

Kemudian diubah menjadi tensor:

```python
# Mengubah NumPy array menjadi PyTorch tensor.
observation_tensor = torch.tensor(observation, dtype=torch.float32)
```

Tensor merupakan representasi data utama yang digunakan oleh PyTorch.

Program juga memilih device:

```python
# Memilih CUDA jika tersedia, jika tidak gunakan CPU.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

Kemudian tensor dipindahkan:

```python
# Memindahkan tensor ke device yang dipilih.
observation_tensor = observation_tensor.to(device)
```

Konsep utamanya:

```text
Sensor / Image Data
        ↓
NumPy Array
        ↓
PyTorch Tensor
        ↓
AI Model
```

Pada subbagian ini GPU tidak wajib. Jika CUDA tidak tersedia, tensor tetap berjalan dengan CPU.

---

# 6. Observation-Action Loop

File:

```text
scripts/04_observation_action_loop.py
```

Jalankan:

```bash
# Menjalankan observation-action loop sederhana.
python scripts/04_observation_action_loop.py
```

Ini adalah script terpenting dalam repository karena memperkenalkan pola dasar Embodied AI:

```text
Environment
     ↓
Observation
     ↓
Policy
     ↓
Action
     ↓
Environment
     ↓
Next Observation
```

Environment sederhana menghasilkan tiga sensor jarak:

```python
# Menghasilkan observation baru dari environment.
observation = environment.get_observation()
```

Policy memilih arah:

```python
# Menentukan action dari observation.
action = policy(observation)
```

Kemudian action dikirim kembali ke environment:

```python
# Menjalankan action pada environment.
environment.step(action)
```

Pada repository ini environment masih sederhana dan tidak menggunakan simulator 3D.

Namun pada MuJoCo, AI2-THOR, atau Isaac Sim, strukturnya tetap serupa:

```text
observation = simulator observation
action      = policy(observation)
simulator.step(action)
```

---

# 7. Mengenal `observation`

Dalam Embodied AI, `observation` adalah informasi yang tersedia bagi agent pada suatu timestep.

Contohnya:

```text
Distance sensor
Joint position
Joint velocity
RGB image
Depth image
Robot pose
Object position
```

Observation tidak selalu sama dengan seluruh state environment. Agent hanya dapat mengambil keputusan berdasarkan informasi yang diberikan kepadanya.

---

# 8. Mengenal `policy`

Policy adalah mekanisme yang menentukan action berdasarkan observation:

```text
observation
     ↓
policy
     ↓
action
```

Pada repository ini policy masih berupa rules sederhana:

```python
# Memilih arah dengan jarak obstacle terbesar.
action = int(np.argmax(observation))
```

Pada bagian lain buku, policy dapat diganti menjadi:

```text
Neural Network
Imitation Learning
Reinforcement Learning
World Model
Vision-Language-Action Model
```

Walaupun metode policy berubah, konsep interface-nya tetap:

```text
action = policy(observation)
```

---

# 9. Mengenal `action`

Action adalah keputusan yang dikirim dari agent ke environment.

Dalam contoh kita:

```text
0 → LEFT
1 → FORWARD
2 → RIGHT
```

Pada robot yang lebih kompleks, action dapat berupa:

```text
Joint angle
Joint velocity
Motor torque
End-effector position
Gripper command
Action chunk
```

---

# 10. Urutan Hands-on yang Direkomendasikan

Jalankan script secara berurutan:

```text
01_array_as_state.py
        ↓
02_image_as_observation.py
        ↓
03_tensor_basics.py
        ↓
04_observation_action_loop.py
```

Progression-nya:

```text
Numbers
   ↓
Array
   ↓
Image
   ↓
Tensor
   ↓
Observation-Action Loop
```

Setelah memahami pola ini, kita sudah memiliki dasar Python yang cukup untuk masuk ke simulator pertama, yaitu **MuJoCo**.

---

# 11. Hubungan dengan Subbagian Berikutnya

Kode sederhana:

```python
# Membaca observation.
observation = environment.get_observation()

# Menghasilkan action.
action = policy(observation)

# Menjalankan action.
environment.step(action)
```

akan muncul kembali dalam bentuk yang lebih nyata:

```text
Python Environment
       ↓
MuJoCo
       ↓
AI2-THOR
       ↓
Isaac Sim
```

Perbedaannya hanya pada sumber observation dan bentuk action.

---

# 12. Catatan

Semua script sengaja dibuat kecil dan setiap langkah utama diberi komentar.

Tujuan repository ini adalah:

```text
understand data
      ↓
understand observation
      ↓
understand action
      ↓
understand loop
```

Kita belum membangun robot AI yang kompleks. Fokusnya adalah memahami bentuk data dan aliran program yang akan terus digunakan sepanjang pembahasan Embodied AI.
