# Import time so the viewer loop can run at a human-readable speed.
import time

# Import MuJoCo's Python API.
import mujoco

# Import the built-in MuJoCo viewer.
import mujoco.viewer


# Store a minimal MuJoCo model as an XML string.
MODEL_XML = """
<mujoco model="first_mujoco">
    <option timestep="0.01"/>
    <worldbody>
        <geom name="floor"
              type="plane"
              size="2 2 0.1"/>
        <body name="pendulum"
              pos="0 0 1">
            <joint name="hinge"
                   type="hinge"
                   axis="0 1 0"/>
            <geom name="link"
                  type="capsule"
                  fromto="0 0 0 0 0 -0.6"
                  size="0.06"
                  mass="1"/>
        </body>
    </worldbody>
    <actuator>
        <motor name="hinge_motor"
               joint="hinge"
               gear="1"/>
    </actuator>
</mujoco>
"""

# Compile the XML description into an MuJoCo model.
model = mujoco.MjModel.from_xml_string(MODEL_XML)

# Create the runtime state associated with the model.
data = mujoco.MjData(model)

# Print the MuJoCo version to confirm the package is loaded.
print("MuJoCo version:", mujoco.__version__)

# Print the initial joint position.
print("Initial qpos  :", data.qpos.copy())

# Launch a viewer that stays synchronized with the Python simulation loop.
with mujoco.viewer.launch_passive(model, data) as viewer:
    # Keep stepping while the viewer window remains open.
    while viewer.is_running() and data.time < 5.0:
        # Apply a positive motor command during the first half of the demo.
        if data.time < 2.5:
            # Write the motor command into the first actuator control slot.
            data.ctrl[0] = 0.5
        # Switch the motor direction during the second half of the demo.
        else:
            # Write a negative motor command into the actuator control slot.
            data.ctrl[0] = -0.5

        # Advance the MuJoCo physics simulation by one timestep.
        mujoco.mj_step(model, data)

        # Synchronize the graphical viewer with the new simulation state.
        viewer.sync()

        # Sleep briefly so the simulation is easier to observe visually.
        time.sleep(model.opt.timestep)

# Print the final simulated time after the viewer loop ends.
print("Final time    :", data.time)

# Print the final joint position.
print("Final qpos    :", data.qpos.copy())

# Print the final joint velocity.
print("Final qvel    :", data.qvel.copy())
