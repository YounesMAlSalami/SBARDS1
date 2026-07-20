rule SuspiciousMultimediaFile
{
    meta:
        description = "Detects suspicious patterns in multimedia files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        // Common image file headers
        $jpg = { FF D8 FF }
        $png = { 89 50 4E 47 }
        $gif = { 47 49 46 38 }
        
        // Common audio/video file headers
        $mp3 = { 49 44 33 }
        $mp4 = { 66 74 79 70 }
        $wav = { 52 49 46 46 }
        
        // Suspicious strings that shouldn't be in multimedia files
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
    
    condition:
        (($jpg at 0) or ($png at 0) or ($gif at 0) or ($mp3 at 0) or ($mp4 at 0) or ($wav at 0)) and
        any of ($susp*)
}

rule SteganographyDetection
{
    meta:
        description = "Detects potential steganography in image files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        // Common image file headers
        $jpg = { FF D8 FF }
        $png = { 89 50 4E 47 }
        $gif = { 47 49 46 38 }
        
        // Suspicious strings that might indicate steganography
        $steg1 = "outguess" nocase
        $steg2 = "steghide" nocase
        $steg3 = "stegdetect" nocase
        $steg4 = "steganography" nocase
        $steg5 = "hidden" nocase
        $steg6 = "secret" nocase
        $steg7 = "conceal" nocase
        $steg8 = "embed" nocase
        
        // Executable content in image
        $exe = "MZ" nocase
        $script = "<script" nocase
        $php = "<?php" nocase
    
    condition:
        (($jpg at 0) or ($png at 0) or ($gif at 0)) and
        (any of ($steg*) or $exe or $script or $php)
}
