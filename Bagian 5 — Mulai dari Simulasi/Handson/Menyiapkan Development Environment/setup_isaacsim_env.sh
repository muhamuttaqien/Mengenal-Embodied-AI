#!/usr/bin/env bash
# Stop the script immediately if one command fails.
set -e

# Define the name of the Isaac Sim virtual environment.
ENV_NAME="isaacsim-env"

# Allow the Python executable to be overridden from the shell.
PYTHON_BIN="${PYTHON_BIN:-python3.12}"

# Check whether the requested Python executable exists.
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    # Explain the problem if Python 3.12 is unavailable.
    echo "ERROR: $PYTHON_BIN was not found."

    # Show one way to override the executable.
    echo "Example: PYTHON_BIN=/path/to/python3.12 bash setup_isaacsim_env.sh"

    # Exit with an error status.
    exit 1
fi

# Create the dedicated Isaac Sim virtual environment.
"$PYTHON_BIN" -m venv "$ENV_NAME"

# Activate the Isaac Sim environment.
source "$ENV_NAME/bin/activate"

# Upgrade pip inside the environment.
python -m pip install --upgrade pip

# Install Isaac Sim and extension caches from NVIDIA PyPI.
pip install "isaacsim[all,extscache]" --extra-index-url https://pypi.nvidia.com

# Print a blank line for readability.
echo

# Confirm successful setup.
echo "Isaac Sim environment is ready."

# Show how to activate the environment later.
echo "Activate with: source $ENV_NAME/bin/activate"

# Show the command used to start Isaac Sim.
echo "Launch with: isaacsim"
