#!/usr/bin/env python3
# Suspicious network scanner script (FOR TESTING ONLY)
# This script scans network ports and could be used for reconnaissance

import socket
import sys
import time
import random
import argparse
from datetime import datetime

def print_banner():
    """Print the tool banner"""
    banner = """
    #############################################################
    #                                                           #
    #                 Network Scanner Tool                      #
    #                                                           #
    #           FOR TESTING SECURITY TOOLS ONLY                 #
    #                                                           #
    #############################################################
    """
    print(banner)
    print("This script performs network scanning operations")
    print("FOR TESTING SECURITY TOOLS ONLY - Use responsibly\n")

def scan_port(target_ip, port):
    """Scan a single port on the target IP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            service = get_service_name(port)
            print(f"Port {port} ({service}): Open")
            return True
        sock.close()
    except socket.error:
        pass
    return False

def get_service_name(port):
    """Get the service name for a port number"""
    common_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        115: "SFTP",
        135: "RPC",
        139: "NetBIOS",
        143: "IMAP",
        194: "IRC",
        443: "HTTPS",
        445: "SMB",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP Proxy"
    }
    return common_ports.get(port, "Unknown")

def scan_target(target_ip, port_range=None, scan_type="basic"):
    """Scan a target IP address"""
    print(f"Starting scan of {target_ip} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Scan type: {scan_type}")
    print("-" * 60)
    
    open_ports = []
    
    if port_range:
        start_port, end_port = port_range
    else:
        if scan_type == "basic":
            # Common ports for basic scan
            ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 8080]
        elif scan_type == "full":
            # Full port range for comprehensive scan
            ports_to_scan = range(1, 1025)
        elif scan_type == "stealth":
            # Random selection of ports for stealth scan
            ports_to_scan = sorted(random.sample(range(1, 1025), 20))
        else:
            ports_to_scan = range(1, 100)  # Default range
    
        start_port = min(ports_to_scan)
        end_port = max(ports_to_scan)
    
    print(f"Scanning ports {start_port}-{end_port}...")
    
    # Simulate scanning
    total_ports = end_port - start_port + 1
    scanned = 0
    
    for port in range(start_port, end_port + 1):
        # Update progress
        scanned += 1
        if scanned % 100 == 0 or scanned == total_ports:
            progress = (scanned / total_ports) * 100
            sys.stdout.write(f"\rProgress: {progress:.1f}% ({scanned}/{total_ports})")
            sys.stdout.flush()
        
        # Scan the port
        if scan_port(target_ip, port):
            open_ports.append(port)
        
        # Add delay for stealth scan
        if scan_type == "stealth":
            time.sleep(random.uniform(0.1, 0.5))
    
    print("\n")
    print("-" * 60)
    print(f"Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Found {len(open_ports)} open ports on {target_ip}")
    
    return open_ports

def fingerprint_services(target_ip, open_ports):
    """Attempt to fingerprint services on open ports"""
    print("\nAttempting to fingerprint services...")
    print("-" * 60)
    
    for port in open_ports:
        service = get_service_name(port)
        print(f"Port {port} ({service}):")
        
        # This is just a simulation - no actual fingerprinting is performed
        if service == "HTTP" or service == "HTTPS":
            print(f"  - Web server detected")
            print(f"  - Server: Apache/2.4.41 (Unix)")
            print(f"  - Technologies: PHP/7.4.3, MySQL/5.7.29")
        elif service == "SSH":
            print(f"  - SSH server detected")
            print(f"  - Version: OpenSSH_8.2p1 Ubuntu-4ubuntu0.1")
        elif service == "FTP":
            print(f"  - FTP server detected")
            print(f"  - Version: vsftpd 3.0.3")
        elif service == "SMB":
            print(f"  - SMB server detected")
            print(f"  - Version: Samba 4.11.6-Ubuntu")
        else:
            print(f"  - Service fingerprinting not available")

def check_vulnerabilities(target_ip, open_ports):
    """Check for known vulnerabilities (simulation)"""
    print("\nChecking for known vulnerabilities...")
    print("-" * 60)
    
    vulnerabilities = {
        21: ["FTP Anonymous Login", "ProFTPD 1.3.5 Remote Command Execution"],
        22: ["OpenSSH 7.2p1 Username Enumeration"],
        80: ["Apache 2.4.49 Path Traversal", "Log4j Remote Code Execution"],
        443: ["Heartbleed", "POODLE SSL Vulnerability"],
        445: ["EternalBlue SMB Vulnerability", "SambaCry"],
        3306: ["MySQL Weak Password Policy", "MySQL UDF Dynamic Library"],
        3389: ["BlueKeep RDP Vulnerability"]
    }
    
    found_vulnerabilities = False
    
    for port in open_ports:
        if port in vulnerabilities:
            found_vulnerabilities = True
            service = get_service_name(port)
            print(f"Port {port} ({service}) potential vulnerabilities:")
            for vuln in vulnerabilities[port]:
                print(f"  - {vuln}")
    
    if not found_vulnerabilities:
        print("No known vulnerabilities found for the open ports")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Network Scanner Tool (FOR TESTING ONLY)")
    parser.add_argument("target", help="Target IP address to scan")
    parser.add_argument("-p", "--ports", help="Port range to scan (e.g., 1-100)", default=None)
    parser.add_argument("-t", "--type", help="Scan type (basic, full, stealth)", default="basic")
    parser.add_argument("-f", "--fingerprint", help="Fingerprint services on open ports", action="store_true")
    parser.add_argument("-v", "--vulnerabilities", help="Check for known vulnerabilities", action="store_true")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Parse port range if provided
    port_range = None
    if args.ports:
        try:
            if "-" in args.ports:
                start, end = args.ports.split("-")
                port_range = (int(start), int(end))
            else:
                port = int(args.ports)
                port_range = (port, port)
        except ValueError:
            print("Invalid port range. Using default.")
    
    # Scan target
    open_ports = scan_target(args.target, port_range, args.type)
    
    # Fingerprint services if requested
    if args.fingerprint:
        fingerprint_services(args.target, open_ports)
    
    # Check for vulnerabilities if requested
    if args.vulnerabilities:
        check_vulnerabilities(args.target, open_ports)
    
    print("\nScan complete. This was a test script for security tools.")

if __name__ == "__main__":
    main()
