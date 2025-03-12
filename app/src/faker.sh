#!/bin/bash

# Define paths
SRC_DIR="$(dirname "$(realpath "$0")")"  # Get the directory of this script
DATA_DIR="$(realpath "$SRC_DIR/../data")"  # Navigate to the sibling 'data' directory
PYTHON_SCRIPT="$SRC_DIR/badLogFaker.py"  # Path to Python script
LOG_FILE="badLogs.csv"  # Name of the output file from the Python script

# Ensure the data directory exists
mkdir -p "$DATA_DIR"

echo "Starting badLogFaker.py loop... Press Ctrl+C to stop."

while true; do
    TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")  # Format: YYYY-MM-DD_HH-MM-SS
    OUTPUT_FILE="$DATA_DIR/log_$TIMESTAMP.csv"

    echo "Generating log: $OUTPUT_FILE"

    # Run the Python script
    python3 "$PYTHON_SCRIPT"

    # Move the generated log file to the data directory with a timestamped name
    if [ -f "$SRC_DIR/$LOG_FILE" ]; then
        mv "$SRC_DIR/$LOG_FILE" "$OUTPUT_FILE"
    else
        echo "Warning: $LOG_FILE not found! Skipping..."
    fi

    # Wait for 2 seconds before running again
    sleep 10
done
