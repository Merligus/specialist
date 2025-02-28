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

conda activate specialist
# python Chroma.py
python LangChain.py
conda deactivate
echo "Completed."