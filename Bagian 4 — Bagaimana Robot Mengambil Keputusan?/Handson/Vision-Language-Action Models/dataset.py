# Import NumPy untuk membaca dataset.
import numpy as np

# Import PyTorch untuk membuat tensor dan Dataset.
import torch
from torch.utils.data import Dataset


# Daftar warna target.
COLORS = [
    "red",
    "green",
    "blue",
]

# Daftar jenis instruction.
VERBS = [
    "move",
    "pick",
]

# Vocabulary sederhana untuk instruction.
VOCAB = {
    "<pad>": 0,
    "move": 1,
    "pick": 2,
    "to": 3,
    "the": 4,
    "red": 5,
    "green": 6,
    "blue": 7,
    "block": 8,
}

# Panjang maksimal token instruction.
MAX_TOKENS = 5

# Koordinat normalized untuk workspace 3 x 3.
GRID_POINTS = np.array(
    [
        [0.20, 0.20],
        [0.50, 0.20],
        [0.80, 0.20],
        [0.20, 0.50],
        [0.50, 0.50],
        [0.80, 0.50],
        [0.20, 0.80],
        [0.50, 0.80],
        [0.80, 0.80],
    ],
    dtype=np.float32,
)


def instruction_from_ids(verb_id, color_id):
    # Mengubah ID menjadi kata.
    verb = VERBS[verb_id]
    color = COLORS[color_id]

    # Membentuk instruction sesuai jenis action.
    if verb == "move":
        return f"move to the {color} block"

    return f"pick the {color} block"


def tokenize_instruction(text):
    # Mengubah setiap kata menjadi token ID.
    tokens = [
        VOCAB[word]
        for word in text.split()
    ]

    # Membatasi panjang token.
    tokens = tokens[:MAX_TOKENS]

    # Menambahkan padding jika diperlukan.
    tokens += [0] * (
        MAX_TOKENS
        - len(tokens)
    )

    return torch.tensor(
        tokens,
        dtype=torch.long,
    )


class SyntheticVLADataset(Dataset):
    # Dataset untuk Mini-VLA.
    def __init__(self, file_path):
        # Membaca file dataset.
        data = np.load(file_path)

        # Menyimpan setiap komponen dataset.
        self.images = data["images"]
        self.color_ids = data["color_ids"]
        self.verb_ids = data["verb_ids"]
        self.target_cells = data["target_cells"]
        self.gripper = data["gripper"]

    def __len__(self):
        # Mengembalikan jumlah sample.
        return len(self.target_cells)

    def __getitem__(self, index):
        # Normalisasi image ke rentang 0 sampai 1.
        image = (
            self.images[index].astype(np.float32)
            / 255.0
        )

        # Mengubah format image menjadi C x H x W.
        image = torch.tensor(
            image,
            dtype=torch.float32,
        ).permute(
            2,
            0,
            1,
        )

        # Membaca metadata instruction.
        color_id = int(self.color_ids[index])
        verb_id = int(self.verb_ids[index])

        # Membentuk natural-language instruction.
        instruction = instruction_from_ids(
            verb_id,
            color_id,
        )

        # Mengubah instruction menjadi token.
        tokens = tokenize_instruction(
            instruction
        )

        # Membuat target cell.
        target_cell = torch.tensor(
            self.target_cells[index],
            dtype=torch.long,
        )

        # Membuat target gripper.
        gripper = torch.tensor(
            self.gripper[index],
            dtype=torch.float32,
        )

        return {
            "image": image,
            "tokens": tokens,
            "target_cell": target_cell,
            "gripper": gripper,
            "instruction": instruction,
        }
