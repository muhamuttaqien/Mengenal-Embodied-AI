# Import argparse for training options.
import argparse

# Import csv for training logs.
import csv

# Import random for reproducibility.
import random

# Import Path for output directories.
from pathlib import Path

# Import NumPy.
import numpy as np

# Import PyTorch.
import torch

# Import the AI2-THOR RL wrapper.
from rl.ai2thor_nav_env import AI2THORNavigationEnv

# Import the DQN model.
from rl.dqn_model import DQN

# Import the replay buffer.
from rl.replay_buffer import ReplayBuffer

# Import DQN helper functions.
from rl.training_utils import (
    epsilon_by_step,
    optimize_dqn,
    select_action,
)


# Create command-line options.
parser = argparse.ArgumentParser(
    description="Train CNN + DQN navigation in AI2-THOR."
)

# Add the AI2-THOR scene.
parser.add_argument(
    "--scene",
    default="FloorPlan3",
)

# Add the fixed semantic target object.
parser.add_argument(
    "--target-object-type",
    default="Fridge",
)

# Add the number of training episodes.
parser.add_argument(
    "--episodes",
    type=int,
    default=500,
)

# Add the episode step limit.
parser.add_argument(
    "--max-steps",
    type=int,
    default=150,
)

# Add the replay-buffer capacity.
parser.add_argument(
    "--buffer-size",
    type=int,
    default=50000,
)

# Add the mini-batch size.
parser.add_argument(
    "--batch-size",
    type=int,
    default=32,
)

# Add the discount factor.
parser.add_argument(
    "--gamma",
    type=float,
    default=0.99,
)

# Add the Adam learning rate.
parser.add_argument(
    "--lr",
    type=float,
    default=1e-4,
)

# Add the number of transitions collected before learning starts.
parser.add_argument(
    "--learning-starts",
    type=int,
    default=1000,
)

# Add the target-network copy interval.
parser.add_argument(
    "--target-update-steps",
    type=int,
    default=1000,
)

# Add the epsilon-decay duration.
parser.add_argument(
    "--epsilon-decay-steps",
    type=int,
    default=30000,
)

# Add the random seed.
parser.add_argument(
    "--seed",
    type=int,
    default=42,
)

# Disable random starts when requested.
parser.add_argument(
    "--no-random-start",
    action="store_true",
)

# Parse command-line options.
args = parser.parse_args()

# Seed Python's global random module.
random.seed(args.seed)

# Seed NumPy.
np.random.seed(args.seed)

# Seed PyTorch.
torch.manual_seed(args.seed)

# Select CUDA when it is available.
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

# Print the selected training device.
print("Device:", device)

# Create output directories.
Path("checkpoints").mkdir(
    parents=True,
    exist_ok=True,
)

# Create the results directory.
Path("results").mkdir(
    parents=True,
    exist_ok=True,
)

# Create the AI2-THOR navigation environment.
env = AI2THORNavigationEnv(
    scene=args.scene,
    target_object_type=args.target_object_type,
    max_steps=args.max_steps,
    random_start=not args.no_random_start,
    seed=args.seed,
)

# Create the online policy network.
policy_net = DQN(
    num_actions=env.num_actions
).to(device)

# Create the target network.
target_net = DQN(
    num_actions=env.num_actions
).to(device)

# Copy online-network weights into the target network.
target_net.load_state_dict(
    policy_net.state_dict()
)

# Put the target network in evaluation mode.
target_net.eval()

# Create the Adam optimizer.
optimizer = torch.optim.Adam(
    policy_net.parameters(),
    lr=args.lr,
)

# Create replay memory.
replay_buffer = ReplayBuffer(
    capacity=args.buffer_size,
    seed=args.seed,
)

# Define the training CSV path.
log_path = Path(
    "results/training_log.csv"
)

# Initialize the total environment-step counter.
global_step = 0

# Track the best episode reward for checkpointing.
best_reward = -float("inf")

# Open the CSV training log.
with log_path.open(
    "w",
    newline="",
    encoding="utf-8",
) as log_file:

    # Create the CSV writer.
    writer = csv.writer(
        log_file
    )

    # Write the column header.
    writer.writerow(
        [
            "episode",
            "reward",
            "steps",
            "success",
            "epsilon",
            "mean_loss",
        ]
    )

    # Make sure the environment closes even if training is interrupted.
    try:
        # Iterate through training episodes.
        for episode in range(1, args.episodes + 1):
            # Reset the simulator and read the first RGB state.
            state = env.reset()

            # Reset episode reward.
            episode_reward = 0.0

            # Create an empty list for optimization losses.
            losses = []

            # Initialize episode success.
            success = False

            # Run one episode.
            for episode_step in range(1, args.max_steps + 1):
                # Compute the current epsilon value.
                epsilon = epsilon_by_step(
                    global_step,
                    start=1.0,
                    end=0.05,
                    decay_steps=args.epsilon_decay_steps,
                )

                # Choose one epsilon-greedy action.
                action = select_action(
                    model=policy_net,
                    state=state,
                    epsilon=epsilon,
                    num_actions=env.num_actions,
                    device=device,
                )

                # Execute the selected action.
                (
                    next_state,
                    reward,
                    done,
                    info,
                ) = env.step(
                    action
                )

                # Add the transition to replay memory.
                replay_buffer.add(
                    state=state,
                    action=action,
                    reward=reward,
                    next_state=next_state,
                    done=done,
                )

                # Update total episode reward.
                episode_reward += reward

                # Move to the next observation.
                state = next_state

                # Increase the global step.
                global_step += 1

                # Start optimization after enough transitions are available.
                if (
                    len(replay_buffer) >= args.learning_starts
                    and len(replay_buffer) >= args.batch_size
                ):
                    # Perform one gradient update.
                    loss = optimize_dqn(
                        policy_net=policy_net,
                        target_net=target_net,
                        optimizer=optimizer,
                        replay_buffer=replay_buffer,
                        batch_size=args.batch_size,
                        gamma=args.gamma,
                        device=device,
                    )

                    # Record the current loss.
                    losses.append(loss)

                # Periodically synchronize the target network.
                if (
                    global_step > 0
                    and global_step % args.target_update_steps == 0
                ):
                    # Copy current policy weights.
                    target_net.load_state_dict(
                        policy_net.state_dict()
                    )

                # Read success from the environment info dictionary.
                success = bool(
                    info["success"]
                )

                # End the episode when done.
                if done:
                    # Exit the timestep loop.
                    break

            # Compute mean loss for the completed episode.
            mean_loss = (
                float(np.mean(losses))
                if losses
                else 0.0
            )

            # Write one CSV row.
            writer.writerow(
                [
                    episode,
                    episode_reward,
                    episode_step,
                    int(success),
                    epsilon,
                    mean_loss,
                ]
            )

            # Flush the CSV so progress survives interruptions.
            log_file.flush()

            # Print compact progress.
            print(
                f"Episode {episode:04d} | "
                f"reward={episode_reward:8.3f} | "
                f"steps={episode_step:3d} | "
                f"success={int(success)} | "
                f"epsilon={epsilon:.3f} | "
                f"loss={mean_loss:.5f}"
            )

            # Save a checkpoint when episode reward improves.
            if episode_reward > best_reward:
                # Update the best-reward tracker.
                best_reward = episode_reward

                # Save the current best model.
                torch.save(
                    {
                        "model_state_dict": policy_net.state_dict(),
                        "scene": args.scene,
                        "target_object_type": args.target_object_type,
                        "num_actions": env.num_actions,
                        "image_size": 84,
                        "random_start": not args.no_random_start,
                        "episode": episode,
                        "global_step": global_step,
                        "best_reward": best_reward,
                    },
                    "checkpoints/dqn_best.pt",
                )

    # Always close the simulator.
    finally:
        # Stop AI2-THOR.
        env.close()

# Save the final network after training.
torch.save(
    {
        "model_state_dict": policy_net.state_dict(),
        "scene": args.scene,
        "target_object_type": args.target_object_type,
        "num_actions": 3,
        "image_size": 84,
        "random_start": not args.no_random_start,
        "episode": args.episodes,
        "global_step": global_step,
        "best_reward": best_reward,
    },
    "checkpoints/dqn_final.pt",
)

# Print output locations.
print("Saved:", log_path)

# Print the final checkpoint path.
print("Saved: checkpoints/dqn_final.pt")

# Import the plotting function only after training completes.
from rl.plot_training import plot_training_log

# Create reward and success plots.
plot_training_log(
    log_path
)
