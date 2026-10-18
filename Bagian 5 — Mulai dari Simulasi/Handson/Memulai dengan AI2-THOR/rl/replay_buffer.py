# Import random for uniform transition sampling.
import random

# Import deque for a bounded replay memory.
from collections import deque

# Import NumPy for stacking batches.
import numpy as np

# Import PyTorch for tensor conversion.
import torch


# Implement a simple DQN replay buffer.
class ReplayBuffer:

    # Initialize the replay buffer.
    def __init__(
        self,
        capacity=50000,
        seed=42,
    ):
        # Store transitions in a bounded deque.
        self.buffer = deque(
            maxlen=capacity
        )

        # Create a reproducible sampler.
        self.rng = random.Random(seed)

    # Return the current number of stored transitions.
    def __len__(self):
        # Return the deque length.
        return len(self.buffer)

    # Add one transition.
    def add(
        self,
        state,
        action,
        reward,
        next_state,
        done,
    ):
        # Store states as uint8 to reduce memory use.
        state_uint8 = np.asarray(
            state,
            dtype=np.uint8,
        ).copy()

        # Store next states as uint8 as well.
        next_state_uint8 = np.asarray(
            next_state,
            dtype=np.uint8,
        ).copy()

        # Append the complete transition.
        self.buffer.append(
            (
                state_uint8,
                int(action),
                float(reward),
                next_state_uint8,
                bool(done),
            )
        )

    # Sample one mini-batch.
    def sample(
        self,
        batch_size,
        device,
    ):
        # Draw transitions uniformly without replacement.
        batch = self.rng.sample(
            self.buffer,
            batch_size,
        )

        # Unpack transition tuples.
        states, actions, rewards, next_states, dones = zip(
            *batch
        )

        # Stack and normalize image states into [0,1].
        states = torch.from_numpy(
            np.stack(states)
        ).float().to(device) / 255.0

        # Convert actions into int64 indices.
        actions = torch.tensor(
            actions,
            dtype=torch.long,
            device=device,
        ).unsqueeze(1)

        # Convert rewards into float tensors.
        rewards = torch.tensor(
            rewards,
            dtype=torch.float32,
            device=device,
        ).unsqueeze(1)

        # Stack and normalize next image states.
        next_states = torch.from_numpy(
            np.stack(next_states)
        ).float().to(device) / 255.0

        # Convert done flags into float masks.
        dones = torch.tensor(
            dones,
            dtype=torch.float32,
            device=device,
        ).unsqueeze(1)

        # Return the training batch.
        return (
            states,
            actions,
            rewards,
            next_states,
            dones,
        )
