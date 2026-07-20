rule SuspiciousDocumentFile
{
    meta:
        description = "Detects suspicious patterns in document files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "High"
    
    strings:
        // Document file headers
        $pdf = { 25 50 44 46 } // %PDF
        $doc = { D0 CF 11 E0 } // DOC/XLS/PPT
        $docx = { 50 4B 03 04 } // DOCX/XLSX/PPTX (ZIP format)
        
        // Suspicious strings in documents
        $macro1 = "AutoOpen" nocase
        $macro2 = "AutoExec" nocase
        $macro3 = "Document_Open" nocase
        $macro4 = "Auto_Open" nocase
        $macro5 = "AutoExit" nocase
        $macro6 = "Shell" nocase
        $macro7 = "VBA" nocase
        $macro8 = "CreateObject" nocase
        $macro9 = "WScript.Shell" nocase
        $macro10 = "PowerShell" nocase
        
        // JavaScript in PDF
        $js1 = "JavaScript" nocase
        $js2 = "/JS" nocase
        $js3 = "/JavaScript" nocase
        $js4 = "eval" nocase
        $js5 = "unescape" nocase
        
        // Suspicious functions
        $susp1 = "cmd.exe" nocase
        $susp2 = "powershell.exe" nocase
        $susp3 = "wget" nocase
        $susp4 = "curl" nocase
        $susp5 = "bitsadmin" nocase
    
    condition:
        (($pdf at 0) or ($doc at 0) or ($docx at 0)) and
        (2 of ($macro*) or 2 of ($js*) or any of ($susp*))
}

rule MaliciousPDF
{
    meta:
        description = "Detects potentially malicious PDF files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "High"
    
    strings:
        $pdf_header = { 25 50 44 46 } // %PDF
        
        // Suspicious PDF elements
        $obj = "/ObjStm" nocase
        $js = "/JavaScript" nocase
        $action = "/Action" nocase
        $launch = "/Launch" nocase
        $uri = "/URI" nocase
        $form = "/AcroForm" nocase
        $xfa = "/XFA" nocase
        $openaction = "/OpenAction" nocase
        $aa = "/AA" nocase
        
        // Suspicious functions
        $suspicious1 = "eval" nocase
        $suspicious2 = "unescape" nocase
        $suspicious3 = "String.fromCharCode" nocase
        $suspicious4 = "getAnnots" nocase
        $suspicious5 = "getIcon" nocase
        $suspicious6 = "util.exec" nocase
        $suspicious7 = "app.exec" nocase
        $suspicious8 = "app.launch" nocase
    
    condition:
        $pdf_header at 0 and
        (2 of ($obj, $js, $action, $launch, $uri, $form, $xfa, $openaction, $aa) and
         any of ($suspicious*))
}
