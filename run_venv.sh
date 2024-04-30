#!/bin/bash

# Set up a virtual environment directory
VENV_DIR="venv"

# Create a virtual environment
python3 -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Check if requirements.txt exists and install the required Python packages
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt does not exist."
fi

# Inform the user that the script is done
echo "Virtual environment set up and packages installed."
