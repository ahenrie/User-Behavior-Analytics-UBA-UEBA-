---
title: "Windows Event Log Feature Extraction"
author: "Arza Henrie"
date: "2025-02-26"
version: "1.0"
status: "Draft"
category: "Cybersecurity / Machine Learning"
project: "CS Capstone - UAB"
license: "MIT"
---

# Windows Event Log Feature Extraction

Before creating fake Windows Event logs, I need to understand what is in them and how they are structured. I am going to break down each field or feature and do some research to get some context. This will help me determine which features should be used in our machine learning model.

## List of Features

| Feature | Description |
|---------|-------------|
| `EventTime` | The exact timestamp when an event occurred on the system. |
| `EventReceivedTime` | The timestamp when the event was logged to the logging service. |
| `Date` | Date of the event. |
| `Hour` | Hour of the event. |
| `DayOfWeek` | Day of the week of the event. |
| `MonthYear` | Month and year of the event. |
| `Hostname` | Name of the host where the log occurred. |
| `Keywords` | A 64-bit mask where bits represent keywords, including Audit Success and Audit Failure events. |
| `EventType` | The type of log: ERROR, INFO, WARNING, VERBOSE. |
| `SeverityValue` | Integer (1-4) tied to the severity type. |
| `Severity` | Severity type: DEBUG, INFO, ERROR, WARNING. |
| `EventID` | Windows ID number that specifies the event type. |
| `SourceName` | The name of the application or service that generated the event. |
| `ProviderGuid` | A unique identifier (GUID) for the application or system component generating the event. |
| `Version` | The version of the program source if reported. |
| `Task` | ID representing a specific action or operation within a process. |
| `OpcodeValue` | Numeric value identifying an activity or point within an activity when the event occurred. |
| `RecordNumber` | The record number for the event log entry. |
| `ProcessID` | Unique numerical identifier assigned to each running process on a system. |
| `ThreadID` | Thread identifier for the thread in which the event provider is running. |
| `Channel` | A named stream of events serving as a logical pathway for transporting events. |
| `Domain` | The domain controller name logged in the details of error events. |
| `AccountName` | The username of the user account that performed an action. |
| `UserID` | The ID associated with each user. |
| `AccountType` | The type of user account. |
| `LogonType` | Policy setting managing logon options. |
| `IpAddress` | IP address of the source. |
| `IpPort` | Port number associated with the event. |
| `DeviceInstanceId` | Unique identifier assigned to each device on a system. |
| `DeviceCount` | Count of devices associated with an event. |
| `Opcode` | Numeric value identifying an application's activity when the event occurred. |
| `PackageFullName` | Unique identifier for a packaged application, often related to Windows Store apps. |
| `AppUserModelId` | Similar to `PackageFullName`, identifying an application. |
| `AppSettings` | Application-specific settings. |
| `FunctionName` | Identifier for a system error that can be disregarded. |
| `ErrorCode` | Error code associated with the event, if applicable. |
| `SourceModuleName` | The Nxlog module generating the event. |
| `SourceModuleType` | The type of the Nxlog module. |
| `Message` | The message associated with the event. |

## Sources
- [Windows Event Level Keywords](https://eventlogxp.com/blog/windows-event-level-keywords-or-type/)
- [Windows Event Logging](https://learn.microsoft.com/en-us/windows/win32/EventLog/event-logging)
- [EventLogRecord Thread ID](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.eventing.reader.eventlogrecord.threadid?view=windowsdesktop-9.0)
- [Windows Event Log Protocol](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-even6/f628d868-3810-4efe-bf44-c6e6901bf30e)
- [Internet Explorer Logon Policy](https://admx.help/?Category=InternetExplorer&Policy=Microsoft.Policies.InternetExplorer::IZ_PolicyLogon_9)
