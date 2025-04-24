#!/bin/bash
cd /home/admin/Desktop/whisperapp || exit
source venvs/whisper2/bin/activate

# Log startup for debugging
echo "[$(date)] Starting WhisperApp" >> /home/admin/whisper_boot.log

# Launch scripts and log output
./start.sh >> start.log 2>&1 &
sleep 10
./web_ui.sh >> webui.log 2>&1 & 
sleep 5
./browser_start.sh >> browser.log 2>&1 
