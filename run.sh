#!/bin/bash

# Function to check if ffmpeg is installed
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo "ffmpeg could not be found"
        install_ffmpeg
    else
        echo "ffmpeg is installed"
    fi
}

# Function to install ffmpeg
install_ffmpeg() {
    echo "Installing ffmpeg..."
    # This is an example for a Debian-based system:
    sudo apt-get update
    sudo apt-get install -y ffmpeg
}

# Function to check if the .venv directory exists and install dependencies
setup_virtualenv() {
    if [ ! -d ".venv" ]; then
        echo "Virtual environment not found. Setting up the environment..."
        pdm install
    else
        echo "Virtual environment found."
    fi
}

# Function to activate virtual environment
activate_virtualenv() {
    echo "Activating the virtual environment..."
    source .venv/bin/activate
}

# Check if ffmpeg is installed
check_ffmpeg

# Check if the virtual environment exists and set it up if it doesn't
setup_virtualenv

# Activate virtual environment
activate_virtualenv

# Run uvicorn server
echo "Starting uvicorn server..."
uvicorn main:app --reload
