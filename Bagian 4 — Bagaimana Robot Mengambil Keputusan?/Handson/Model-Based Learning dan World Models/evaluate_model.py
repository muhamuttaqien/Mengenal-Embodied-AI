# Import Path untuk mengatur path file.
from pathlib import Path

# Import NumPy untuk membaca dataset.
import numpy as np

# Import PyTorch.
import torch

# Import dynamics model.
from world_model import DynamicsModel


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent

# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"

# Menentukan file input.
TEST_DATA_PATH = (
    RESULTS_DIR
    / "test_transitions.npz"
)

MODEL_PATH = (
    RESULTS_DIR
    / "world_model.pt"
)

# Menentukan file hasil evaluasi.
EVALUATION_OUTPUT_PATH = (
    RESULTS_DIR
    / "evaluation_result.txt"
)


# Membaca testing data.
data = np.load(
    TEST_DATA_PATH
)


# Mengubah state menjadi tensor.
states = torch.tensor(
    data["states"],
    dtype=torch.float32,
)

# Mengubah action menjadi tensor.
actions = torch.tensor(
    data["actions"],
    dtype=torch.float32,
)

# Mengubah true next state menjadi tensor.
true_next_states = torch.tensor(
    data["next_states"],
    dtype=torch.float32,
)


# Membuat dynamics model.
model = DynamicsModel()

# Membaca trained model.
model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location="cpu",
    )
)

# Mengubah model ke evaluation mode.
model.eval()


# Memprediksi next state tanpa gradient.
with torch.no_grad():
    predicted_next_states = (
        model.predict_next_state(
            states,
            actions,
        )
    )


# Menghitung MSE pada testing data.
mse = torch.mean(
    (
        predicted_next_states
        - true_next_states
    ) ** 2
).item()


# Menyimpan baris hasil evaluasi.
result_lines = [
    f"Test next-state MSE: {mse:.8f}",
    "",
    "Example predictions:",
]


# Menampilkan hasil MSE.
print(
    result_lines[0]
)

print(
    "\nExample predictions:"
)


# Menampilkan beberapa contoh prediction.
for index in range(
    5
):
    # Membaca sample.
    state = states[
        index
    ].numpy()

    action = actions[
        index
    ].numpy()

    true_next = true_next_states[
        index
    ].numpy()

    predicted_next = predicted_next_states[
        index
    ].numpy()

    # Membuat teks hasil sample.
    sample_lines = [
        "",
        f"State: {state}",
        f"Action: {action}",
        f"True next state: {true_next}",
        f"Predicted next state: {predicted_next}",
    ]

    # Menampilkan sample ke terminal.
    for line in sample_lines:
        print(
            line
        )

    # Menyimpan sample ke hasil evaluasi.
    result_lines.extend(
        sample_lines
    )


# Menyimpan hasil evaluasi ke file.
EVALUATION_OUTPUT_PATH.write_text(
    "\n".join(
        result_lines
    ),
    encoding="utf-8",
)


print(
    "\nEvaluation result saved to:",
    EVALUATION_OUTPUT_PATH,
)
