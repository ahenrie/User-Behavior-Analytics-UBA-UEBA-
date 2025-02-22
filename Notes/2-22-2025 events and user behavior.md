---
title: "Anomaly Detection with Windows Event Logs"
author: "Arza Henrie"
date: "2025-02-22"
version: "1.0"
status: "Draft"
category: "Cybersecurity / Machine Learning"
project: "CS Capstone - UAB"
license: "MIT"
---

# Updates for 2-22-2025
1. Logs are now being sent via nxlog in json formatting, so more data is captured
2. Two Golang parsers:
  - One for generic rsyslog formatting
  - the other is for the json formatting that is more complicated and
3. Python program will be used to generate logs using the faker library and genuine logs

## Golang Log Parsers
They both do the same thing differently. They create a csv file and extract the different data fields from the logs into features that can be used for machine learning.
