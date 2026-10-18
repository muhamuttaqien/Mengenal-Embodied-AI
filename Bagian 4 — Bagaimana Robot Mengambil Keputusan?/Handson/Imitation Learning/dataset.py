# Import NumPy untuk membaca demonstration data.
import numpy as np

# Import PyTorch.
import torch

# Import Dataset dari PyTorch.
from torch.utils.data import Dataset


class DemonstrationDataset(Dataset):
    # Membuat dataset dari file observation-action.
    def __init__(
        self,
        file_path,
    ):
        # Membaca file demonstration.
        data = np.load(
            file_path
        )

        # Mengubah observations menjadi tensor.
        self.observations = torch.tensor(
            data["observations"],
            dtype=torch.float32,
        )

        # Mengubah actions menjadi tensor.
        self.actions = torch.tensor(
            data["actions"],
            dtype=torch.float32,
        )

    # Mengembalikan jumlah demonstration.
    def __len__(self):
        return len(
            self.observations
        )

    # Mengembalikan satu pasangan observation-action.
    def __getitem__(
        self,
        index,
    ):
        return (
            self.observations[index],
            self.actions[index],
        )
