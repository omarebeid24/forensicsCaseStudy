This directory contains scripts that simulate the deployment and operation of a backdoor component used in the forensic case study. The goal is to replicate how attackers establish remote access to a compromised system and maintain persistence.

Contents:
deploy_backdoor.ps1 – A PowerShell script that emulates the setup and installation of a backdoor on a target system.

server.py – A Python script acting as the command-and-control (C2) server, listening for incoming connections from the deployed backdoor.

⚠️ Warning: These scripts are intended solely for educational and simulation purposes in a secure forensic lab environment. Do not use or run them on production or public systems.
