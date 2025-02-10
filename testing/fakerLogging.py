import random
import sys
from datetime import datetime
from faker import Faker

# Create a Faker object
fake = Faker()

def random_priority():
    priorities = {
        0: 'EMERGENCY', 1: 'ALERT', 2: 'CRITICAL', 3: 'ERROR',
        4: 'WARNING', 5: 'NOTICE', 6: 'INFO', 7: 'DEBUG'
    }
    severity = random.randint(0, 7)
    facility = random.randint(0, 23)
    priority_num = facility * 8 + severity
    return priority_num, priorities[severity]

def generate_structured_data():
    if random.random() < 0.5:
        sd_id = f"exampleSDID@{random.randint(1000, 9999)}"
        params = [f'{fake.word()}="{fake.word()}"' for _ in range(random.randint(1, 3))]
        return f"[{sd_id} {' '.join(params)}]"
    return None

def generate_syslog_message():
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    hostname = fake.hostname()
    app_name = fake.word().capitalize()
    procid = random.randint(1, 9999)
    msgid = fake.random_int(min=1, max=9999)
    message = fake.sentence()
    structured_data = generate_structured_data()
    priority_num, priority_text = random_priority()
    priority = f'<{priority_num}>1'
    header = f'{priority} {timestamp} {hostname} {app_name} {procid} {msgid}'

    syslog_msg = f'{header} {structured_data} {message}' if structured_data else f'{header} - {message}'

    # Print to console (stdout)
    print(syslog_msg)

# Generate and print 10 syslog messages to console
for _ in range(10):
    generate_syslog_message()
