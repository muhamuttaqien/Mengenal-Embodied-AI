# Import argparse untuk membaca argumen dari terminal.
import argparse

# Import json untuk menyimpan action dalam format JSON.
import json

# Import Path untuk mengelola file hasil.
from pathlib import Path

# Import NumPy untuk menyimpan action vector.
import numpy as np

# Import PyTorch untuk inference OpenVLA.
import torch

# Import PIL untuk membuka image.
from PIL import Image

# Import model dan processor dari Hugging Face.
from transformers import (
    AutoModelForVision2Seq,
    AutoProcessor,
)

# Import fungsi visualisasi action.
from visualize_action import (
    save_action_visualizations,
)


# Model OpenVLA yang digunakan.
MODEL_ID = "openvla/openvla-7b"

# Folder utama script.
BASE_DIR = Path(__file__).resolve().parent

# Semua hasil disimpan ke folder results.
DEFAULT_RESULTS_DIR = BASE_DIR / "results"


def choose_dtype():
    # Menggunakan float32 jika CUDA tidak tersedia.
    if not torch.cuda.is_available():
        return torch.float32

    # Membaca compute capability GPU.
    major, _ = torch.cuda.get_device_capability()

    # GPU modern menggunakan bfloat16.
    if major >= 8:
        return torch.bfloat16

    # GPU lama menggunakan float16.
    return torch.float16


def load_openvla():
    # OpenVLA-7B sangat disarankan dijalankan dengan GPU.
    if not torch.cuda.is_available():
        raise RuntimeError(
            "A CUDA GPU is strongly recommended "
            "for OpenVLA-7B inference."
        )

    # Memilih dtype sesuai GPU.
    dtype = choose_dtype()

    print("Loading processor...")

    # Load processor OpenVLA.
    processor = AutoProcessor.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
    )

    print("Loading OpenVLA...")

    # Load pretrained OpenVLA.
    model = AutoModelForVision2Seq.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        device_map="auto",
    )

    # Mengaktifkan evaluation mode.
    model.eval()

    return (
        processor,
        model,
        dtype,
    )


def predict_action(
    image,
    instruction,
    processor,
    model,
    dtype,
    unnorm_key="bridge_orig",
):
    # Membuat prompt sesuai format OpenVLA.
    prompt = (
        "In: What action should the robot take to "
        f"{instruction.lower()}?\nOut:"
    )

    # Membaca device tempat model berada.
    input_device = next(
        model.parameters()
    ).device

    # Memproses image dan language instruction.
    inputs = processor(
        prompt,
        image,
    ).to(
        input_device,
        dtype=dtype,
    )

    # Menjalankan inference tanpa gradient.
    with torch.no_grad():
        action = model.predict_action(
            **inputs,
            unnorm_key=unnorm_key,
            do_sample=False,
        )

    # Mengubah action menjadi NumPy array.
    return np.asarray(
        action,
        dtype=np.float32,
    )


def save_action(
    action,
    output_dir,
    instruction,
    unnorm_key,
):
    # Memastikan folder hasil tersedia.
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Path output raw action.
    npy_path = (
        output_dir
        / "openvla_action.npy"
    )
    json_path = (
        output_dir
        / "openvla_action.json"
    )

    # Menyimpan raw action dalam format NumPy.
    np.save(
        npy_path,
        action,
    )

    # Membuat record yang mudah dibaca.
    record = {
        "instruction": instruction,
        "unnorm_key": unnorm_key,
        "action_labels": [
            "delta_x",
            "delta_y",
            "delta_z",
            "delta_roll",
            "delta_pitch",
            "delta_yaw",
            "gripper",
        ],
        "action": [
            float(x)
            for x in action
        ],
    }

    # Menyimpan action dalam format JSON.
    json_path.write_text(
        json.dumps(
            record,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("NumPy action saved to:", npy_path)
    print("JSON action saved to:", json_path)


def resolve_output_dir(output_dir):
    # Jika tidak diberikan, gunakan Bonus/results.
    if output_dir is None:
        return DEFAULT_RESULTS_DIR

    path = Path(output_dir)

    # Path relatif dibuat relatif terhadap folder Bonus.
    if not path.is_absolute():
        path = BASE_DIR / path

    return path


def main():
    # Membuat parser argumen terminal.
    parser = argparse.ArgumentParser(
        description=(
            "Run one OpenVLA inference and visualize "
            "the returned 7-DoF action."
        )
    )

    # Path input image.
    parser.add_argument(
        "--image",
        required=True,
        help="Path to an RGB image.",
    )

    # Natural-language robot instruction.
    parser.add_argument(
        "--instruction",
        required=True,
        help=(
            "Natural-language robot instruction, "
            'for example "pick up the red object".'
        ),
    )

    # Statistik action untuk un-normalization.
    parser.add_argument(
        "--unnorm-key",
        default="bridge_orig",
        help=(
            "Action un-normalization key. "
            "bridge_orig follows the official OpenVLA example."
        ),
    )

    # Folder output.
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output folder. Default: Bonus/results",
    )

    args = parser.parse_args()

    # Membaca input image.
    image_path = Path(args.image)

    if not image_path.is_absolute():
        image_path = BASE_DIR / image_path

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image = Image.open(
        image_path
    ).convert(
        "RGB"
    )

    # Menentukan folder hasil.
    output_dir = resolve_output_dir(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Load OpenVLA.
    (
        processor,
        model,
        dtype,
    ) = load_openvla()

    # Prediksi action.
    action = predict_action(
        image=image,
        instruction=args.instruction,
        processor=processor,
        model=model,
        dtype=dtype,
        unnorm_key=args.unnorm_key,
    )

    # Memastikan action memiliki tujuh dimensi.
    if action.shape != (7,):
        raise ValueError(
            f"Expected a 7-D action, got shape {action.shape}."
        )

    print()
    print("OpenVLA action:")
    print(action)

    # Menyimpan raw action.
    save_action(
        action=action,
        output_dir=output_dir,
        instruction=args.instruction,
        unnorm_key=args.unnorm_key,
    )

    # Membuat dan menampilkan visualisasi action.
    save_action_visualizations(
        action=action,
        output_dir=output_dir,
    )

    print()
    print("OpenVLA results saved to:", output_dir)


if __name__ == "__main__":
    main()
