rule SuspiciousCertificate
{
    meta:
        description = "Detects suspicious certificate-related patterns"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "High"
    
    strings:
        // Certificate file extensions
        $ext_cert1 = ".crt" nocase
        $ext_cert2 = ".pem" nocase
        $ext_cert3 = ".der" nocase
        $ext_cert4 = ".p12" nocase
        $ext_cert5 = ".pfx" nocase
        
        // Certificate headers
        $cert_header1 = "-----BEGIN CERTIFICATE-----" nocase
        $cert_header2 = "-----BEGIN PRIVATE KEY-----" nocase
        $cert_header3 = "-----BEGIN RSA PRIVATE KEY-----" nocase
        $cert_header4 = "-----BEGIN DSA PRIVATE KEY-----" nocase
        $cert_header5 = "-----BEGIN EC PRIVATE KEY-----" nocase
        
        // Suspicious strings in certificates
        $susp1 = "localhost" nocase
        $susp2 = "127.0.0.1" nocase
        $susp3 = "test" nocase
        $susp4 = "example" nocase
        $susp5 = "dummy" nocase
        $susp6 = "fake" nocase
        $susp7 = "invalid" nocase
        $susp8 = "expired" nocase
        $susp9 = "revoked" nocase
        $susp10 = "untrusted" nocase
    
    condition:
        (any of ($ext_cert*) or any of ($cert_header*)) and
        any of ($susp*)
}

rule SelfSignedCertificate
{
    meta:
        description = "Detects self-signed certificates"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        // Certificate headers
        $cert_header1 = "-----BEGIN CERTIFICATE-----" nocase
        $cert_header2 = "-----BEGIN PRIVATE KEY-----" nocase
        $cert_header3 = "-----BEGIN RSA PRIVATE KEY-----" nocase
        
        // Self-signed indicators
        $self1 = "self signed" nocase
        $self2 = "self-signed" nocase
        $self3 = "selfsigned" nocase
        $self4 = "own certificate" nocase
        
        // Same subject and issuer (common in self-signed certs)
        $same1 = "Subject: CN=" nocase
        $same2 = "Issuer: CN=" nocase
    
    condition:
        any of ($cert_header*) and
        (any of ($self*) or ($same1 and $same2))
}
