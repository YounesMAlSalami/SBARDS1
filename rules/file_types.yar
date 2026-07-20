/*
 * SBARDS Project - File Type Detection YARA Rules
 * 
 * These rules detect common file types based on file headers and content.
 * 
 * Author: SBARDS Project Team
 * Date: 2023-07-15
 * Version: 1.0
 */

rule PE_Executable {
    meta:
        description = "Detects Windows PE executables"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $mz = "MZ"
        $pe = "PE\x00\x00"
    condition:
        $mz at 0 and $pe
}

rule ELF_Executable {
    meta:
        description = "Detects ELF executables (Linux/Unix)"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $elf = { 7F 45 4C 46 }
    condition:
        $elf at 0
}

rule Mach_O_Executable {
    meta:
        description = "Detects Mach-O executables (macOS)"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $macho_32 = { CE FA ED FE }
        $macho_64 = { CF FA ED FE }
        $macho_fat = { CA FE BA BE }
    condition:
        $macho_32 at 0 or $macho_64 at 0 or $macho_fat at 0
}

rule DLL_File {
    meta:
        description = "Detects Windows DLL files"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $mz = "MZ"
        $pe = "PE\x00\x00"
        $dll = { 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 }
    condition:
        $mz at 0 and $pe and $dll
}

rule PDF_File {
    meta:
        description = "Detects PDF files"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $pdf = "%PDF-"
        $eof = "%%EOF"
    condition:
        $pdf at 0 and $eof
}

rule ZIP_File {
    meta:
        description = "Detects ZIP files"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $zip = { 50 4B 03 04 }
        $empty_zip = { 50 4B 05 06 }
        $spanned_zip = { 50 4B 07 08 }
    condition:
        $zip at 0 or $empty_zip at 0 or $spanned_zip at 0
}

rule Office_Document {
    meta:
        description = "Detects Microsoft Office documents"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $ole = { D0 CF 11 E0 A1 B1 1A E1 }
        $zip = { 50 4B 03 04 }
        $word = "word/"
        $excel = "xl/"
        $ppt = "ppt/"
    condition:
        ($ole at 0) or ($zip at 0 and ($word or $excel or $ppt))
}

rule JPEG_Image {
    meta:
        description = "Detects JPEG images"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $jpeg = { FF D8 FF }
    condition:
        $jpeg at 0
}

rule PNG_Image {
    meta:
        description = "Detects PNG images"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $png = { 89 50 4E 47 0D 0A 1A 0A }
    condition:
        $png at 0
}

rule GIF_Image {
    meta:
        description = "Detects GIF images"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $gif87 = "GIF87a"
        $gif89 = "GIF89a"
    condition:
        $gif87 at 0 or $gif89 at 0
}

rule Audio_File {
    meta:
        description = "Detects common audio file formats"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $wav = "RIFF" // WAV files
        $mp3 = { 49 44 33 } // MP3 files with ID3 tag
        $ogg = { 4F 67 67 53 } // OGG files
        $flac = { 66 4C 61 43 } // FLAC files
    condition:
        $wav at 0 or $mp3 at 0 or $ogg at 0 or $flac at 0
}

rule Video_File {
    meta:
        description = "Detects common video file formats"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $avi = "RIFF" // AVI files
        $mp4 = { 00 00 00 [1-4] 66 74 79 70 } // MP4 files
        $mkv = { 1A 45 DF A3 } // MKV files
        $flv = { 46 4C 56 01 } // FLV files
    condition:
        $avi at 0 or $mp4 in (0..8) or $mkv at 0 or $flv at 0
}

rule Script_File {
    meta:
        description = "Detects script files (shell, batch, PowerShell, etc.)"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "info"
        date = "2023-07-15"
    strings:
        $bash = "#!/bin/bash"
        $sh = "#!/bin/sh"
        $python = "#!/usr/bin/python"
        $perl = "#!/usr/bin/perl"
        $batch = "@echo off"
        $powershell = "<#"
        $ps_import = "Import-Module"
        $ps_function = "function "
        $ps_param = "param("
    condition:
        any of them
}

rule Encrypted_File {
    meta:
        description = "Detects potentially encrypted files"
        author = "SBARDS Project Team"
        reference = "Internal Research"
        severity = "medium"
        date = "2023-07-15"
    condition:
        // High entropy check - file has random-looking content
        // This is a simplified check that looks for lack of repeating patterns
        filesize > 100 and
        not (
            // Known file headers
            uint32(0) == 0x464C457F or // ELF
            uint16(0) == 0x5A4D or // MZ
            uint32(0) == 0xE011CFD0 or // OLE
            uint32(0) == 0x04034B50 or // ZIP
            uint16(0) == 0xD8FF or // JPEG
            uint32(0) == 0x474E5089 or // PNG
            uint32(0) == 0x46494947 or // GIF
            uint32(0) == 0x46464952 or // RIFF
            uint32(0) == 0x5367674F or // OGG
            uint32(0) == 0x43614C66 // FLAC
        ) and
        // Check for lack of common text patterns
        not (
            // ASCII text markers
            uint8(0) == 0x3C or // <
            uint8(0) == 0x7B or // {
            uint8(0) == 0x23 or // #
            uint8(0) == 0x2F or // /
            uint8(0) == 0x69 or // i (import)
            uint8(0) == 0x66 or // f (function)
            uint8(0) == 0x76 or // v (var)
            uint8(0) == 0x63 or // c (class)
            uint8(0) == 0x70 or // p (package)
            uint8(0) == 0x3D // =
        )
}
