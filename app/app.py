import os
import time
import pandas as pd
from flask import Flask, render_template, jsonify
from src.cleaner import CleanedDF
from src.pikl_maker import IsolationForestModel

app = Flask(__name__)

MODEL_PATH = "models/isolation_forest.pkl"
DATA_DIR = "data"
PROCESSED_FILES = set()  # Keep track of processed files

# Load the model once
model = IsolationForestModel(MODEL_PATH)
model.load_model()  # Load the trained model
"""
def process_file(filepath):
    #Process a single CSV log file.
    try:
        data = CleanedDF(filepath)
        data.preprocess()
        predictions, anomaly_scores = model.predict(data.df)
        data.df["Anomaly"] = predictions
        anomalies = data.df[data.df["Anomaly"] == -1]
        anomalies["Exe"] = data.df.loc[anomalies.index, "OriginalExe"]
        return anomalies.to_dict(orient="records")  # Return anomalies as a list of dicts
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []
"""
def process_file(filepath):
    """Process a single CSV log file."""
    try:
        # Load and clean the data
        data = CleanedDF(filepath)

        # Store the original columns before preprocessing
        original_data = data.df[['EventTime', 'EventID', 'Severity', 'AccountName', 'IpAddress', 'Message']].copy()

        # Preprocess the data (this will modify the dataframe)
        data.preprocess()

        # Perform anomaly prediction
        predictions, anomaly_scores = model.predict(data.df)
        data.df["Anomaly"] = predictions
        anomalies = data.df[data.df["Anomaly"] == -1]

        # Add the original data back to the anomalies dataframe
        anomalies["EventTime"] = original_data.loc[anomalies.index, "EventTime"]
        anomalies["EventID"] = original_data.loc[anomalies.index, "EventID"]
        anomalies["Severity"] = original_data.loc[anomalies.index, "Severity"]
        anomalies["AccountName"] = original_data.loc[anomalies.index, "AccountName"]
        anomalies["IpAddress"] = original_data.loc[anomalies.index, "IpAddress"]
        anomalies["Message"] = original_data.loc[anomalies.index, "Message"]

        # Return the anomalies with the original fields
        return anomalies[['EventTime', 'EventID', 'Severity', 'AccountName', 'IpAddress', 'Message']].to_dict(orient="records")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []


def get_new_files():
    """Find new CSV files in the data directory."""
    files = set(f for f in os.listdir(DATA_DIR) if f.endswith(".csv"))
    new_files = files - PROCESSED_FILES
    return [os.path.join(DATA_DIR, f) for f in new_files]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_anomalies")
def get_anomalies():
    """Endpoint to fetch anomalies from new files."""
    new_files = get_new_files()
    all_anomalies = []
    for filepath in new_files:
        anomalies = process_file(filepath)
        all_anomalies.extend(anomalies)
        PROCESSED_FILES.add(os.path.basename(filepath))  # Mark as processed
    return jsonify(all_anomalies)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
