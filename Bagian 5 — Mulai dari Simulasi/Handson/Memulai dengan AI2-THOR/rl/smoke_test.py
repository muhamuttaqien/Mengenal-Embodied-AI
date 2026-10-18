# Import Path for the temporary checkpoint.
from pathlib import Path

# Import NumPy for synthetic image states.
import numpy as np

# Import PyTorch.
import torch

# Import the DQN network.
from rl.dqn_model import DQN

# Import replay memory.
from rl.replay_buffer import ReplayBuffer

# Import one optimization helper.
from rl.training_utils import optimize_dqn


# Use the CPU so the smoke test works on any machine.
device = torch.device(
    "cpu"
)

# Fix NumPy randomness.
rng = np.random.default_rng(
    123
)

# Create the online network.
policy_net = DQN(
    num_actions=3
).to(device)

# Create the target network.
target_net = DQN(
    num_actions=3
).to(device)

# Copy online weights into the target network.
target_net.load_state_dict(
    policy_net.state_dict()
)

# Create the optimizer.
optimizer = torch.optim.Adam(
    policy_net.parameters(),
    lr=1e-4,
)

# Create replay memory.
buffer = ReplayBuffer(
    capacity=128,
    seed=123,
)

# Fill the buffer with synthetic transitions.
for index in range(64):
    # Create one random uint8 RGB state.
    state = rng.integers(
        0,
        256,
        size=(3, 84, 84),
        dtype=np.uint8,
    )

    # Create one random next state.
    next_state = rng.integers(
        0,
        256,
        size=(3, 84, 84),
        dtype=np.uint8,
    )

    # Cycle through the three valid actions.
    action = index % 3

    # Create a small deterministic reward.
    reward = float(
        (index % 7) - 3
    ) / 10.0

    # Mark occasional transitions terminal.
    done = bool(
        index % 13 == 0
    )

    # Add the transition.
    buffer.add(
        state,
        action,
        reward,
        next_state,
        done,
    )

# Create one normalized dummy image batch.
dummy = torch.zeros(
    2,
    3,
    84,
    84,
    dtype=torch.float32,
    device=device,
)

# Run a forward pass.
q_values = policy_net(
    dummy
)

# Assert the expected batch-by-action output shape.
assert q_values.shape == (
    2,
    3,
)

# Run one real DQN optimization step.
loss = optimize_dqn(
    policy_net=policy_net,
    target_net=target_net,
    optimizer=optimizer,
    replay_buffer=buffer,
    batch_size=16,
    gamma=0.99,
    device=device,
)

# Make sure the loss is finite.
assert np.isfinite(
    loss
)

# Ensure the checkpoint directory exists.
Path("checkpoints").mkdir(
    parents=True,
    exist_ok=True,
)

# Define a temporary smoke-test checkpoint.
checkpoint_path = Path(
    "checkpoints/smoke_test.pt"
)

# Save the network state.
torch.save(
    {
        "model_state_dict":
            policy_net.state_dict(),
        "num_actions":
            3,
    },
    checkpoint_path,
)

# Create a new model instance.
reloaded = DQN(
    num_actions=3
).to(device)

# Load the checkpoint.
checkpoint = torch.load(
    checkpoint_path,
    map_location=device,
)

# Restore model weights.
reloaded.load_state_dict(
    checkpoint["model_state_dict"]
)

# Run a forward pass after reload.
reloaded_q = reloaded(
    dummy
)

# Verify that checkpoint reload preserves the same predictions.
assert torch.allclose(
    policy_net(dummy),
    reloaded_q,
    atol=1e-6,
)

# Print the successful forward shape.
print(
    "Q-value shape:",
    tuple(q_values.shape),
)

# Print the optimization loss.
print(
    "Optimization loss:",
    f"{loss:.6f}",
)

# Print replay-buffer size.
print(
    "Replay size:",
    len(buffer),
)

# Print final status.
print(
    "SMOKE TEST PASSED"
)
