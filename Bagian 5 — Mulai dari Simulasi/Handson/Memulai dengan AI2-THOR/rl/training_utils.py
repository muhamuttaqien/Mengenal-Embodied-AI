# Import math for epsilon schedules.
import math

# Import random for epsilon-greedy exploration.
import random

# Import PyTorch.
import torch

# Import functional neural-network losses.
import torch.nn.functional as F


# Compute linearly decayed epsilon.
def epsilon_by_step(
    step,
    start=1.0,
    end=0.05,
    decay_steps=30000,
):
    # Clamp progress between zero and one.
    fraction = min(
        1.0,
        float(step) / float(decay_steps),
    )

    # Interpolate from start to end.
    epsilon = (
        start
        + fraction * (end - start)
    )

    # Return the exploration probability.
    return float(epsilon)


# Choose one epsilon-greedy action.
def select_action(
    model,
    state,
    epsilon,
    num_actions,
    device,
):
    # Explore with probability epsilon.
    if random.random() < epsilon:
        # Return a random action index.
        return random.randrange(num_actions)

    # Convert uint8 CHW image into a normalized batch tensor.
    state_tensor = torch.from_numpy(
        state
    ).float().unsqueeze(0).to(device) / 255.0

    # Disable gradient tracking during action selection.
    with torch.no_grad():
        # Predict Q-values for all actions.
        q_values = model(
            state_tensor
        )

    # Return the action with the highest Q-value.
    return int(
        q_values.argmax(
            dim=1
        ).item()
    )


# Perform one standard DQN optimization step.
def optimize_dqn(
    policy_net,
    target_net,
    optimizer,
    replay_buffer,
    batch_size,
    gamma,
    device,
):
    # Sample one replay mini-batch.
    (
        states,
        actions,
        rewards,
        next_states,
        dones,
    ) = replay_buffer.sample(
        batch_size,
        device,
    )

    # Predict Q-values for current states.
    all_q_values = policy_net(
        states
    )

    # Gather Q-values corresponding to executed actions.
    current_q = all_q_values.gather(
        1,
        actions,
    )

    # Disable gradients when constructing Bellman targets.
    with torch.no_grad():
        # Predict target-network Q-values at next states.
        next_q = target_net(
            next_states
        ).max(
            dim=1,
            keepdim=True,
        )[0]

        # Mask bootstrapping when the transition is terminal.
        target_q = rewards + (
            gamma
            * next_q
            * (1.0 - dones)
        )

    # Compute a robust temporal-difference loss.
    loss = F.smooth_l1_loss(
        current_q,
        target_q,
    )

    # Clear gradients from the previous update.
    optimizer.zero_grad()

    # Backpropagate the loss.
    loss.backward()

    # Clip gradients for additional numerical stability.
    torch.nn.utils.clip_grad_norm_(
        policy_net.parameters(),
        max_norm=10.0,
    )

    # Update policy-network weights.
    optimizer.step()

    # Return the scalar loss for logging.
    return float(
        loss.item()
    )
