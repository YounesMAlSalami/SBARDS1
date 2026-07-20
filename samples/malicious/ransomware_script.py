#!/usr/bin/env python3
# Malicious ransomware-like script (FOR TESTING ONLY - DOES NOT ACTUALLY ENCRYPT FILES)

import os
import sys
import random
import string
import platform
import socket
import requests
import base64
import subprocess
import time

# Command and control server (fake)
C2_SERVER = "http://malicious-ransomware.com/report"

# Bitcoin wallet for ransom payment (fake)
BITCOIN_WALLET = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# Ransom amount
RANSOM_AMOUNT = 0.5  # BTC

def generate_encryption_key():
    """Generate a random encryption key"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

def get_system_info():
    """Collect system information"""
    info = {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "username": os.getlogin(),
        "ip_address": socket.gethostbyname(socket.gethostname())
    }
    return info

def scan_for_files():
    """Scan for files to encrypt (simulation only)"""
    target_extensions = [
        # Documents
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".csv",
        # Images
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        # Audio/Video
        ".mp3", ".wav", ".mp4", ".avi", ".mkv",
        # Archives
        ".zip", ".rar", ".7z",
        # Other
        ".sql", ".json", ".xml"
    ]
    
    # This is a simulation - we're not actually scanning files
    print("[*] Scanning for files to encrypt...")
    time.sleep(1)
    print("[+] Found 1,523 files that would be encrypted")
    
    return target_extensions

def simulate_encryption():
    """Simulate encryption process (doesn't actually encrypt anything)"""
    print("[*] Starting encryption process...")
    
    # Generate fake encryption key
    key = generate_encryption_key()
    print(f"[+] Generated encryption key: {key}")
    
    # Simulate encryption progress
    total_files = 1523
    for i in range(1, 11):
        files_done = int(total_files * (i / 10))
        print(f"[*] Encrypted {files_done}/{total_files} files ({i*10}%)")
        time.sleep(0.5)
    
    print("[+] Encryption complete!")
    return key

def send_key_to_c2(key, system_info):
    """Simulate sending the key to C2 server"""
    print(f"[*] Sending encryption key to C2 server: {C2_SERVER}")
    
    # In a real ransomware, this would send the key to the attacker
    # This is just a simulation
    try:
        print(f"[+] Successfully sent key and system info to C2 server")
        print(f"[+] System info collected: {system_info}")
    except:
        print("[-] Failed to contact C2 server")

def display_ransom_note():
    """Display the ransom note"""
    ransom_note = f"""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!                                                                !!
    !!                    YOUR FILES ARE ENCRYPTED                    !!
    !!                                                                !!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    All your documents, photos, videos, and other important files have been
    encrypted with military-grade encryption.
    
    To decrypt your files, you need to pay {RANSOM_AMOUNT} Bitcoin to the following wallet:
    
    {BITCOIN_WALLET}
    
    After payment, contact us at decrypt@malicious-ransomware.com with your
    unique ID: {generate_encryption_key()}
    
    YOU HAVE 72 HOURS TO PAY. AFTER THAT, THE PRICE WILL DOUBLE.
    IF YOU DON'T PAY WITHIN A WEEK, YOUR FILES WILL BE PERMANENTLY DELETED.
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    
    print(ransom_note)
    
    # In a real ransomware, this would create ransom note files
    # This is just a simulation

def main():
    """Main function"""
    print("MALICIOUS RANSOMWARE SIMULATION STARTING")
    print("THIS IS A SIMULATION FOR TESTING SECURITY TOOLS")
    print("NO ACTUAL ENCRYPTION OR DAMAGE WILL OCCUR")
    print("-" * 60)
    
    # Get system information
    system_info = get_system_info()
    
    # Scan for files
    target_extensions = scan_for_files()
    
    # Simulate encryption
    key = simulate_encryption()
    
    # Send key to C2 server
    send_key_to_c2(key, system_info)
    
    # Display ransom note
    display_ransom_note()
    
    print("-" * 60)
    print("SIMULATION COMPLETE")
    print("THIS WAS A TEST - NO FILES WERE HARMED")

if __name__ == "__main__":
    main()
