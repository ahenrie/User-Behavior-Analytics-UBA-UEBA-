import os
import time
import pandas as pd
from flask import Flask, render_template, jsonify
from src.cleaner import CleanedDF
from src.pikl_maker import IsolationForestModel
import plotly.graph_objs as go
import plotly.offline as pyo
import numpy as np
from collections import defaultdict

app = Flask(__name__)
MODEL_PATH = "models/isolation_forest.pkl"
DATA_DIR = "data"
PROCESSED_FILES = set()
ALL_ANOMALIES = pd.DataFrame()

# Load the Isolation Forest model from a pickle file.
model = IsolationForestModel(MODEL_PATH)
model.load_model()

# Function to process a single CSV file for anomaly detection.
def process_file(filepath):
    try:
        # Load and preprocess the data.
        data = CleanedDF(filepath)
        # Store original data for later retrieval of specific columns.
        original_data = data.df[['EventTime', 'EventID', 'Severity', 'AccountName', 'IpAddress', 'Message']].copy()
        data.preprocess()
        # Predict anomalies and get anomaly scores using the loaded model.
        predictions, anomaly_scores = model.predict(data.df)
        data.df["Anomaly"] = predictions
        data.df["AnomalyScore"] = anomaly_scores
        # Filter out anomalies and restore the original columns.
        anomalies = data.df[data.df["Anomaly"] == -1]
        anomalies["EventTime"] = original_data.loc[anomalies.index, "EventTime"]
        anomalies["EventID"] = original_data.loc[anomalies.index, "EventID"]
        anomalies["Severity"] = original_data.loc[anomalies.index, "Severity"]
        anomalies["AccountName"] = original_data.loc[anomalies.index, "AccountName"]
        anomalies["IpAddress"] = original_data.loc[anomalies.index, "IpAddress"]
        anomalies["Message"] = original_data.loc[anomalies.index, "Message"]
        # Return the anomalies and the entire processed data.
        return anomalies[['EventTime', 'EventID', 'Severity', 'AccountName', 'IpAddress', 'Message']], data.df
    except Exception as e:
        # Handle exceptions during file processing.
        print(f"Error processing {filepath}: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Function to get new CSV files in the data directory.
def get_new_files():
    # Get a set of all CSV files in the data directory.
    files = set(f for f in os.listdir(DATA_DIR) if f.endswith(".csv"))
    # Find files that have not been processed yet.
    new_files = files - PROCESSED_FILES
    # Return the full filepaths of the new files.
    return [os.path.join(DATA_DIR, f) for f in new_files]

# Function to generate a scatter plot of anomaly scores.
def generate_scatter_plot(all_data):
    if all_data.empty:
        return None
    # Extract predictions and anomaly scores.
    predictions = all_data["Anomaly"].values
    anomaly_scores = all_data["AnomalyScore"].values
    # Separate normal and anomaly indices.
    normal_indices = np.where(predictions == 1)[0]
    anomaly_indices = np.where(predictions == -1)[0]
    # Create scatter plot traces for normal and anomaly points.
    trace_normal = go.Scatter(
        x=normal_indices,
        y=anomaly_scores[normal_indices],
        mode="markers",
        name="Normal",
        marker=dict(color="blue", size=5)
    )
    trace_anomalies = go.Scatter(
        x=anomaly_indices,
        y=anomaly_scores[anomaly_indices],
        mode="markers",
        name="Anomaly",
        marker=dict(color="red", size=10)
    )
    # Define the layout of the plot.
    layout = go.Layout(
        title="Anomaly Scores Scatter Plot",
        xaxis=dict(title="Data Point Index"),
        yaxis=dict(title="Anomaly Score")
    )
    # Create the figure and generate the plot div.
    fig = go.Figure(data=[trace_normal, trace_anomalies], layout=layout)
    plot_div = pyo.plot(fig, output_type="div")
    return plot_div

# Function to calculate anomaly counts by user.
def get_anomaly_counts_by_user(anomalies):
    df = pd.DataFrame(anomalies)
    if not df.empty:
        # Calculate value counts and rename columns.
        counts = df['AccountName'].value_counts().reset_index()
        counts.columns = ['AccountName', 'AnomalyCount']
        return counts.to_dict(orient='records')
    else:
        return []

# Flask route for the main index page.
@app.route("/")
def index():
    return render_template("index.html")

# Flask route for the users page.
@app.route("/users")
def users():
    return render_template("users.html")

# Flask route to get anomalies grouped by user.
@app.route("/get_anomalies_by_user")
def get_anomalies_by_user():
    # Group anomalies by AccountName.
    grouped_anomalies = defaultdict(list)
    anomalies_list = ALL_ANOMALIES.to_dict(orient='records')
    if anomalies_list:
        for anomaly in anomalies_list:
            grouped_anomalies[anomaly["AccountName"]].append(anomaly)
    # Prepare anomaly counts for the chart.
    anomaly_counts = get_anomaly_counts_by_user(ALL_ANOMALIES)
    chart_data = {
        "users": [item['AccountName'] for item in anomaly_counts],
        "anomaly_counts": [item['AnomalyCount'] for item in anomaly_counts]
    }
    # Return grouped anomalies and chart data as JSON.
    return jsonify({
        "users": grouped_anomalies,
        "chart_data": chart_data
    })

# Flask route to get all anomalies and the scatter plot.
@app.route("/get_anomalies")
def get_anomalies():
    global ALL_ANOMALIES
    # Get new files and process them.
    new_files = get_new_files()
    all_data = pd.DataFrame()
    for filepath in new_files:
        anomalies, data = process_file(filepath)
        if not anomalies.empty:
            ALL_ANOMALIES = pd.concat([ALL_ANOMALIES, anomalies])
        if not data.empty:
            all_data = pd.concat([all_data, data])
        PROCESSED_FILES.add(os.path.basename(filepath))
    # Generate scatter plot and anomaly counts.
    plot_div = generate_scatter_plot(all_data)
    anomaly_counts = get_anomaly_counts_by_user(ALL_ANOMALIES)
    # Return anomalies, plot, and anomaly counts as JSON.
    return jsonify({
        "anomalies": ALL_ANOMALIES.to_dict(orient="records"),
        "plot": plot_div,
        "anomaly_counts": anomaly_counts
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
