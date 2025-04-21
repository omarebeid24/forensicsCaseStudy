This directory contains the source code and database schema for a simulated online banking server environment. It was created to model a real-world financial platform targeted in a cyberattack scenario. The goal is to provide a realistic setup for analyzing attack vectors such as web-based payloads, credential harvesting, and lateral movement.

Application Structure:
index.php – Landing/login page for users accessing their bank accounts.

dashboard.php – User dashboard displaying account information and balances.

transfer.php – Interface for making bank transfers between accounts.

admin.php – Admin-only interface for privileged account access.

logout.php – Logout script for securely ending user sessions.

db.php – Database connection file used by all core components.

Database:
bank.sql – MySQL dump containing the schema and sample records for users, accounts, and transactions.

⚠️ Forensic Purpose Only
This server environment was intentionally made vulnerable to support:

Phishing and payload injection testing

Web shell and backdoor deployment

Credential theft simulations

⚠️ Disclaimer: This project is for educational and controlled forensic investigation purposes only. Do not deploy on public or production systems.
