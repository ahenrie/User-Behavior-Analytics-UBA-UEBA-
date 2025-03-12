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

def process_file(filepath):
    """Process a single CSV log file."""
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
    app.run(port=8080,debug=True)
