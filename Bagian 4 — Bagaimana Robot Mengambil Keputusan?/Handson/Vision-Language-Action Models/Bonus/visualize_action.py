# Import argparse untuk membaca argumen dari terminal.
import argparse

# Import json untuk membaca action JSON.
import json

# Import Path untuk mengelola file hasil.
from pathlib import Path

# Import Matplotlib untuk visualisasi.
import matplotlib.pyplot as plt

# Import NumPy untuk memproses action vector.
import numpy as np


# Label tujuh dimensi action.
ACTION_LABELS = [
    "Δx",
    "Δy",
    "Δz",
    "Δroll",
    "Δpitch",
    "Δyaw",
    "gripper",
]

# Folder utama script.
BASE_DIR = Path(__file__).resolve().parent

# Folder hasil default.
DEFAULT_RESULTS_DIR = BASE_DIR / "results"


def load_action(path):
    # Membaca path action.
    path = Path(path)

    if not path.is_absolute():
        path = BASE_DIR / path

    if not path.exists():
        raise FileNotFoundError(
            f"Action file not found: {path}"
        )

    # Membaca action dari file NumPy.
    if path.suffix == ".npy":
        action = np.load(
            path
        )

    # Membaca action dari file JSON.
    elif path.suffix == ".json":
        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        action = np.asarray(
            data["action"],
            dtype=np.float32,
        )

    else:
        raise ValueError(
            "Action file must be .npy or .json"
        )

    # Memastikan action berupa vector 1D.
    action = np.asarray(
        action,
        dtype=np.float32,
    ).reshape(-1)

    # Memastikan action memiliki tujuh dimensi.
    if action.shape != (7,):
        raise ValueError(
            f"Expected 7 values, got shape {action.shape}."
        )

    return action


def save_action_bar_chart(action, output_path):
    # Membuat bar chart tujuh dimensi action.
    plt.figure(
        figsize=(9, 5)
    )

    plt.bar(
        ACTION_LABELS,
        action,
    )

    # Menambahkan garis nol.
    plt.axhline(
        0.0,
        linewidth=1,
    )

    plt.xlabel(
        "Action Dimension"
    )

    plt.ylabel(
        "Predicted Value"
    )

    plt.title(
        "OpenVLA 7-DoF Action Vector"
    )

    plt.grid(
        axis="y",
        alpha=0.25,
    )

    plt.tight_layout()

    # Menyimpan bar chart.
    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    print("Action bar chart saved to:", output_path)

    # Menampilkan bar chart.
    plt.show()

    # Menutup figure setelah window ditutup.
    plt.close()


def save_translation_vector(action, output_path):
    # Mengambil komponen translasi.
    dx, dy, dz = action[:3]

    # Menghitung magnitude translasi.
    magnitude = max(
        float(
            np.linalg.norm(
                action[:3]
            )
        ),
        1e-6,
    )

    # Menentukan batas plot 3D.
    limit = max(
        0.05,
        magnitude * 1.35,
    )

    # Membuat figure 3D.
    fig = plt.figure(
        figsize=(6, 6)
    )

    ax = fig.add_subplot(
        111,
        projection="3d",
    )

    # Menggambar predicted translation vector.
    ax.quiver(
        0,
        0,
        0,
        dx,
        dy,
        dz,
        arrow_length_ratio=0.12,
        linewidth=2,
    )

    # Menandai posisi end-effector saat ini.
    ax.scatter(
        [0],
        [0],
        [0],
        s=50,
        label="Current EE",
    )

    # Menandai predicted delta.
    ax.scatter(
        [dx],
        [dy],
        [dz],
        s=70,
        marker="*",
        label="Predicted Delta",
    )

    # Mengatur batas axis.
    ax.set_xlim(
        -limit,
        limit,
    )
    ax.set_ylim(
        -limit,
        limit,
    )
    ax.set_zlim(
        -limit,
        limit,
    )

    ax.set_xlabel(
        "Δx"
    )
    ax.set_ylabel(
        "Δy"
    )
    ax.set_zlabel(
        "Δz"
    )

    ax.set_title(
        "Predicted End-Effector Translation"
    )

    ax.legend()

    plt.tight_layout()

    # Menyimpan visualisasi vector.
    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    print("Translation vector saved to:", output_path)

    # Menampilkan visualisasi vector.
    plt.show()

    # Menutup figure setelah window ditutup.
    plt.close()


def save_action_summary(action, output_path):
    # Membuat ringkasan text tujuh dimensi action.
    lines = [
        "OpenVLA 7-DoF Action Summary",
        "",
        f"Δx      : {action[0]: .6f}",
        f"Δy      : {action[1]: .6f}",
        f"Δz      : {action[2]: .6f}",
        f"Δroll   : {action[3]: .6f}",
        f"Δpitch  : {action[4]: .6f}",
        f"Δyaw    : {action[5]: .6f}",
        f"gripper : {action[6]: .6f}",
        "",
        (
            "Note: axis/frame conventions and gripper semantics "
            "depend on the dataset/robot action convention."
        ),
    ]

    # Menyimpan summary.
    Path(output_path).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("Action summary saved to:", output_path)


def save_action_visualizations(
    action,
    output_dir=DEFAULT_RESULTS_DIR,
):
    # Menyiapkan folder hasil.
    output_dir = Path(output_dir)

    if not output_dir.is_absolute():
        output_dir = BASE_DIR / output_dir

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Menyimpan dan menampilkan bar chart.
    save_action_bar_chart(
        action,
        output_dir
        / "action_bar_chart.png",
    )

    # Menyimpan dan menampilkan vector translasi.
    save_translation_vector(
        action,
        output_dir
        / "translation_vector.png",
    )

    # Menyimpan ringkasan text.
    save_action_summary(
        action,
        output_dir
        / "action_summary.txt",
    )


def main():
    # Membuat parser argumen terminal.
    parser = argparse.ArgumentParser(
        description=(
            "Visualize a 7-DoF OpenVLA action."
        )
    )

    # File action hasil inference.
    parser.add_argument(
        "--action-file",
        help=(
            "Path to openvla_action.npy "
            "or openvla_action.json."
        ),
    )

    # Demo tanpa download OpenVLA.
    parser.add_argument(
        "--demo",
        action="store_true",
        help=(
            "Use a sample 7-D action "
            "to test the visualization."
        ),
    )

    # Folder hasil.
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output folder. Default: Bonus/results",
    )

    args = parser.parse_args()

    # Menggunakan action contoh.
    if args.demo:
        action = np.array(
            [
                0.035,
                -0.018,
                0.024,
                0.012,
                -0.020,
                0.008,
                0.91,
            ],
            dtype=np.float32,
        )

    # Membaca action hasil inference.
    elif args.action_file:
        action = load_action(
            args.action_file
        )

    else:
        raise ValueError(
            "Use --action-file or --demo."
        )

    # Menentukan folder hasil.
    output_dir = (
        DEFAULT_RESULTS_DIR
        if args.output_dir is None
        else Path(args.output_dir)
    )

    if not output_dir.is_absolute():
        output_dir = BASE_DIR / output_dir

    # Membuat seluruh hasil visualisasi.
    save_action_visualizations(
        action=action,
        output_dir=output_dir,
    )

    print("Visualization results saved to:", output_dir)


if __name__ == "__main__":
    main()
