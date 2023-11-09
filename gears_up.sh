#!/bin/bash

# This script get everything ready for the running envirnment.

# Step-1: Activate virtual environment.
if [ ! -d "blossom_venv" ]; then
	# Create the virtual environment
	echo "Creating virtual environment..."
	python -m venv blossom_venv
	echo "Virtual environment created."
fi

echo "Activating the virtual environment..."
source ./blossom_venv/bin/activate
echo "Virtual environment activating done."
