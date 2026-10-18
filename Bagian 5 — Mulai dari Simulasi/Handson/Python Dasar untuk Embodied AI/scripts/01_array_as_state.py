# Import NumPy to work with numerical arrays.
import numpy as np


# Create one observation containing three distance sensor values.
observation = np.array(
    [
        0.4,  # Distance on the LEFT side.
        0.8,  # Distance in FRONT of the robot.
        0.3,  # Distance on the RIGHT side.
    ],
    dtype=np.float32,
)

# Print the complete observation.
print("Observation:", observation)

# Print the array shape.
print("Shape      :", observation.shape)

# Read the first element as the left sensor.
left = observation[0]

# Read the second element as the front sensor.
front = observation[1]

# Read the third element as the right sensor.
right = observation[2]

# Print the left sensor value.
print("Left       :", left)

# Print the front sensor value.
print("Front      :", front)

# Print the right sensor value.
print("Right      :", right)

# Find the index containing the largest distance value.
action_index = int(np.argmax(observation))

# Define readable names for each possible action.
action_names = [
    "LEFT",
    "FORWARD",
    "RIGHT",
]

# Convert the selected index into an action name.
selected_action = action_names[action_index]

# Print the selected action index.
print("Action ID  :", action_index)

# Print the selected action name.
print("Action     :", selected_action)
