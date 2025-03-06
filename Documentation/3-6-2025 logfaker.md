---
title: "Log Faker for Synthetic Windows Event Logs"
author: "Arza Henrie"
date: "2025-03-06"
version: "1.0"
status: "Draft"
category: "Cybersecurity / Machine Learning"
project: "CS Capstone - UAB"
license: "MIT"
---
# Log Faker for Synthetic Windows Event Logs

## Overview
This Python script generates synthetic Windows Event Logs using the `Faker` library. It preserves real hostnames and usernames from an existing dataset while creating realistic event entries for behavioral analysis and machine learning.

## Features
- Generates synthetic Windows Event Logs based on an existing dataset.
- Preserves real hostnames while introducing randomized but realistic event details.
- Ensures timestamps fall within Monday to Friday, 9 AM to 5 PM.
- Randomly selects applications from a predefined list of executables.
- Generates network-related details like IP addresses and ports.
- Saves the generated logs in CSV format for further analysis.

## Requirements
Ensure you have the following Python packages installed before running the script:

```sh
pip install pandas faker numpy
```

## How It Works
1. **Define Applications and Usernames**: A list of common Windows applications and usernames (`doris`, `Robot`) is preloaded.
2. **Generate Random Timestamps**: Ensures event times fall within typical working hours (Monday to Friday, 9 AM - 5 PM).
3. **Select Random Event Attributes**: Pulls random values from an existing dataset to ensure diversity.
4. **Create Log Entries**: Each entry includes details like EventID, Severity, ProcessID, Hostname, and an Application Message.
5. **Save as CSV**: Outputs the generated logs to `fakelogs.csv`.

## Usage
1. Place a CSV file (`test.csv`) with existing logs in the working directory.
2. Run the script to generate synthetic logs:

```sh
python log_faker.py
```

3. The script will generate `fakelogs.csv` containing the synthetic logs.

## Code Breakdown
### 1. **Initialize Faker and Define Applications**
```python
from faker import Faker
fake = Faker()
applications = ['chrome.exe', 'svchost.exe', 'explorer.exe', 'python.exe', 'powershell.exe', 'msedge.exe']
```

### 2. **Generate Random Timestamps**
```python
from datetime import datetime, timedelta
import random

def generate_random_time():
    while True:
        random_hour = random.randint(9, 17)
        random_date = fake.date_this_year()
        date_time_str = f"{random_date} {random_hour}:00:00"
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        if date_time.weekday() < 5:
            return date_time
```

### 3. **Generate Synthetic Logs**
```python
import pandas as pd

def generate_synthetic_logs(existing_logs, num_synthetic=100):
    synthetic_logs = []
    for _ in range(num_synthetic):
        event_time = generate_random_time()
        event_received_time = event_time + timedelta(seconds=random.randint(0, 30))
        hostname = random.choice(existing_logs['Hostname'])
        application = random.choice(applications)
        message = f"Application {application} performed an action."

        synthetic_logs.append({
            'EventTime': event_time,
            'EventReceivedTime': event_received_time,
            'Hostname': hostname,
            'Application': application,
            'Message': message
        })
    return pd.DataFrame(synthetic_logs)
```

### 4. **Read Existing Logs and Generate Synthetic Data**
```python
logs_df = pd.read_csv('test.csv')
synthetic_df = generate_synthetic_logs(logs_df, 1000)
synthetic_df.to_csv('fakelogs.csv', index=False)
print("Synthetic logs generated and saved.")
```

## Applications
- **Cybersecurity Research**: Use the logs to train anomaly detection models.
- **Behavioral Analytics**: Identify suspicious patterns in user and process activity.
- **SIEM Testing**: Test log ingestion and alerting mechanisms in Security Information and Event Management (SIEM) systems.
