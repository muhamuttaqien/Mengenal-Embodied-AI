#!/usr/bin/env bash
# Stop the script immediately if one command fails.
set -e

# Define the name of the main virtual environment.
ENV_NAME="embodied-ai-env"

# Create the virtual environment using Python 3.
python3 -m venv "$ENV_NAME"

# Activate the newly created virtual environment.
source "$ENV_NAME/bin/activate"

# Upgrade pip inside the virtual environment.
python -m pip install --upgrade pip

# Install the packages listed in requirements-main.txt.
pip install -r requirements-main.txt

# Print a blank line for readability.
echo

# Tell the user that installation finished.
echo "Main environment is ready."

# Show how to activate the environment later.
echo "Activate with: source $ENV_NAME/bin/activate"
