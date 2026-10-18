# Import PyTorch untuk membangun Mini-VLA.
import torch
import torch.nn as nn


class MiniVLA(nn.Module):
    # Mini-VLA edukasional: vision + language -> robot action.
    def __init__(
        self,
        vocab_size=9,
        embedding_dim=32,
    ):
        super().__init__()

        # Vision encoder untuk image RGB 64 x 64.
        self.vision_encoder = nn.Sequential(
            nn.Conv2d(
                3,
                16,
                kernel_size=5,
                stride=2,
                padding=2,
            ),
            nn.ReLU(),
            nn.Conv2d(
                16,
                32,
                kernel_size=3,
                stride=2,
                padding=1,
            ),
            nn.ReLU(),
            nn.Conv2d(
                32,
                64,
                kernel_size=3,
                stride=2,
                padding=1,
            ),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(
                64 * 8 * 8,
                256,
            ),
            nn.ReLU(),
        )

        # Embedding untuk token instruction.
        self.token_embedding = nn.Embedding(
            vocab_size,
            embedding_dim,
            padding_idx=0,
        )

        # Mengubah language embedding menjadi feature vector.
        self.language_projection = nn.Sequential(
            nn.Linear(
                embedding_dim,
                64,
            ),
            nn.ReLU(),
        )

        # Menggabungkan feature vision dan language.
        self.fusion = nn.Sequential(
            nn.Linear(
                256 + 64,
                192,
            ),
            nn.ReLU(),
            nn.Linear(
                192,
                96,
            ),
            nn.ReLU(),
        )

        # Head untuk memilih target cell.
        self.cell_head = nn.Linear(
            96,
            9,
        )

        # Head untuk memprediksi gripper.
        self.gripper_head = nn.Linear(
            96,
            1,
        )

    def encode_language(self, tokens):
        # Mengubah token menjadi embedding.
        embedded = self.token_embedding(
            tokens
        )

        # Membuat mask agar padding tidak ikut dirata-ratakan.
        mask = (
            tokens != 0
        ).float().unsqueeze(-1)

        # Mengambil mean embedding dari token valid.
        pooled = (
            (embedded * mask).sum(dim=1)
            / mask.sum(dim=1).clamp(min=1.0)
        )

        # Memproyeksikan language feature.
        return self.language_projection(
            pooled
        )

    def forward(self, image, tokens):
        # Mengambil visual feature.
        vision_features = self.vision_encoder(
            image
        )

        # Mengambil language feature.
        language_features = self.encode_language(
            tokens
        )

        # Menggabungkan kedua modality.
        multimodal_features = torch.cat(
            [
                vision_features,
                language_features,
            ],
            dim=1,
        )

        # Membuat fused representation.
        fused = self.fusion(
            multimodal_features
        )

        # Menghasilkan target-cell logits.
        cell_logits = self.cell_head(
            fused
        )

        # Menghasilkan gripper logit.
        gripper_logit = self.gripper_head(
            fused
        ).squeeze(1)

        return (
            cell_logits,
            gripper_logit,
        )
