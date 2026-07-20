rule SuspiciousNetworkActivity
{
    meta:
        description = "Detects suspicious network-related patterns in files"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "High"
    
    strings:
        // Suspicious URLs and domains
        $url1 = /https?:\/\/[^\s\/$.?#].[^\s]*\.onion/ nocase // .onion (Tor) domains
        $url2 = /https?:\/\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/ nocase // IP URLs
        $url3 = /https?:\/\/[^\s\/$.?#].[^\s]*\.ru/ nocase // .ru domains
        $url4 = /https?:\/\/[^\s\/$.?#].[^\s]*\.cn/ nocase // .cn domains
        $url5 = /https?:\/\/[^\s\/$.?#].[^\s]*\.xyz/ nocase // .xyz domains
        $url6 = /https?:\/\/[^\s\/$.?#].[^\s]*\.top/ nocase // .top domains
        $url7 = /https?:\/\/[^\s\/$.?#].[^\s]*\.cc/ nocase // .cc domains
        $url8 = /https?:\/\/[^\s\/$.?#].[^\s]*\.tk/ nocase // .tk domains
        
        // Command and control patterns
        $c2_1 = "beacon" nocase
        $c2_2 = "command" nocase
        $c2_3 = "control" nocase
        $c2_4 = "check-in" nocase
        $c2_5 = "checkin" nocase
        $c2_6 = "heartbeat" nocase
        $c2_7 = "exfil" nocase
        $c2_8 = "callback" nocase
        
        // Network functions
        $net1 = "socket(" nocase
        $net2 = "connect(" nocase
        $net3 = "bind(" nocase
        $net4 = "listen(" nocase
        $net5 = "accept(" nocase
        $net6 = "recv(" nocase
        $net7 = "send(" nocase
        $net8 = "WSASocket" nocase
        $net9 = "InternetOpen" nocase
        $net10 = "URLDownloadToFile" nocase
    
    condition:
        any of ($url*) or (2 of ($c2_*) and 2 of ($net*))
}

rule SuspiciousDNSQueries
{
    meta:
        description = "Detects suspicious DNS-related patterns"
        author = "SBARDS Project"
        date = "2025-05-13"
        severity = "Medium"
    
    strings:
        // DNS functions
        $dns1 = "gethostbyname" nocase
        $dns2 = "getaddrinfo" nocase
        $dns3 = "DnsQuery" nocase
        $dns4 = "nslookup" nocase
        $dns5 = "dig" nocase
        
        // Domain generation algorithm (DGA) patterns
        $dga1 = /[a-z]{10,}\.[a-z]{2,3}/ nocase // Long random-looking domain
        $dga2 = /[a-z0-9]{16,}\.[a-z]{2,3}/ nocase // Long alphanumeric domain
        
        // DNS tunneling
        $tunnel1 = "base64" nocase
        $tunnel2 = "encode" nocase
        $tunnel3 = "decode" nocase
        $tunnel4 = "subdomain" nocase
        $tunnel5 = "exfiltrate" nocase
    
    condition:
        2 of ($dns*) and (any of ($dga*) or 2 of ($tunnel*))
}
