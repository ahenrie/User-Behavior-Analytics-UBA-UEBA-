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

Before creating fake Windows Event logs, I need to understand what are in them, and how they are structured. I am going to breakdown each field or feature and do some research to get some context. This will help me to know what features should be used in our machine learning model.

## List of Features
1. `EventTime`--> The exact timestamp when an event occured on the system.
2. `EventReceivedTime`--> The timestamp when the event was logged to the logging service.
3. `Date`--> Date of event.
4. `Hour`--> Hour of event.
5. `DayOfWeek`--> Day of the week of the event.
6. `MonthYear`--> Month and year of the event.
7. `Hostname`--> Name of the host where the log occurred.
8. `Keywords`--> "There is a new event attribute called keywords. Keywords is a 64-bit mask, every bit of each may represent a keyword. 2 bits of this mask represent Audit Success and Audit Failure events" - Michael Karsyan
9. `EventType`--> The type of log: ERROR, INFO, WARNING, VERBOSE
10. `SeverityValue`--> 1-4 int that is tied to the severity type.
11. `Severity`--> Severity type: DEBUG, INFO, ERROR, WARNING
12. `EventID`--> Windows ID number that specifies the event type.
13. `SourceName`--> Refers to the name of the application or service that generated the event, essentially identifying the source of the log entry.
14. `ProviderGuid`--> A unique identifier (GUID) that identifies the specific application or system component that generated an event.
15. `Version`--> The version of the source of the program if the program reports it (?)
16. `Task`--> ID that represents a specific action or operation within a process.
17. `OpcodeValue`--> "The opcode defines a numeric value that identifies the activity or a point within an activity that the application was performing when it raised the event" - Windows
18. `RecordNumber`--> "The RecordNumber member of EVENTLOGRECORD contains the record number for the event log record" - Microsoft
19. `ProcessID`--> A unique numerical identifier assigned to each running process on a system.
20. `ThreadID`--> "Gets the thread identifier for the thread that the event provider is running in." - Microsoft
21. `Channel`--> "A channel is a named stream of events. It serves as a logical pathway for transporting events from the event publisher to a log file and possibly a subscriber. It is a sink that collects events." - Microsoft
22. `Domain`--> The domain is represented in Windows event logs through the domain controller name, which is logged in the details of error events.
23. `AccountName`--> The username of the user account that performed an action.
24. `UserID`--> The ID associated with each user.
25. `AccountType`--> The type of the account of the user.
26. `LogonType`--> This policy setting allows you to manage settings for logon options.
27. `IpAddress`--> Address IP
28. `IpPort`--> Port
29. `DeviceInstanceId`--> Refers to a unique identifier assigned to each device on a system.
30. `DeviceCount`-->
31. `Opcode`--> A numeric value that identifies the activity of an application when an event occur
32. `PackageFullName`--> Refers to the unique identifier for a packaged application, typically found within the details of an event related to the installation, deployment, or operation of a Windows Store app.
33. `AppUserModelId`--> Pretty much the same thing as PackageFullName
34. `AppSettings`-->
35. `FunctionName`--> Identifier for a system error that we can disregard
36. `ErrorCode`--> Error code of the event if there is an error
37. `SourceModuleName`--> This will be the Nxlog module.
38. `SourceModuleType`--> This will be the Nxlog module.
39. `Message`--> Message


## Sources
- https://eventlogxp.com/blog/windows-event-level-keywords-or-type/
- https://learn.microsoft.com/en-us/windows/win32/EventLog/event-logging
- https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.eventing.reader.eventlogrecord.threadid?view=windowsdesktop-9.0
- https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-even6/f628d868-3810-4efe-bf44-c6e6901bf30e
- https://admx.help/?Category=InternetExplorer&Policy=Microsoft.Policies.InternetExplorer::IZ_PolicyLogon_9
