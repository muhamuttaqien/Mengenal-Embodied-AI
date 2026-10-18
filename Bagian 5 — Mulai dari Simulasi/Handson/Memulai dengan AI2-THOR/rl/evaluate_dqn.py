# Import argparse for evaluation options.
import argparse

# Import csv for the evaluation log.
import csv

# Import Path for output files.
from pathlib import Path

# Import imageio for optional MP4 recording.
import imageio.v2 as imageio

# Import NumPy for metric aggregation.
import numpy as np

# Import PyTorch.
import torch

# Import the AI2-THOR RL environment.
from rl.ai2thor_nav_env import AI2THORNavigationEnv

# Import the DQN architecture.
from rl.dqn_model import DQN

# Import greedy action selection.
from rl.training_utils import select_action


# Create the command-line parser.
parser = argparse.ArgumentParser(
    description="Evaluate a trained AI2-THOR DQN policy."
)

# Add the checkpoint path.
parser.add_argument(
    "--checkpoint",
    default="checkpoints/dqn_final.pt",
)

# Add the number of evaluation episodes.
parser.add_argument(
    "--episodes",
    type=int,
    default=20,
)

# Add the maximum episode length.
parser.add_argument(
    "--max-steps",
    type=int,
    default=150,
)

# Add an optional video flag.
parser.add_argument(
    "--record-video",
    action="store_true",
)

# Disable randomized starts when requested.
parser.add_argument(
    "--no-random-start",
    action="store_true",
)

# Parse arguments.
args = parser.parse_args()

# Select the evaluation device.
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

# Load the checkpoint.
checkpoint = torch.load(
    args.checkpoint,
    map_location=device,
)

# Read scene information saved during training.
scene = checkpoint.get(
    "scene",
    "FloorPlan1",
)

# Read the target category saved during training.
target_object_type = checkpoint.get(
    "target_object_type",
    "Fridge",
)

# Read the action count.
num_actions = int(
    checkpoint.get(
        "num_actions",
        3,
    )
)

# Construct the DQN model.
model = DQN(
    num_actions=num_actions
).to(device)

# Load learned weights.
model.load_state_dict(
    checkpoint["model_state_dict"]
)

# Switch to evaluation mode.
model.eval()

# Construct the AI2-THOR environment.
env = AI2THORNavigationEnv(
    scene=scene,
    target_object_type=target_object_type,
    max_steps=args.max_steps,
    random_start=not args.no_random_start,
    seed=1000,
)

# Ensure the output folder exists.
Path("results").mkdir(
    parents=True,
    exist_ok=True,
)

# Define the evaluation CSV path.
log_path = Path(
    "results/evaluation_log.csv"
)

# Create lists for summary metrics.
episode_rewards = []

# Create a list for success flags.
episode_successes = []

# Create a list for episode lengths.
episode_lengths = []

# Open the CSV log file.
with log_path.open(
    "w",
    newline="",
    encoding="utf-8",
) as log_file:

    # Create the CSV writer.
    writer = csv.writer(
        log_file
    )

    # Write the evaluation header.
    writer.writerow(
        [
            "episode",
            "reward",
            "steps",
            "success",
        ]
    )

    # Make sure the simulator closes after evaluation.
    try:
        # Iterate through evaluation episodes.
        for episode in range(args.episodes):
            # Reset the environment.
            state = env.reset()

            # Reset the episode reward.
            total_reward = 0.0

            # Reset success.
            success = False

            # Create the video frame list only for episode zero.
            video_frames = (
                [env.rgb_frame()]
                if args.record_video and episode == 0
                else None
            )

            # Run one greedy episode.
            for step in range(1, args.max_steps + 1):
                # Select the greedy action by using epsilon zero.
                action = select_action(
                    model=model,
                    state=state,
                    epsilon=0.0,
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

                # Update episode reward.
                total_reward += reward

                # Move to the next state.
                state = next_state

                # Save the rendered frame when recording video.
                if video_frames is not None:
                    # Append the current RGB frame.
                    video_frames.append(
                        env.rgb_frame()
                    )

                # Read the success flag.
                success = bool(
                    info["success"]
                )

                # Stop at episode termination.
                if done:
                    # Exit the timestep loop.
                    break

            # Save the first evaluation episode as MP4 when requested.
            if video_frames is not None:
                # Define the output video path.
                video_path = Path(
                    "results/evaluation_episode_000.mp4"
                )

                # Encode the frames at six frames per second.
                imageio.mimsave(
                    video_path,
                    video_frames,
                    fps=6,
                )

                # Print the video path.
                print("Saved:", video_path)

            # Store reward for summary metrics.
            episode_rewards.append(
                total_reward
            )

            # Store success as an integer.
            episode_successes.append(
                int(success)
            )

            # Store episode length.
            episode_lengths.append(
                step
            )

            # Write the episode result.
            writer.writerow(
                [
                    episode,
                    total_reward,
                    step,
                    int(success),
                ]
            )

            # Print the episode result.
            print(
                f"Episode {episode:03d} | "
                f"reward={total_reward:8.3f} | "
                f"steps={step:3d} | "
                f"success={int(success)}"
            )

    # Always close AI2-THOR.
    finally:
        # Stop the Unity process.
        env.close()

# Compute the average reward.
average_reward = float(
    np.mean(episode_rewards)
)

# Compute success rate.
success_rate = float(
    np.mean(episode_successes)
)

# Compute mean episode length.
average_length = float(
    np.mean(episode_lengths)
)

# Print a summary header.
print("\nEvaluation Summary")

# Print the average reward.
print("Average reward :", average_reward)

# Print success rate.
print("Success rate   :", success_rate)

# Print average episode length.
print("Average length :", average_length)

# Print the log path.
print("Saved          :", log_path)
