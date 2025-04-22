# 🕵️‍♂️ Phantom Breach – Digital Forensics Case Study

**Repository Name:** `phantom-breach-case-study`  
**Case ID:** NXT-2025-DFIR-042  
**Target Organization:** NexusTech Financial Services  
**Date of Incident:** April 4–6, 2025  
**Status:** 🔒 Closed | 🟡 Confirmed Data Breach

---

## 📖 Overview

This repository documents a full-scope digital forensics investigation conducted on a critical financial breach simulation at NexusTech Financial Services. The attack scenario involved a multi-stage intrusion starting with a phishing email, a malicious PDF payload, banking trojan deployment, lateral movement, data exfiltration, and ransomware preparation.

The project simulates both attacker and defender environments to support cybersecurity education, malware analysis, memory forensics, and attack chain reconstruction.

---

## 🧠 Objective

To investigate, analyze, and document the lifecycle of a sophisticated breach using industry-standard tools and techniques.  
Key goals:
- Reconstruct the attack timeline
- Analyze evidence across disk, memory, logs, and network
- Identify the indicators of compromise (IOCs)
- Simulate both attacker infrastructure and victim systems
- Provide remediation and prevention recommendations

---

## 📂 Repository Structure

```plaintext
.
├── pdf_payloads/         # Malicious PDF & scripts used for initial infection
├── phishing_scripts/     # Scripts and HTML for email-based phishing
├── backdoor/             # Backdoor installation and C2 listener
├── web_payloads/         # PHP-based banking trojan (web skimmer)
├── bank_server/          # Simulated bank web application (victim system)
├── config/               # Configuration files (JSON command sets, etc.)
├── system_updates/       # Fake update scripts used for disguise
├── Final Report.pdf      # Full forensic investigation documentation
└── README.md             # This file
```

## 🔍 Technical Summary

- Initial Vector: Spearphishing Email
- Attachment: Security_Update_2025.pdf
- Execution: Embedded JavaScript → downloads deploy_pdf_payload.bat
- Payload: Banking trojan in bank_hijacker.php
- C2 Infrastructure: Apache server via XAMPP
- Persistence: Scheduled tasks and BITS job abuse
- Ransomware Stage: LockBit & DarkSide indicators found
- Exfiltration: HTTP POST requests and staged MySQL exports
- Impact: Millions in fake transactions + credential theft

## 🛠 Tools Used
- FTK Imager – Disk imaging and analysis

- Volatility 3 – Memory forensics

- Wireshark / Tshark – PCAP protocol and credential analysis

- Autopsy – Filesystem timeline reconstruction

- Custom Scripts – Batch, PowerShell, PHP, Python
  

## 📌 Notes
- All files are for simulation and training purposes only.

- Do not use these payloads or scripts outside of isolated lab environments.

- The forensic timeline and report are based on a fictional breach simulation conducted for academic purposes.
