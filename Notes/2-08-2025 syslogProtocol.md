---
title: "syslog"
author: "Arza Henrie"
date: "2025-02-08"
version: "1.0"
status: "Draft"
category: "Cybersecurity / Machine Learning"
project: "CS Capstone - UAB"
license: "MIT"
---

# The Syslog Protocol

**Source:** [RFC 5424](https://datatracker.ietf.org/doc/html/rfc5424)

## **Structure of a Syslog Message**
A syslog message consists of three main components:

1. **HEADER** – Contains metadata such as priority, version, timestamp, hostname, application name, process ID, and message ID.
2. **STRUCTURED-DATA (Optional)** – Allows structured information to be included using key-value pairs.
3. **MSG (Optional)** – The actual log message.

---

## **HEADER Details**
The HEADER contains several fields, all in ASCII (except MSG).

- **PRI (Priority):** Indicates message severity and facility (system type).
  - Computed as: `Facility * 8 + Severity`
  - Expressed as: `<PRIVAL>`

- **VERSION:** Syslog protocol version (currently `1`).

- **TIMESTAMP:**
  - Uses RFC 3339 format (`YYYY-MM-DDThh:mm:ssZ`).
  - No leap seconds allowed.
  - May be set to `"-"` (NILVALUE).

- **HOSTNAME:** Identifies the message's source (FQDN, IP address, or hostname). Can be `"-"`.

- **APP-NAME:** Name of the application sending the message. Can be `"-"`.

- **PROCID:** Identifier for the process (often a PID). Can be `"-"`.

- **MSGID:** Identifies the type of message. Can be `"-"`.

---

## **STRUCTURED-DATA Details**
Structured data allows for additional metadata using **SD-ELEMENTs**, each consisting of:

- **SD-ID:**
  - Identifier for structured data (e.g., `timeQuality@32473`).
  - Can be an IANA-registered name or a private enterprise name.

- **SD-PARAM:**
  - Name-value pairs (`PARAM-NAME="PARAM-VALUE"`).
  - Values are UTF-8 encoded and may contain escaped characters (`"`, `\`, `]`).

- **Example Structured Data Block:**
  ```plaintext
  [timeQuality tzKnown="1" isSynced="1" syncAccuracy="12345"]
  ```

---

## **MSG Details**
- Contains the actual log message.
- Ideally **UTF-8 encoded** (indicated by a **Byte Order Mark - BOM**).
- Other encodings are allowed if UTF-8 isn't available.
- Control characters (ASCII < 32) **should be avoided**.

---

## **Message Length**
- No strict upper limit.
- Transport receivers must support at least **480 octets**, should support **2048 octets**, and may allow more.
- If too long, truncation is allowed.

---

## **Key Considerations**
- **Standardization & Interoperability:** Defines a robust syslog format for better system communication.
- **Predefined SD-IDs:** Includes standard metadata fields (`timeQuality`, `origin`).
- **Encoding Rules:** UTF-8 recommended, escape sequences defined for special characters.

This RFC aims to **standardize logging practices** and **improve interoperability** across different systems while allowing flexibility in message structure.
