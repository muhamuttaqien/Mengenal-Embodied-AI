# Import PyTorch.
import torch

# Import neural network module.
import torch.nn as nn


class DynamicsModel(nn.Module):
    # Membuat dynamics model sederhana.
    def __init__(self):
        super().__init__()

        # Membuat neural network untuk memprediksi perubahan state.
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
        )

    def forward(
        self,
        state,
        action,
    ):
        # Menggabungkan state dan action sebagai input model.
        model_input = torch.cat(
            [
                state,
                action,
            ],
            dim=-1,
        )

        # Memprediksi perubahan state.
        delta_state = self.network(
            model_input
        )

        return delta_state

    def predict_next_state(
        self,
        state,
        action,
    ):
        # Memprediksi perubahan state.
        delta_state = self.forward(
            state,
            action,
        )

        # Menghitung next state.
        return (
            state
            + delta_state
        )
