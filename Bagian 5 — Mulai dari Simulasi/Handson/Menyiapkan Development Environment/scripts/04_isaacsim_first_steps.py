# Import SimulationApp first because it starts the Omniverse runtime.
from isaacsim import SimulationApp


# Launch Isaac Sim with a visible graphical window.
simulation_app = SimulationApp({"headless": False})

# Import NumPy after SimulationApp has initialized the Omniverse runtime.
import numpy as np

# Import stage utilities used to create a new USD stage.
import isaacsim.core.experimental.utils.stage as stage_utils

# Import GroundPlane so the scene contains a visible floor.
from isaacsim.core.experimental.objects import GroundPlane

# Import the simulation manager used to advance physics.
from isaacsim.core.simulation_manager import SimulationManager

# Import the rendering manager used to render each frame.
from isaacsim.core.rendering_manager import RenderingManager


# Create a new empty stage.
stage_utils.create_new_stage()

# Add a ground plane at the origin of the scene.
GroundPlane(
    "/World/GroundPlane",
    positions=np.array([0.0, 0.0, 0.0]),
)

# Print a short message so the user knows that scene creation succeeded.
print("Isaac Sim stage created.")

# Print another message describing the object that was added.
print("Ground plane added at /World/GroundPlane.")

# Run a short simulation/render loop.
for step in range(180):
    # Advance physics by one simulation step.
    SimulationManager.step()

    # Render the current scene.
    RenderingManager.render()

    # Let the Isaac Sim application process one update.
    simulation_app.update()

    # Print progress every 60 steps.
    if step % 60 == 0:
        # Display the current step number.
        print("Simulation step:", step)

# Print a final message before shutting down.
print("First Isaac Sim scene completed.")

# Close Isaac Sim and release the Omniverse runtime.
simulation_app.close()
