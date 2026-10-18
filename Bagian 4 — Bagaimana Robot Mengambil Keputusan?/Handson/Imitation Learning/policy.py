# Import neural network module dari PyTorch.
import torch.nn as nn


class BehaviorCloningPolicy(nn.Module):
    # Membuat neural network policy.
    def __init__(self):
        super().__init__()

        # Membuat network observation ke action.
        self.network = nn.Sequential(
            nn.Linear(
                4,
                64,
            ),
            nn.ReLU(),
            nn.Linear(
                64,
                64,
            ),
            nn.ReLU(),
            nn.Linear(
                64,
                2,
            ),
            nn.Tanh(),
        )

    # Menghasilkan action dari observation.
    def forward(
        self,
        observation,
    ):
        return self.network(
            observation
        )
