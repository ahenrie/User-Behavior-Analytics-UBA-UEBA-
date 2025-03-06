import pandas as pd
import random
from faker import Faker
import numpy as np
from datetime import datetime, timedelta

# Initialize Faker for generating realistic data
fake = Faker()

# Define the list of applications
applications = [
    'None', 'services.exe', 'RuntimeBroker.exe', 'winlogon.exe', 'svchost.exe', 'LogonUI.exe',
    'lsass.exe', 'NgcIso.exe', 'chrome.exe', 'opera.exe', 'explorer.exe', 'OneDriveUpdaterService.exe',
    'OneDriveSetup.exe', 'installer.exe', 'SystemSettings.exe', 'DllHost.exe', 'consent.exe',
    'OneDriveStandaloneUpdater.exe', 'SlackSetup.exe', 'slack.exe', 'OneDrive.exe', 'Code.exe',
    'setup.exe', 'msedge.exe', 'msedgewebview2.exe', 'powershell.exe', 'python.exe', 'identity_helper.exe',
    'firefox.exe', 'OfficeClickToRun.exe', 'taskhostw.exe', 'DeviceCensus.exe', 'devicecensus.exe',
    'WinLogon.exe', 'DefenderBootstrapper.exe', 'smss.exe', 'autochk.exe', 'csrss.exe', 'wininit.exe',
    'LsaIso.exe', 'lsaiso.exe', 'LSASS.exe', 'esif_uf.exe', 'SearchIndexer.exe', 'VSInstallerElevationService.exe',
    'VSSVC.exe', 'dllhost.exe', 'IisExpressAdminCmd.exe', 'sqlwriter.exe', 'msiexec.exe', 'DFInit.exe',
    'winsdksetup.exe', 'appverif.exe', 'appcertui.exe', 'WPRUI.exe', 'GPUView.exe', 'wpa.exe', 'TiWorker.exe',
    'd3dconfig.exe', 'DXCap.exe', 'DXCpl.exe', 'VsGraphicsDesktopEngine.exe', 'VsGraphicsRemoteEngine.exe',
    'netsh.exe', 'UnityHubSetup.exe', 'VSFinalizer.exe'
]

# Define the possible AccountNames
account_names = ['doris', 'Robot']

# Helper function to generate a random datetime between Monday to Friday, 9 AM to 5 PM
def generate_random_time():
    while True:
        random_hour = random.randint(9, 17)
        random_day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        random_date = fake.date_this_year()
        date_time_str = f"{random_date} {random_hour}:00:00"
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        # If it's within M-F, 9-5, we can use this time
        if date_time.weekday() < 5 and 9 <= date_time.hour <= 17:
            return date_time

# Helper function to generate synthetic logs
def generate_synthetic_logs(existing_logs, num_synthetic=100):
    synthetic_logs = []

    for _ in range(num_synthetic):
        # Randomly select values from the existing logs and apply small variations
        event_time = generate_random_time()
        event_received_time = event_time + timedelta(seconds=random.randint(0, 30))  # Small delay
        date = event_time.date().strftime("%Y-%m-%d")
        hour = event_time.hour
        day_of_week = event_time.strftime('%A')
        month_year = event_time.strftime("%b-%Y")
        hostname = random.choice(existing_logs['Hostname'])
        keywords = random.choice(existing_logs['Keywords'])
        event_type = random.choice(existing_logs['EventType'])
        severity_value = random.choice(existing_logs['SeverityValue'])
        severity = random.choice(existing_logs['Severity'])
        event_id = random.choice(existing_logs['EventID'])
        source_name = random.choice(existing_logs['SourceName'])
        provider_guid = fake.uuid4()  # Generate a random GUID
        version = random.choice(existing_logs['Version'])
        task = random.choice(existing_logs['Task'])
        opcode_value = random.choice(existing_logs['OpcodeValue'])
        record_number = random.randint(100000, 999999)
        process_id = random.randint(1000, 9999)
        thread_id = random.randint(1000, 9999)
        channel = random.choice(existing_logs['Channel'])
        domain = random.choice(existing_logs['Domain'])
        account_name = random.choice(account_names)
        user_id = random.randint(1000, 9999)
        account_type = random.choice(existing_logs['AccountType'])
        logon_type = random.choice(existing_logs['LogonType'])
        ip_address = fake.ipv4()  # Random IP address
        ip_port = random.randint(1024, 65535)
        device_instance_id = random.randint(10000, 99999)
        device_count = random.randint(1, 10)
        opcode = random.choice(existing_logs['Opcode'])
        source_module_type = random.choice(existing_logs['SourceModuleType'])

        # Randomly select an application to include in the message
        application = random.choice(applications)
        message = f"Application {application} performed an action."

        # Create synthetic log entry
        synthetic_logs.append({
            'EventTime': event_time,
            'EventReceivedTime': event_received_time,
            'Date': date,
            'Hour': hour,
            'DayOfWeek': day_of_week,
            'MonthYear': month_year,
            'Hostname': hostname,
            'Keywords': keywords,
            'EventType': event_type,
            'SeverityValue': severity_value,
            'Severity': severity,
            'EventID': event_id,
            'SourceName': source_name,
            'ProviderGuid': provider_guid,
            'Version': version,
            'Task': task,
            'OpcodeValue': opcode_value,
            'RecordNumber': record_number,
            'ProcessID': process_id,
            'ThreadID': thread_id,
            'Channel': channel,
            'Domain': domain,
            'AccountName': account_name,
            'UserID': user_id,
            'AccountType': account_type,
            'LogonType': logon_type,
            'IpAddress': ip_address,
            'IpPort': ip_port,
            'DeviceInstanceId': device_instance_id,
            'DeviceCount': device_count,
            'Opcode': opcode,
            'SourceModuleType': source_module_type,
            'Message': message
        })

    return pd.DataFrame(synthetic_logs)

logs_df = pd.read_csv('test.csv')

num_synthetic = 1000
synthetic_df = generate_synthetic_logs(logs_df, num_synthetic)

synthetic_df.to_csv('fakelogs.csv', index=False)

print("Synthetic logs generated and saved.")
