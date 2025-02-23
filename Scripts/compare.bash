#!/bin/bash

ML_DIR="~/ML"  # Directory where new CSVs are stored
MODEL_FILE="~/ML/random_forest_model.pkl"  # Path to the pkl file
FLASK_SCRIPT="run_flask_app.py"  # Python script to load the model and make predictions

# Monitor the directory for new CSV files
inotifywait -m -e create "$ML_DIR" | while read path _ file; do
    # Check if the file has a .csv extension
    if [[ "$file" == *.csv ]]; then
        echo "New CSV file detected: $file. Running model comparison..."

        # Run Python script to load the CSV, load the model, and compare
        python3 "$FLASK_SCRIPT" --csv "$ML_DIR/$file" --model "$MODEL_FILE"

        echo "Model comparison complete."
    fi
done
