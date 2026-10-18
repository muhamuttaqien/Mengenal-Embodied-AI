# Import PIL untuk membuka image.
from PIL import Image


def load_image(
    image_path,
):
    # Membuka image dan mengubahnya menjadi RGB.
    return Image.open(
        image_path
    ).convert(
        "RGB"
    )


def build_robot_prompt(
    instruction,
):
    # Membuat prompt multimodal untuk task robot.
    return f"""
You are helping a robot understand a visual scene.

Human instruction:
"{instruction}"

Look at the image and answer these points:
1. Which visible object is the instruction referring to?
2. What visual evidence supports your answer?
3. What simple robot action should be taken next?

Keep the answer concise and practical.
""".strip()
