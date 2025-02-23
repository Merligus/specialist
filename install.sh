#!/bin/bash

# Path to the conda executable
CONDA_PATH=$(which conda)

# Check if conda is installed
if [ -z "$CONDA_PATH" ]; then
    echo "Conda could not be found. Please install conda first."
    exit
fi

# Initialize conda
eval "$($CONDA_PATH shell.bash hook)"

# List of conda environments to activate
ENVIRONMENTS=("specialist:3.11")

# Loop through each environment and activate it
for ENV_NAME_VERSION in "${ENVIRONMENTS[@]}"; do
    # get environment name and python version
    IFS=':' read -r ENV_NAME PYTHON_VERSION <<< "$ENV_NAME_VERSION"

    if { conda env list | grep $ENV_NAME; } >/dev/null 2>&1; then
        echo "$ENV_NAME already exists."
    else
        # Create the conda environment
        echo "Creating conda environment: $ENV_NAME with Python version: $PYTHON_VERSION"
        conda create -n $ENV_NAME python=$PYTHON_VERSION -y
    fi
    # Activate the conda environment
    echo "Activating conda environment..."
    conda activate $ENV_NAME

    # Install the requirements from requirements.txt
    if [ -f requirements.txt ]; then
        echo "Installing requirements from requirements.txt..."
        pip install -r requirements.txt
    else
        echo "requirements.txt file not found. Please provide the file."
        exit
    fi

    echo "Conda environment '$ENV_NAME' is ready."

    echo "Deactivating conda environment..."
    conda deactivate
    cd ..
done

echo "Installation complete."
