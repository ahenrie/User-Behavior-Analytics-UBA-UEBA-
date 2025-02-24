#!/bin/bash

LOG_FILE="/var/log/10.10.10.log"
OUTPUT_DIR="$HOME/CSVs/"
REMOTE_USER="based"
REMOTE_HOST="10.10.10.70"
REMOTE_DIR="$HOME/ML"
LAST_PROCESSED_FILE="$OUTPUT_DIR/last_position"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Initialize the last processed position if not exists
if [ ! -f "$LAST_PROCESSED_FILE" ]; then
    echo 0 > "$LAST_PROCESSED_FILE"
fi

while true; do
    # Read the last processed byte position
    LAST_POS=$(cat "$LAST_PROCESSED_FILE")

    # Get the current file size
    CURRENT_SIZE=$(stat -c%s "$LOG_FILE")

    # If log file size has increased, process new data
    if [ "$CURRENT_SIZE" -gt "$LAST_POS" ]; then
        echo "New log data detected. Processing..."

        # Extract only the new lines from the log file
        tail -c +$((LAST_POS + 1)) "$LOG_FILE" > "$OUTPUT_DIR/new_logs.txt"

        # Run Go parser on the new logs only
        go run log_parser.go "$OUTPUT_DIR/new_logs.txt" "$OUTPUT_DIR/new_logs.csv"

        # Transfer the CSV to the remote Linux machine
        scp "$OUTPUT_DIR/new_logs.csv" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"

        echo "Logs processed and transferred successfully."

        # Update last processed position
        echo "$CURRENT_SIZE" > "$LAST_PROCESSED_FILE"
    fi

    # Wait 10 seconds before checking again
    sleep 10
done
