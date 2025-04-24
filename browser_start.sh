#!/bin/bash
lxterminal -e "/home/admin/Desktop/whisperapp/web_ui.sh" &

# Wait for server to start, then open GUI
sleep 10
chromium-browser --kiosk http://localhost:7860