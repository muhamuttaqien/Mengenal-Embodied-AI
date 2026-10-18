# Import argparse untuk membaca argumen dari terminal.
import argparse

# Import Path untuk mengelola path file dan folder.
from pathlib import Path

# Import textwrap untuk merapikan label panjang.
import textwrap

# Import torch untuk menjalankan CLIP.
import torch

# Import PIL untuk membuka gambar.
from PIL import Image

# Import matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import CLIP dari Hugging Face.
from transformers import CLIPModel, CLIPProcessor


# Folder tempat script berada.
BASE_DIR = Path(__file__).resolve().parent

# Folder untuk menyimpan hasil.
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def parse_args():
    # Membuat parser argumen terminal.
    parser = argparse.ArgumentParser(
        description="Membandingkan image dengan beberapa candidate text menggunakan CLIP."
    )

    # Path gambar.
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path gambar, misalnya person.jpg",
    )

    # Candidate text langsung dari terminal.
    parser.add_argument(
        "--texts",
        nargs="+",
        default=None,
        help="Candidate text yang ditulis langsung di terminal.",
    )

    # Candidate text dari file.
    parser.add_argument(
        "--texts-file",
        type=str,
        default=None,
        help="File text dengan satu candidate pada setiap baris.",
    )

    # Nama file visualisasi.
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path output visualisasi.",
    )

    return parser.parse_args()


def resolve_path(path_string):
    # Membaca path yang diberikan pengguna.
    path = Path(path_string)

    # Gunakan langsung jika ditemukan.
    if path.exists():
        return path

    # Coba cari relatif terhadap folder script.
    script_path = BASE_DIR / path

    if script_path.exists():
        return script_path

    # Jika tidak ditemukan, kembalikan path awal.
    return path


def load_text_candidates(args):
    # Jika menggunakan --texts-file.
    if args.texts_file is not None:
        texts_path = resolve_path(args.texts_file)

        if not texts_path.exists():
            raise FileNotFoundError(
                f"File candidate text tidak ditemukan: {texts_path}"
            )

        # Membaca setiap baris yang tidak kosong.
        texts = [
            line.strip()
            for line in texts_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        if len(texts) == 0:
            raise ValueError(
                f"Tidak ada candidate text di dalam: {texts_path}"
            )

        return texts

    # Jika menggunakan --texts.
    if args.texts is not None:
        return args.texts

    # Candidate default jika tidak ada argumen text.
    return [
        "a person wearing a blue shirt and holding a bottle",
        "a person sitting in front of a laptop",
        "a bottle being held by a person",
        "a red car on the street",
    ]


def print_similarity_table(image_name, ranked_results):
    # Menampilkan nama gambar.
    print()
    print(f"Image: {image_name}")
    print()

    # Header tabel.
    print(
        f"{'Cosine':>8} | "
        f"{'Relative':>10} | "
        f"Text Candidate"
    )

    print("-" * 80)

    # Menampilkan ranking.
    for text, similarity, probability in ranked_results:
        print(
            f"{similarity:8.4f} | "
            f"{probability * 100:9.2f}% | "
            f"{text}"
        )


def save_similarity_scores(image_name, ranked_results):
    # Path hasil text.
    output_path = RESULTS_DIR / "clip_similarity_scores.txt"

    lines = []

    lines.append(f"Image: {image_name}")
    lines.append("")
    lines.append(
        f"{'Cosine Similarity':>18} | "
        f"{'Relative Probability':>20} | "
        f"Text Candidate"
    )
    lines.append("-" * 100)

    # Menulis setiap candidate.
    for text, similarity, probability in ranked_results:
        lines.append(
            f"{similarity:18.4f} | "
            f"{probability * 100:19.2f}% | "
            f"{text}"
        )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print()
    print(f"Similarity scores disimpan ke: {output_path}")


def create_visualization(
    image,
    ranked_results,
    output_path,
):
    # Mengambil candidate text.
    labels = [
        text
        for text, _, _ in ranked_results
    ]

    # Mengambil cosine similarity.
    similarities = [
        similarity
        for _, similarity, _ in ranked_results
    ]

    # Membungkus teks agar label tidak terlalu panjang.
    labels = [
        "\n".join(
            textwrap.wrap(
                label,
                width=34,
            )
        )
        for label in labels
    ]

    # Membalik urutan agar similarity tertinggi berada di atas.
    labels_plot = labels[::-1]
    similarities_plot = similarities[::-1]

    # Membuat figure dua panel.
    fig, (ax_image, ax_chart) = plt.subplots(
        1,
        2,
        figsize=(14, 6),
        gridspec_kw={
            "width_ratios": [1.0, 1.6]
        },
    )

    # Menampilkan input image.
    ax_image.imshow(image)
    ax_image.set_title(
        "Input Image",
        fontsize=14,
    )
    ax_image.axis("off")

    # Membuat horizontal bar chart.
    bars = ax_chart.barh(
        labels_plot,
        similarities_plot,
    )

    ax_chart.set_title(
        "CLIP Image-Text Similarity",
        fontsize=14,
    )

    ax_chart.set_xlabel(
        "Cosine Similarity"
    )

    # Menentukan batas sumbu X.
    minimum = min(similarities)
    maximum = max(similarities)

    x_min = min(
        0.0,
        minimum - 0.05,
    )

    x_max = maximum + 0.08

    ax_chart.set_xlim(
        x_min,
        x_max,
    )

    ax_chart.grid(
        axis="x",
        alpha=0.25,
    )

    # Menampilkan nilai similarity pada bar.
    padding = max(
        0.01,
        (x_max - x_min) * 0.015,
    )

    for bar, similarity in zip(
        bars,
        similarities_plot,
    ):
        ax_chart.text(
            similarity + padding,
            bar.get_y() + bar.get_height() / 2,
            f"{similarity:.3f}",
            va="center",
            fontsize=10,
        )

    # Merapikan layout.
    plt.tight_layout()

    # Menyimpan visualisasi.
    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    print(
        f"Visualization saved to: {output_path}"
    )

    # Menampilkan visualisasi.
    plt.show()

    # Menutup figure setelah window ditutup.
    plt.close()


def main():
    # Membaca argumen.
    args = parse_args()

    # Menentukan device.
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(f"Device: {device}")

    # Membaca path gambar.
    image_path = resolve_path(
        args.image
    )

    if not image_path.exists():
        raise FileNotFoundError(
            f"Gambar tidak ditemukan: {image_path}"
        )

    # Membaca candidate text.
    texts = load_text_candidates(
        args
    )

    print(
        f"Jumlah candidate text: {len(texts)}"
    )

    # Membuka image.
    image = Image.open(
        image_path
    ).convert("RGB")

    # Nama model CLIP.
    model_name = (
        "openai/clip-vit-base-patch32"
    )

    print(
        f"Loading CLIP model: {model_name}"
    )

    # Load processor.
    processor = CLIPProcessor.from_pretrained(
        model_name
    )

    # Load model.
    model = CLIPModel.from_pretrained(
        model_name
    )

    # Memindahkan model ke device.
    model = model.to(
        device
    )

    # Mode evaluasi.
    model.eval()

    # Menyiapkan input.
    inputs = processor(
        text=texts,
        images=image,
        return_tensors="pt",
        padding=True,
    )

    # Memindahkan tensor ke device.
    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    # Menjalankan inference.
    with torch.no_grad():
        outputs = model(
            **inputs
        )

        # Image embedding.
        image_embedding = (
            outputs.image_embeds
        )

        # Text embeddings.
        text_embeddings = (
            outputs.text_embeds
        )

        # Normalisasi image embedding.
        image_embedding = (
            image_embedding
            / image_embedding.norm(
                dim=-1,
                keepdim=True,
            )
        )

        # Normalisasi text embedding.
        text_embeddings = (
            text_embeddings
            / text_embeddings.norm(
                dim=-1,
                keepdim=True,
            )
        )

        # Menghitung cosine similarity.
        similarities = (
            image_embedding
            @ text_embeddings.T
        )

        similarities = (
            similarities
            .squeeze(0)
            .cpu()
            .numpy()
        )

        # Menghitung relative probability.
        probabilities = (
            outputs.logits_per_image
            .softmax(dim=1)
            .squeeze(0)
            .cpu()
            .numpy()
        )

    # Menggabungkan hasil.
    results = list(
        zip(
            texts,
            similarities,
            probabilities,
        )
    )

    # Mengurutkan berdasarkan cosine similarity.
    ranked_results = sorted(
        results,
        key=lambda item: item[1],
        reverse=True,
    )

    # Menampilkan hasil di terminal.
    print_similarity_table(
        image_path.name,
        ranked_results,
    )

    # Menyimpan hasil text.
    save_similarity_scores(
        image_path.name,
        ranked_results,
    )

    # Menentukan path visualisasi.
    if args.output is None:
        output_path = (
            RESULTS_DIR
            / "clip_similarity_result.png"
        )
    else:
        output_path = Path(
            args.output
        )

        if not output_path.is_absolute():
            output_path = (
                BASE_DIR
                / output_path
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    # Membuat visualisasi.
    create_visualization(
        image=image,
        ranked_results=ranked_results,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
