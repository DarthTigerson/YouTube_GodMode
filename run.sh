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
    sudo apt-get update
    sudo apt-get install -y ffmpeg
}

# Check if ffmpeg is installed
check_ffmpeg

# Run uvicorn server
echo "Starting uvicorn server..."
uvicorn main:app --reload
