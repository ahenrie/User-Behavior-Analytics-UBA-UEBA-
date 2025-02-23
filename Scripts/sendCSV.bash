#!/bin/bash

LOG_FILE="/var/log/10.10.10.log"
OUTPUT_DIR="~/CSVs/"
REMOTE_USER="based"
REMOTE_HOST="10.10.10.70"
REMOTE_DIR="~/ML"

# Monitor the log file for new entries (write events)
inotifywait -m -e modify "$LOG_FILE" | while read path _ file; do
    echo "New data detected in $LOG_FILE. Processing..."

    # Run Go parser to process the logs and create a CSV
    go run log_parser.go "$LOG_FILE" "$OUTPUT_DIR/new_logs.csv"

    # Transfer the CSV to the Linux machine
    scp "$OUTPUT_DIR/new_logs.csv" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"

    echo "Logs processed and transferred successfully."

done
