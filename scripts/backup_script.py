import paramiko
import time
from datetime import datetime
import os
import socket

routers = [
    {"hostname": "R1", "ip": "192.168.1.1"},
    {"hostname": "R2", "ip": "192.168.1.2"},
    {"hostname": "R3", "ip": "192.168.1.3"}
]

username = "admin"
password = "Admin123"
current_date = datetime.now().strftime("%Y-%m-%d")

if not os.path.exists("router_backups"):
    os.makedirs("router_backups")

print("Starting Week 5 Fault-Tolerant Automation Engine...")
print("-" * 60)

for router in routers:
    print(f"Initializing connection loop for {router['hostname']} ({router['ip']})...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(router['ip'], username=username, password=password, timeout=5)
        print(f"✅ Secure SSH Channel Established to {router['hostname']}")
        
        channel = ssh.invoke_shell()
        time.sleep(1)
        
        channel.send("terminal length 0\n")
        time.sleep(1)
        
        channel.send("show running-config\n")
        print(f"📥 Streaming configuration data from {router['hostname']}...")
        time.sleep(3)
        
        output = channel.recv(65535).decode('utf-8')
        
        filename = f"router_backups/{router['hostname']}_{current_date}.txt"
        with open(filename, "w") as backup_file:
            backup_file.write(output)
        print(f"💾 Backup saved successfully: {filename}")
        
    except socket.timeout:
        print(f"❌ CRITICAL FAULT: {router['hostname']} connection timed out. Link is down.")
    except paramiko.AuthenticationException:
        print(f"❌ SECURITY FAULT: Authentication failed on {router['hostname']}. Check credentials.")
    except paramiko.SSHException as ssh_err:
        print(f"❌ TRANSPORT FAULT: SSH negotiation failed on {router['hostname']}: {ssh_err}")
    except Exception as general_err:
        print(f"❌ UNKNOWN FAULT on {router['hostname']}: {general_err}")
        
    finally:
        ssh.close()
        print("-" * 60)

print("Week 5 resilience execution routine complete.")