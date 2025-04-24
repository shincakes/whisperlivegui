#!/bin/bash
cd /home/admin/Desktop/whisperapp || exit
source venvs/whisper2/bin/activate

# Run whisper.py and keep terminal open afterward
python whisper.py
echo ""
echo "=== Whisper stopped or crashed ==="
echo "Press Enter to close..."
read
