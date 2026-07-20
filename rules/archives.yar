rule SuspiciousArchiveFile
{
    meta:
        description = "Detects suspicious patterns in archive files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        // Archive file headers
        $zip = { 50 4B 03 04 } // ZIP
        $rar = { 52 61 72 21 } // RAR
        $tar = { 75 73 74 61 72 } // TAR
        $gzip = { 1F 8B } // GZIP
        $7z = { 37 7A BC AF 27 1C } // 7Z
        
        // Suspicious file extensions within archives
        $ext_exe = ".exe" nocase
        $ext_dll = ".dll" nocase
        $ext_bat = ".bat" nocase
        $ext_cmd = ".cmd" nocase
        $ext_ps1 = ".ps1" nocase
        $ext_vbs = ".vbs" nocase
        $ext_js = ".js" nocase
        $ext_wsf = ".wsf" nocase
        $ext_hta = ".hta" nocase
        $ext_scr = ".scr" nocase
        
        // Suspicious strings
        $susp1 = "cmd.exe" nocase
        $susp2 = "powershell.exe" nocase
        $susp3 = "wscript.exe" nocase
        $susp4 = "cscript.exe" nocase
        $susp5 = "rundll32.exe" nocase
    
    condition:
        (($zip at 0) or ($rar at 0) or ($tar at 0) or ($gzip at 0) or ($7z at 0)) and
        (any of ($ext_*) or any of ($susp*))
}

rule PasswordProtectedArchive
{
    meta:
        description = "Detects password-protected archive files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Low"
    
    strings:
        // Archive file headers
        $zip = { 50 4B 03 04 } // ZIP
        $rar = { 52 61 72 21 } // RAR
        
        // Password protection indicators for ZIP
        $zip_encrypt1 = { 01 00 63 00 00 00 } // General purpose bit flag with bit 0 set (encryption)
        $zip_encrypt2 = { 01 00 09 00 00 00 } // Another encryption signature
        
        // Password protection indicators for RAR
        $rar_encrypt1 = { 90 73 00 00 } // RAR encryption header
        $rar_encrypt2 = { 50 61 73 73 77 6F 72 64 } // "Password" string
    
    condition:
        ($zip at 0 and ($zip_encrypt1 or $zip_encrypt2)) or
        ($rar at 0 and ($rar_encrypt1 or $rar_encrypt2))
}
