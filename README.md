# User-Behavior-Analytics-UBA-UEBA

## Key Areas of Focus for Insider Threat Detection:
- User Behavior Analytics (UBA/UEBA) – Detects deviations from normal user behavior.
- Access & Authentication Anomalies – Flags unusual login times, locations, or privilege escalations.
- Data Exfiltration Detection – Identifies large file transfers, unauthorized USB usage, or emails with sensitive data.
- Privilege Misuse – Monitors users with admin access for unusual activities.
- Process & Application Monitoring – Detects unauthorized tools or scripts being executed.

## Log Sources You Could Fabricate:
- Authentication logs (Active Directory, Okta, or IAM logs)
- File access logs (sensitive data access patterns)
- Network logs (VPN, proxy, DNS queries)
- USB device insertions and file transfers
- Failed login attempts and privilege escalations
- Email and communication logs (optional for phishing detection)

## Machine Learning Approaches:
- Unsupervised Anomaly Detection (Isolation Forest, Autoencoders, DBSCAN) to detect outliers.
- Behavior Profiling with Time-Series Analysis (LSTMs, Hidden Markov Models) to track user activity over time.
- Graph-Based Analysis to model relationships between users, devices, and access patterns.
