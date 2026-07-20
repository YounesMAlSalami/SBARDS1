#!/bin/bash
# This is a shell script that would normally be executable
# For testing permission scanning

echo "This is a shell script that would normally be executable"
echo "It is used to test permission scanning in security tools"

# Print system information
echo "System Information:"
echo "-------------------"
echo "Hostname: $(hostname)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "OS: $(uname -o)"

# List running processes
echo "Running Processes:"
echo "-----------------"
ps aux | head -5

# List network connections
echo "Network Connections:"
echo "------------------"
netstat -tuln | head -5

# List users
echo "Users:"
echo "-----"
cat /etc/passwd | head -5

echo "This script is for testing permission scanning only"
echo "No actual system changes are made"
