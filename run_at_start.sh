#!/bin/bash

# Delay start for 1 minute
sleep 60

# Activate the Python virtual environment
source ./venv/bin/activate

# Function to keep running a command continuously if it fails
run_forever() {
  local cmd="$1"
  while true; do
    echo "Starting: $cmd"
    eval "$cmd"
    echo "Command failed: $cmd. Restarting in 5 seconds..."
    sleep 5
  done
}

# Run each task in the background with persistent retry
run_forever "python3 ./udp_drones/heartbeat.py" &
run_forever "bash ./udp_drones/start_mavproxy.sh" &
run_forever "bash ./udp_drones/streamvid.sh 100.113.114.176 1" &

# Wait for all background tasks to complete (which they never will, but keeps script alive)
wait
