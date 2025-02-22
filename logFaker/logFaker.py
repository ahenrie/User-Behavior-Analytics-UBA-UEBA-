import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker for generating random user data
fake = Faker()

# Load the CSV file containing the original logs
df = pd.read_csv('../genuineLogs/parsed.csv')

# Function to generate a random event time
def generate_random_time():
    base_time = datetime(2025, 2, 22, 9, 48, 43)
    random_time = base_time + timedelta(seconds=random.randint(1, 3600))
    return random_time.strftime('%Y-%m-%d %H:%M:%S')

# Function to simulate fake logs
def generate_fake_log():
    return {
        "EventTime": generate_random_time(),
        "EventReceivedTime": generate_random_time(),
        "Hostname": fake.hostname(),
        "Keywords": random.randint(-9223372036854775808, 9223372036854775807),
        "EventType": random.choice(["INFO", "ERROR", "WARNING"]),
        "SeverityValue": random.randint(1, 5),
        "Severity": random.choice(["INFO", "ERROR", "WARNING"]),
        "EventID": random.randint(1000, 9999),
        "SourceName": fake.company(),
        "ProviderGuid": fake.uuid4(),
        "Version": random.randint(0, 5),
        "Task": random.randint(0, 10),
        "OpcodeValue": random.randint(0, 5),
        "RecordNumber": random.randint(1, 50000),
        "ProcessID": random.randint(1000, 9999),
        "ThreadID": random.randint(1000, 9999),
        "Channel": fake.word(),
        "Domain": fake.domain_name(),
        "AccountName": fake.user_name(),
        "UserID": fake.uuid4(),
        "AccountType": random.choice(["User", "Admin"]),
        "LogonType": random.choice(["Interactive", "Network", "RemoteInteractive"]),
        "IpAddress": fake.ipv4(),
        "IpPort": random.choice([str(random.randint(1024, 65535)) for _ in range(5)]),
        "DeviceInstanceId": fake.uuid4(),
        "DeviceCount": str(random.randint(1, 10)),
        "Message": fake.sentence(),
        "Opcode": fake.word(),
        "PackageFullName": fake.word(),
        "AppUserModelId": fake.uuid4(),
        "AppSettings": str(random.randint(1000, 9999)),
        "FunctionName": fake.word(),
        "ErrorCode": fake.random_number(),
        "SourceModuleName": fake.word(),
        "SourceModuleType": fake.word()
    }

# Generate fake logs and save them to a new CSV
fake_logs = [generate_fake_log() for _ in range(10000000)]
fake_logs_df = pd.DataFrame(fake_logs)

# Save the fake logs to a CSV file
fake_logs_df.to_csv('generated_fake_logs.csv', index=False)
