@echo off
REM Malicious keylogger simulation (FOR TESTING ONLY - DOES NOT ACTUALLY LOG KEYS)
REM This is a simulated malicious batch file for testing security tools

echo [*] Starting keylogger simulation...
echo [*] This is a test file for security scanning - no actual keylogging will occur

REM Create a hidden directory for logs
mkdir %TEMP%\system32_logs
attrib +h %TEMP%\system32_logs

REM Add startup persistence
echo @echo off > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\system_service.bat"
echo start /min powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -Command "& {Start-Process '%~f0' -WindowStyle Hidden}" >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\system_service.bat"

REM Simulate keylogging
echo [*] Keylogger running in background...
echo [*] Capturing keystrokes from all applications...
echo [*] Logging to %TEMP%\system32_logs\keylog.dat

REM Simulate sending data to C2 server
echo [*] Connecting to command and control server: http://malicious-keylogger.com/exfil
echo [*] Sending captured data every 30 minutes

REM Simulate anti-analysis techniques
echo [*] Implementing anti-VM detection
echo [*] Checking for debugging tools
echo [*] Implementing sandbox evasion techniques

REM Simulate disabling security tools
echo [*] Attempting to disable Windows Defender...
echo [*] Attempting to disable firewall...
echo [*] Attempting to terminate security processes...

echo [+] Keylogger successfully installed and running!
echo [+] This simulation is complete - no actual malicious actions were performed

REM This is a test file for security scanning - no actual malicious actions are performed
