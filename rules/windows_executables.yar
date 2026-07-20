rule WindowsExecutableMalware
{
    meta:
        description = "Detects common malware patterns in Windows executables"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "High"
    
    strings:
        $mz = "MZ" // PE file header
        $suspicious_api1 = "CreateRemoteThread" nocase
        $suspicious_api2 = "VirtualAllocEx" nocase
        $suspicious_api3 = "WriteProcessMemory" nocase
        $suspicious_api4 = "ShellExecute" nocase
        $suspicious_api5 = "WinExec" nocase
        $suspicious_api6 = "CreateProcess" nocase
        $suspicious_api7 = "ReadProcessMemory" nocase
        $suspicious_api8 = "SetWindowsHookEx" nocase
        $suspicious_api9 = "WSASocket" nocase
        $suspicious_api10 = "InternetOpen" nocase
    
    condition:
        $mz at 0 and 3 of ($suspicious_api*)
}

rule SuspiciousPowerShell
{
    meta:
        description = "Detects suspicious PowerShell commands"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        $ps1 = "powershell" nocase
        $ps2 = "-encodedcommand" nocase
        $ps3 = "-enc " nocase
        $ps4 = "-windowstyle hidden" nocase
        $ps5 = "IEX" nocase
        $ps6 = "Invoke-Expression" nocase
        $ps7 = "New-Object Net.WebClient" nocase
        $ps8 = "DownloadString" nocase
        $ps9 = "DownloadFile" nocase
        $ps10 = "hidden" nocase
    
    condition:
        $ps1 and 2 of ($ps2, $ps3, $ps4, $ps5, $ps6, $ps7, $ps8, $ps9, $ps10)
}

rule SuspiciousBatchFile
{
    meta:
        description = "Detects suspicious batch files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        $cmd1 = "cmd.exe" nocase
        $cmd2 = "del " nocase
        $cmd3 = "rmdir" nocase
        $cmd4 = "taskkill" nocase
        $cmd5 = "reg add" nocase
        $cmd6 = "reg delete" nocase
        $cmd7 = "netsh" nocase
        $cmd8 = "schtasks" nocase
        $cmd9 = "attrib +h" nocase
        $cmd10 = "start " nocase
    
    condition:
        4 of them
}
