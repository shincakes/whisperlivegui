#!/bin/bash

# Absolute path to your virtual environment and project directory
PROJECT_DIR="/home/admin/Desktop/whisperapp/WhisperLive"  # Change this if different
VENV_PATH="/home/admin/Desktop/whisperapp/venvs/whisper2" # Change this if different
CLIENT_SCRIPT_PATH="/home/admin/Desktop/whisperapp/client.py"

# Start run_server.py in a new terminal
lxterminal --working-directory="$PROJECT_DIR" --command="bash -c 'source $VENV_PATH/bin/activate; python3 run_server.py --port 9090 --backend faster_whisper; exec bash'" &

# Wait a few seconds to ensure server starts
sleep 10

# # Start client.py in a new terminal
# lxterminal --command="bash -c 'source $VENV_PATH/bin/activate; python3 $CLIENT_SCRIPT_PATH; exec bash'" &
