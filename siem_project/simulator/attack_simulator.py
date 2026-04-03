"""
Generates realistic fake attack logs into a log file.
Run this in a separate terminal to simulate attacks.
"""
import time
import random
import argparse
from datetime import datetime

LOG_FILE = "logs/auth.log"

USERNAMES    = ["root", "admin", "ubuntu", "pi", "user", "test"]
IPS_NORMAL   = ["192.168.1.10", "192.168.1.20", "10.0.0.5"]
IPS_ATTACK   = ["45.33.32.156", "192.241.186.56", "185.220.101.45"]

def ssh_failed(ip, user):
    ts = datetime.now().strftime("%b %d %H:%M:%S")
    return (f"{ts} ubuntu-server sshd[1234]: "
            f"Failed password for {user} from {ip} port 22 ssh2\n")

def ssh_success(ip, user):
    ts = datetime.now().strftime("%b %d %H:%M:%S")
    return (f"{ts} ubuntu-server sshd[1234]: "
            f"Accepted password for {user} from {ip} port 22 ssh2\n")

def simulate_brute_force(ip, count=10):
    print(f"[Simulator] Brute force from {ip}")
    for _ in range(count):
        user = random.choice(USERNAMES)
        with open(LOG_FILE, "a") as f:
            f.write(ssh_failed(ip, user))
        time.sleep(0.3)

def simulate_normal_traffic(count=5):
    for _ in range(count):
        ip   = random.choice(IPS_NORMAL)
        user = random.choice(USERNAMES)
        with open(LOG_FILE, "a") as f:
            if random.random() > 0.3:
                f.write(ssh_success(ip, user))
            else:
                f.write(ssh_failed(ip, user))
        time.sleep(1)

def simulate_web_attack(log_file="logs/access.log"):
    """Write SQL injection and XSS attempts to a web log."""
    attack_paths = [
        "/' OR '1'='1",
        "/search?q=<script>alert(1)</script>",
        "/admin?id=1 UNION SELECT * FROM users--",
        "/login?user=admin'--",
    ]
    attacker_ip = random.choice(IPS_ATTACK)
    ts = datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")
    for path in attack_paths:
        line = (f'{attacker_ip} - - [{ts}] "GET {path} HTTP/1.1" '
                f'400 512\n')
        with open(log_file, "a") as f:
            f.write(line)
        print(f"[Simulator] Web attack: {path[:50]}")
        time.sleep(0.5)

if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)

    print("=== SIEM Attack Simulator ===")
    print("Generating attacks in 3s...")
    time.sleep(3)

    while True:
        choice = random.random()
        if choice < 0.3:
            simulate_brute_force(random.choice(IPS_ATTACK))
        elif choice < 0.6:
            simulate_web_attack()
        else:
            simulate_normal_traffic()
        time.sleep(random.uniform(2, 6))