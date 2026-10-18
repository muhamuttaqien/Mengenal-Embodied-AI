# Import Path to create a platform-independent output directory.
from pathlib import Path

# Import the main AI2-THOR controller.
from ai2thor.controller import Controller

# Import Pillow so RGB frames can be saved as PNG images.
from PIL import Image


# Define the folder used to store generated images.
RESULT_DIR = Path("results")

# Create the results folder if it does not already exist.
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# Create the AI2-THOR controller and open FloorPlan1.
controller = Controller(
    scene="FloorPlan1",
    width=640,
    height=480,
)

# Use try/finally so the simulator is closed even if an error occurs.
try:
    # Read the first event generated after the scene is initialized.
    initial_event = controller.last_event

    # Extract the RGB observation from the initial event.
    initial_frame = initial_event.frame

    # Save the first RGB observation to disk.
    Image.fromarray(initial_frame).save(RESULT_DIR / "ai2thor_before.png")

    # Read the agent position from the event metadata.
    initial_position = initial_event.metadata["agent"]["position"]

    # Print the starting position of the agent.
    print("Initial agent position:", initial_position)

    # Send a MoveAhead action to the agent.
    move_event = controller.step(action="MoveAhead")

    # Print whether the movement action succeeded.
    print("MoveAhead success:", move_event.metadata["lastActionSuccess"])

    # Send a RotateRight action to the agent.
    rotate_event = controller.step(action="RotateRight")

    # Print whether the rotation action succeeded.
    print("RotateRight success:", rotate_event.metadata["lastActionSuccess"])

    # Extract the RGB frame after the two actions.
    final_frame = rotate_event.frame

    # Save the final RGB observation to disk.
    Image.fromarray(final_frame).save(RESULT_DIR / "ai2thor_after.png")

    # Read the final position from the latest metadata.
    final_position = rotate_event.metadata["agent"]["position"]

    # Print the final agent position.
    print("Final agent position  :", final_position)

    # Select only objects currently marked as visible.
    visible_objects = [
        obj
        for obj in rotate_event.metadata["objects"]
        if obj["visible"]
    ]

    # Print the total number of visible objects.
    print("Visible objects       :", len(visible_objects))

    # Iterate over at most the first ten visible objects.
    for obj in visible_objects[:10]:
        # Print the object type and its unique object identifier.
        print("-", obj["objectType"], "|", obj["objectId"])

    # Tell the user where the generated image files were saved.
    print("Saved: results/ai2thor_before.png")

    # Tell the user where the final image file was saved.
    print("Saved: results/ai2thor_after.png")

# Always execute this block when the try section ends.
finally:
    # Stop the AI2-THOR Unity process cleanly.
    controller.stop()
