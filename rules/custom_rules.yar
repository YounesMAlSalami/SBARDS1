rule ExampleRule
{
    meta:
        description = "This is an example rule"
        author = "SBARDS Project"
        date = "2025-05-11"
    
    strings:
        $text_string = "malicious" nocase
        $hex_string = { 4D 5A 90 00 }  // MZ header for PE files
    
    condition:
        any of them
}

rule PotentialRansomware
{
    meta:
        description = "Detects potential ransomware characteristics"
        author = "SBARDS Project"
        date = "2025-05-11"
    
    strings:
        $ransom_note = "your files have been encrypted" nocase
        $bitcoin = "bitcoin" nocase
        $payment = "payment" nocase
        $decrypt = "decrypt" nocase
        $encrypt = "encrypt" nocase
    
    condition:
        $ransom_note or ($bitcoin and $payment) or ($encrypt and $decrypt)
}
