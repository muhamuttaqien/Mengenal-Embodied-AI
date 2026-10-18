# Import NumPy to create the original observation array.
import numpy as np

# Import PyTorch to work with tensors.
import torch


# Create one observation as a NumPy array.
observation = np.array(
    [
        0.4,
        0.8,
        0.3,
    ],
    dtype=np.float32,
)

# Print the original NumPy array.
print("NumPy observation:", observation)

# Convert the NumPy array into a PyTorch tensor.
observation_tensor = torch.tensor(
    observation,
    dtype=torch.float32,
)

# Print the tensor.
print("Tensor           :", observation_tensor)

# Print the tensor shape.
print("Tensor shape     :", observation_tensor.shape)

# Print the tensor data type.
print("Tensor dtype     :", observation_tensor.dtype)

# Select CUDA when available, otherwise use the CPU.
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

# Print the selected device.
print("Selected device  :", device)

# Move the tensor to the selected device.
observation_tensor = observation_tensor.to(device)

# Print the device currently holding the tensor.
print("Tensor device    :", observation_tensor.device)

# Add a batch dimension at index zero.
batched_tensor = observation_tensor.unsqueeze(0)

# Print the new tensor shape.
print("Batched shape    :", batched_tensor.shape)
