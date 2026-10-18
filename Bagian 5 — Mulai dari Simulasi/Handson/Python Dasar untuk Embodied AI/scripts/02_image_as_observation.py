# Import Path to work with file paths.
from pathlib import Path

# Import NumPy to convert an image into a numerical array.
import numpy as np

# Import Pillow's Image module to load and save images.
from PIL import Image


# Define the input image path.
IMAGE_PATH = Path("assets/scene.jpg")

# Define the output directory.
RESULT_DIR = Path("results")

# Create the results directory if it does not already exist.
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# Open the image and force it to use RGB format.
image = Image.open(IMAGE_PATH).convert("RGB")

# Convert the image into a NumPy array.
image_array = np.array(image)

# Read the image height from the array shape.
height = image_array.shape[0]

# Read the image width from the array shape.
width = image_array.shape[1]

# Read the number of color channels from the array shape.
channels = image_array.shape[2]

# Print the full image shape.
print("Image shape :", image_array.shape)

# Print the height.
print("Height      :", height)

# Print the width.
print("Width       :", width)

# Print the number of channels.
print("Channels    :", channels)

# Read the RGB value of the center pixel.
center_pixel = image_array[
    height // 2,
    width // 2,
]

# Print the center pixel value.
print("Center pixel:", center_pixel)

# Define a path for the copied image.
output_path = RESULT_DIR / "image_observation_copy.png"

# Convert the array back into an image and save it.
Image.fromarray(image_array).save(output_path)

# Print the output path.
print("Saved       :", output_path)
