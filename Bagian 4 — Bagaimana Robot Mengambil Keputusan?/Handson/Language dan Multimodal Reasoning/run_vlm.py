# Import argparse untuk membaca argument command-line.
import argparse

# Import Path untuk mengatur path file.
from pathlib import Path

# Import PyTorch untuk inference model.
import torch

# Import processor dan Vision-Language Model.
from transformers import (
    AutoProcessor,
    Qwen2_5_VLForConditionalGeneration,
)

# Import helper function.
from multimodal_utils import (
    load_image,
    build_robot_prompt,
)


# Menentukan pretrained model yang digunakan.
MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"


# Menentukan folder script.
BASE_DIR = Path(__file__).resolve().parent

# Menentukan folder hasil.
RESULTS_DIR = BASE_DIR / "results"

# Membuat folder results jika belum ada.
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# Menentukan file hasil text.
OUTPUT_PATH = (
    RESULTS_DIR
    / "vlm_response.txt"
)


def main():
    # Membuat command-line parser.
    parser = argparse.ArgumentParser(
        description=(
            "Menjalankan Vision-Language Model "
            "untuk memahami image dan instruction."
        )
    )

    # Menentukan input image.
    parser.add_argument(
        "--image",
        required=True,
        help="Path menuju input image.",
    )

    # Menentukan instruction.
    parser.add_argument(
        "--instruction",
        required=True,
        help="Natural-language instruction untuk robot.",
    )

    # Membaca argument.
    args = parser.parse_args()


    # Membuka image dan mengubahnya menjadi RGB.
    image = load_image(
        args.image
    )


    # Membuat prompt untuk task robot.
    prompt = build_robot_prompt(
        args.instruction
    )


    # Load processor pretrained.
    print(
        "Loading processor:",
        MODEL_ID,
    )

    processor = AutoProcessor.from_pretrained(
        MODEL_ID
    )


    # Load Vision-Language Model pretrained.
    print(
        "Loading model:",
        MODEL_ID,
    )

    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype="auto",
        device_map="auto",
    )


    # Membuat multimodal message.
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image,
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        }
    ]


    # Mengubah message menjadi format prompt model.
    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )


    # Mengubah text dan image menjadi tensor.
    inputs = processor(
        text=[text],
        images=[image],
        padding=True,
        return_tensors="pt",
    )


    # Memindahkan input ke device model.
    inputs = inputs.to(
        model.device
    )


    # Menjalankan inference.
    with torch.no_grad():

        generated_ids = model.generate(
            **inputs,
            max_new_tokens=180,
        )


    # Mengambil token jawaban yang baru dihasilkan.
    generated_ids_trimmed = [
        output_ids[
            len(input_ids):
        ]
        for (
            input_ids,
            output_ids,
        )
        in zip(
            inputs.input_ids,
            generated_ids,
        )
    ]


    # Mengubah token menjadi text.
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )


    # Mengambil response pertama.
    response = output_text[0]


    # Menampilkan hasil inference.
    print(
        "\nModel response:\n"
    )

    print(
        response
    )


    # Menyimpan hasil inference.
    OUTPUT_PATH.write_text(
        response + "\n",
        encoding="utf-8",
    )


    # Menampilkan lokasi file hasil.
    print(
        "\Result saved to::",
        OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()
