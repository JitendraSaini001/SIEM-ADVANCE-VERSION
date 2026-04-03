"""
SIEM main entry point.
Run: python main.py
"""
import os
import time
import threading
from collector.collector import start_collector
from dashboard.app       import app

LOG_FILES = [
    "logs/auth.log",
    "logs/access.log"
]

def create_log_files():
    """Create empty log files if they don't exist."""
    os.makedirs("logs", exist_ok=True)
    for f in LOG_FILES:
        if not os.path.exists(f):
            open(f, "w").close()
            print(f"[Setup] Created {f}")

if __name__ == "__main__":
    print("=" * 50)
    print("  SIEM System Starting...")
    print("=" * 50)

    create_log_files()

    # Start log collectors in background threads
    threads = start_collector(LOG_FILES)
    print(f"[Main] {len(threads)} collector(s) running.")

    print("[Main] Dashboard at http://localhost:5000")
    print("[Main] Run simulator: python -m simulator.attack_simulator")

    # Start Flask dashboard (blocking)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)