#!/usr/bin/env python3
# Malicious cryptocurrency miner (FOR TESTING ONLY - DOES NOT ACTUALLY MINE)
# This is a simulated malicious Python script for testing security tools

import os
import sys
import platform
import socket
import random
import string
import time
import threading
import subprocess
import json
import base64
from datetime import datetime

# Banner
print("""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║             CRYPTOCURRENCY MINER SIMULATION           ║
║                                                       ║
║           FOR TESTING SECURITY TOOLS ONLY             ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
""")

print("This is a simulated cryptocurrency miner for testing security tools.")
print("No actual mining or malicious actions will be performed.")
print("-" * 60)

# Configuration (would be obfuscated in a real malware)
CONFIG = {
    "pool_url": "stratum+tcp://xmr-pool.malicious-miner.com:3333",
    "wallet_address": "44AFFq5kSiGBoZ4NMDwYtN18obc8AemS33DBLWs3H7otXft3XjrpDtQGv7SqSsaBYBb98uNbr2VBBEt7f2wfn3RVGQBEP3A",
    "worker_id": socket.gethostname().lower(),
    "pool_password": "x",
    "cpu_usage": 80,  # Percentage of CPU to use
    "stealth_mode": True,
    "persistence": True,
    "update_url": "http://malicious-miner.com/updates/miner.py",
    "c2_server": "http://malicious-miner.com/report",
    "startup_delay": 300,  # 5 minutes
    "mining_duration": 600,  # 10 minutes
    "idle_threshold": 180,  # 3 minutes
    "process_name": "system_service",
    "process_blacklist": [
        "taskmgr.exe", "procexp.exe", "procexp64.exe", "procmon.exe", 
        "procmon64.exe", "wireshark.exe", "fiddler.exe", "tcpview.exe",
        "autoruns.exe", "autoruns64.exe", "filemon.exe", "regmon.exe",
        "processhacker.exe", "processhacker2.exe", "processmonitor.exe",
        "perfmon.exe", "mmc.exe", "resmon.exe", "netstat.exe", "netmon.exe"
    ]
}

# Persistence mechanisms (would be implemented in a real malware)
def establish_persistence():
    """Establish persistence to survive reboots"""
    print("[*] Simulating persistence establishment...")
    
    if CONFIG["persistence"]:
        system = platform.system()
        
        if system == "Windows":
            print("[+] Would add registry key: HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run")
            print("[+] Would create scheduled task: System Service")
            print("[+] Would create service: SystemManager")
            
        elif system == "Linux":
            print("[+] Would add to crontab: @reboot python3 " + os.path.abspath(__file__))
            print("[+] Would create systemd service: system-manager.service")
            print("[+] Would add to .bashrc and .profile")
            
        elif system == "Darwin":  # macOS
            print("[+] Would create LaunchAgent: com.system.manager.plist")
            print("[+] Would add to login items")
            
        print("[+] Persistence established (simulated)")
    else:
        print("[-] Persistence disabled in configuration")

# Anti-analysis techniques (would be implemented in a real malware)
def anti_analysis():
    """Implement anti-analysis techniques"""
    print("[*] Checking for analysis tools...")
    
    # Check for debugging
    if sys.gettrace() is not None:
        print("[-] Debugger detected, would exit")
        return False
    
    # Check for virtualization (simplified)
    if platform.system() == "Windows":
        vm_signs = [
            "VMware",
            "VirtualBox",
            "QEMU",
            "Xen",
            "KVM",
            "Parallels"
        ]
        
        # This would check for VM artifacts in a real malware
        print("[+] Checking for virtual machine artifacts...")
        for sign in vm_signs:
            if sign.lower() in socket.gethostname().lower():
                print(f"[-] Possible VM detected: {sign}, would exit")
                return False
    
    # Check for analysis tools running
    if platform.system() == "Windows":
        print("[+] Checking for analysis tools...")
        # In a real malware, this would check running processes
        
    print("[+] No analysis tools detected (simulated)")
    return True

# System information gathering
def gather_system_info():
    """Gather system information"""
    print("[*] Gathering system information...")
    
    info = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "username": os.getlogin(),
        "language": os.getenv("LANG") or os.getenv("LANGUAGE") or "unknown",
        "timezone": time.tzname,
        "datetime": datetime.now().isoformat()
    }
    
    # In a real malware, this would gather more detailed information
    
    print("[+] System information gathered")
    return info

# Process hiding (would be implemented in a real malware)
def hide_process():
    """Hide the mining process"""
    print("[*] Simulating process hiding...")
    
    if CONFIG["stealth_mode"]:
        system = platform.system()
        
        if system == "Windows":
            print("[+] Would use WinAPI to hide process")
            print("[+] Would rename process to: " + CONFIG["process_name"])
            
        elif system == "Linux":
            print("[+] Would use LD_PRELOAD to hide from ps and top")
            print("[+] Would rename process to: " + CONFIG["process_name"])
            
        elif system == "Darwin":  # macOS
            print("[+] Would use dynamic library injection to hide process")
            print("[+] Would rename process to: " + CONFIG["process_name"])
            
        print("[+] Process hidden (simulated)")
    else:
        print("[-] Stealth mode disabled in configuration")

# Mining simulation
def simulate_mining():
    """Simulate cryptocurrency mining"""
    print("[*] Starting mining simulation...")
    
    # Connect to pool
    print(f"[+] Would connect to pool: {CONFIG['pool_url']}")
    print(f"[+] Using wallet: {CONFIG['wallet_address']}")
    print(f"[+] Worker ID: {CONFIG['worker_id']}")
    
    # Start mining threads
    cpu_count = os.cpu_count()
    thread_count = max(1, int(cpu_count * CONFIG["cpu_usage"] / 100))
    print(f"[+] System has {cpu_count} CPU cores")
    print(f"[+] Would start {thread_count} mining threads")
    
    # Simulate mining for a period
    start_time = time.time()
    hashes = 0
    accepted_shares = 0
    rejected_shares = 0
    
    try:
        while time.time() - start_time < CONFIG["mining_duration"]:
            # Simulate mining activity
            time.sleep(1)
            current_hashes = random.randint(1500, 3000) * thread_count
            hashes += current_hashes
            
            # Simulate finding shares
            if random.random() < 0.1:  # 10% chance of finding a share
                if random.random() < 0.95:  # 95% chance of accepted share
                    accepted_shares += 1
                    print(f"[+] Share accepted: {accepted_shares} (simulated)")
                else:
                    rejected_shares += 1
                    print(f"[-] Share rejected: {rejected_shares} (simulated)")
            
            # Print status every 10 seconds
            elapsed = time.time() - start_time
            if int(elapsed) % 10 == 0:
                hashrate = hashes / elapsed
                print(f"[*] Mining at {hashrate:.2f} H/s, {accepted_shares} accepted shares (simulated)")
    
    except KeyboardInterrupt:
        print("\n[!] Mining interrupted")
    
    # Print summary
    elapsed = time.time() - start_time
    hashrate = hashes / elapsed
    print("\n[+] Mining simulation completed")
    print(f"[+] Elapsed time: {elapsed:.2f} seconds")
    print(f"[+] Average hashrate: {hashrate:.2f} H/s")
    print(f"[+] Accepted shares: {accepted_shares}")
    print(f"[+] Rejected shares: {rejected_shares}")
    
    # Calculate simulated earnings
    xmr_per_day = (hashrate * 86400) / 2_000_000_000 * 4.0  # Very rough estimate
    print(f"[+] Estimated earnings: {xmr_per_day:.6f} XMR per day (simulated)")
    
    return {
        "duration": elapsed,
        "hashrate": hashrate,
        "accepted_shares": accepted_shares,
        "rejected_shares": rejected_shares,
        "estimated_daily_xmr": xmr_per_day
    }

# Command and control communication (would be implemented in a real malware)
def report_to_c2(system_info, mining_stats):
    """Report to command and control server"""
    print("[*] Simulating C2 communication...")
    
    data = {
        "system_info": system_info,
        "mining_stats": mining_stats,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"[+] Would send data to C2 server: {CONFIG['c2_server']}")
    print(f"[+] Data: {json.dumps(data, indent=2)}")
    print("[+] C2 communication completed (simulated)")

# Main function
def main():
    """Main function"""
    print("[*] Starting cryptocurrency miner simulation...")
    
    # Implement startup delay
    if CONFIG["startup_delay"] > 0:
        print(f"[*] Startup delay: {CONFIG['startup_delay']} seconds (simulated)")
        # In a real malware, this would actually sleep
    
    # Check for analysis tools
    if not anti_analysis():
        print("[!] Analysis environment detected, exiting")
        return
    
    # Gather system information
    system_info = gather_system_info()
    
    # Establish persistence
    establish_persistence()
    
    # Hide process
    hide_process()
    
    # Start mining
    mining_stats = simulate_mining()
    
    # Report to C2
    report_to_c2(system_info, mining_stats)
    
    print("[+] Simulation completed")
    print("-" * 60)
    print("This was a simulation for testing security tools.")
    print("No actual mining or malicious actions were performed.")

if __name__ == "__main__":
    main()
