# Import PyTorch.
import torch

# Import the neural-network module.
import torch.nn as nn


# Define a CNN-based Deep Q-Network.
class DQN(nn.Module):

    # Initialize the network.
    def __init__(
        self,
        num_actions,
        input_channels=3,
        image_size=84,
    ):
        # Initialize the parent nn.Module.
        super().__init__()

        # Build the convolutional visual encoder.
        self.encoder = nn.Sequential(
            # First convolution maps RGB channels to 32 features.
            nn.Conv2d(
                input_channels,
                32,
                kernel_size=8,
                stride=4,
            ),

            # Apply a nonlinear activation.
            nn.ReLU(),

            # Second convolution expands to 64 channels.
            nn.Conv2d(
                32,
                64,
                kernel_size=4,
                stride=2,
            ),

            # Apply another nonlinear activation.
            nn.ReLU(),

            # Third convolution keeps 64 channels.
            nn.Conv2d(
                64,
                64,
                kernel_size=3,
                stride=1,
            ),

            # Apply the final encoder activation.
            nn.ReLU(),
        )

        # Create one dummy image to infer the encoder output size.
        dummy = torch.zeros(
            1,
            input_channels,
            image_size,
            image_size,
        )

        # Disable gradient tracking for shape inference.
        with torch.no_grad():
            # Run the dummy image through the CNN.
            encoded = self.encoder(dummy)

        # Compute the flattened feature dimension.
        feature_dim = int(
            encoded.reshape(1, -1).shape[1]
        )

        # Build the Q-value prediction head.
        self.head = nn.Sequential(
            # Flatten convolutional feature maps.
            nn.Flatten(),

            # Project visual features into a 512-D hidden representation.
            nn.Linear(
                feature_dim,
                512,
            ),

            # Apply a nonlinear activation.
            nn.ReLU(),

            # Predict one Q-value for each discrete action.
            nn.Linear(
                512,
                num_actions,
            ),
        )

    # Define the forward pass.
    def forward(self, x):
        # Encode the RGB observation.
        features = self.encoder(x)

        # Convert visual features into action Q-values.
        q_values = self.head(features)

        # Return one Q-value per action.
        return q_values
