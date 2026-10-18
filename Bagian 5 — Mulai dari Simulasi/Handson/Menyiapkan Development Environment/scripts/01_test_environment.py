# Import library standar.
import platform
import sys
from pathlib import Path

# Import library yang akan diperiksa.
import numpy as np
import torch
from PIL import Image
import matplotlib


# Menentukan folder results.
project_dir = Path(__file__).resolve().parent.parent
results_dir = project_dir / "results"

# Membuat folder jika belum ada.
results_dir.mkdir(
    parents=True,
    exist_ok=True,
)

# Menentukan file log.
log_path = (
    results_dir
    / "01_test_environment.log"
)


# Menampilkan output ke terminal dan file.
class Tee:
    def __init__(
        self,
        terminal,
        log_file,
    ):
        self.terminal = terminal
        self.log_file = log_file

    def write(
        self,
        message,
    ):
        self.terminal.write(
            message
        )

        self.log_file.write(
            message
        )

        self.log_file.flush()

    def flush(
        self,
    ):
        self.terminal.flush()
        self.log_file.flush()


# Membuka file log.
with open(
    log_path,
    "w",
    encoding="utf-8",
) as log_file:

    # Menyimpan stdout asli.
    original_stdout = sys.stdout

    # Mengarahkan output ke terminal dan log.
    sys.stdout = Tee(
        original_stdout,
        log_file,
    )

    try:

        # Menampilkan versi Python.
        print(
            "Python         :",
            platform.python_version(),
        )

        # Menampilkan versi NumPy.
        print(
            "NumPy          :",
            np.__version__,
        )

        # Menampilkan versi PyTorch.
        print(
            "PyTorch        :",
            torch.__version__,
        )

        # Menampilkan versi Pillow.
        print(
            "Pillow         :",
            Image.__version__,
        )

        # Menampilkan versi Matplotlib.
        print(
            "Matplotlib     :",
            matplotlib.__version__,
        )

        # Memeriksa CUDA.
        cuda_available = (
            torch.cuda.is_available()
        )

        print(
            "CUDA available :",
            cuda_available,
        )

        # Menampilkan nama GPU.
        if cuda_available:

            print(
                "CUDA device    :",
                torch.cuda.get_device_name(0),
            )


        print(
            "\nEnvironment ready!"
        )

        print(
            "\nLog saved to:",
            log_path,
        )


    finally:

        # Mengembalikan stdout.
        sys.stdout = original_stdout
