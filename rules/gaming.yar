rule SuspiciousGamingFile
{
    meta:
        description = "Detects suspicious patterns in gaming files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        // Common game file extensions
        $ext_sav = ".sav" nocase
        $ext_pak = ".pak" nocase
        $ext_dat = ".dat" nocase
        $ext_cfg = ".cfg" nocase
        $ext_ini = ".ini" nocase
        $ext_bin = ".bin" nocase
        $ext_asset = ".asset" nocase
        $ext_unity = ".unity3d" nocase
        $ext_unreal = ".uasset" nocase
        
        // Suspicious strings that shouldn't be in game files
        $susp1 = "cmd.exe" nocase
        $susp2 = "powershell" nocase
        $susp3 = "eval(" nocase
        $susp4 = "exec(" nocase
        $susp5 = "system(" nocase
        $susp6 = "CreateProcess" nocase
        $susp7 = "VirtualAlloc" nocase
        $susp8 = "shellcode" nocase
        $susp9 = "payload" nocase
        $susp10 = "<script" nocase
        
        // Executable content
        $exe = { 4D 5A } // MZ header
    
    condition:
        any of ($ext_*) and (any of ($susp*) or $exe)
}

rule GameModCheat
{
    meta:
        description = "Detects potential game cheats or unauthorized mods"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Low"
    
    strings:
        // Cheat-related strings
        $cheat1 = "cheat" nocase
        $cheat2 = "hack" nocase
        $cheat3 = "trainer" nocase
        $cheat4 = "aimbot" nocase
        $cheat5 = "wallhack" nocase
        $cheat6 = "godmode" nocase
        $cheat7 = "noclip" nocase
        $cheat8 = "speedhack" nocase
        $cheat9 = "unlimited" nocase
        $cheat10 = "infinite" nocase
        
        // Memory manipulation
        $mem1 = "memory" nocase
        $mem2 = "inject" nocase
        $mem3 = "hook" nocase
        $mem4 = "patch" nocase
        $mem5 = "bypass" nocase
        
        // Anti-cheat evasion
        $anti1 = "anticheat" nocase
        $anti2 = "detection" nocase
        $anti3 = "bypass" nocase
        $anti4 = "evasion" nocase
        $anti5 = "undetected" nocase
    
    condition:
        3 of ($cheat*) or (2 of ($mem*) and 2 of ($cheat*)) or (2 of ($anti*) and 2 of ($cheat*))
}
