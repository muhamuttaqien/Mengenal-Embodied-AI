# Import modul neural network PyTorch.
import torch.nn as nn


class RobotPolicy(nn.Module):
    # Membuat neural network sederhana sebagai policy.
    def __init__(self):
        super().__init__()

        # Menentukan arsitektur neural network.
        self.network = nn.Sequential(
            nn.Linear(3, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
        )

    # Menjalankan forward pass.
    def forward(self, observation):
        return self.network(observation)
