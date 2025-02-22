---
title: "Configuring NXLog"
author: "Arza Henrie"
date: "2025-01-29"
version: "1.0"
status: "Draft"
category: "Cybersecurity / Machine Learning"
project: "CS Capstone - UAB"
license: "MIT"
---
# Installation and Setup of NXLog on Windows Client

NXLog is a free log collection tool that works well on Windows and is easy to configure.

## Where is the Conf?

The conf file for declaring where to send the logs to and what protocols to use is in the following:

![Image](./pics/nxlogDir.png)

## Updated `nxlog.conf`

Here is the modified `nxlog.conf` file:

```bash
Panic Soft
#NoFreeOnExit TRUE

define ROOT     C:\Program Files\nxlog
define CERTDIR  %ROOT%\cert
define CONFDIR  %ROOT%\conf\nxlog.d
define LOGDIR   %ROOT%\data

include %CONFDIR%\\*.conf
define LOGFILE  %LOGDIR%\nxlog.log
LogFile %LOGFILE%

Moduledir %ROOT%\modules
CacheDir  %ROOT%\data
Pidfile   %ROOT%\data\nxlog.pid
SpoolDir  %ROOT%\data

<Extension _syslog>
    Module      xm_syslog
</Extension>

<Extension _charconv>
    Module      xm_charconv
    AutodetectCharsets iso8859-2, utf-8, utf-16, utf-32
</Extension>

<Extension _exec>
    Module      xm_exec
</Extension>

<Extension _fileop>
    Module      xm_fileop

    # Check the size of our log file hourly, rotate if larger than 5MB
    <Schedule>
        Every   1 hour
        Exec    if (file_exists('%LOGFILE%') and \
                   (file_size('%LOGFILE%') >= 5M)) \
                    file_cycle('%LOGFILE%', 8);
    </Schedule>

    # Rotate our log file every week on Sunday at midnight
    <Schedule>
        When    @weekly
        Exec    if file_exists('%LOGFILE%') file_cycle('%LOGFILE%', 8);
    </Schedule>
</Extension>
#####################################################################################################################
# Collecting Windows Event Logs
<Input in>
    Module      im_msvistalog
</Input>

# Sending logs to rsyslog server
<Output out>
    Module      om_tcp
    Host        10.10.10.42    # Ubuntu server
    Port        514
    Exec        to_syslog();
</Output>
#####################################################################################################################
# Connect input 'in' to output 'out'
<Route 1>
    Path        in => out
</Route>
```
## Restarting the Service

NXlog needs to be restarted for the changes to take.

![Image](./pics/nxlogSer.png)
