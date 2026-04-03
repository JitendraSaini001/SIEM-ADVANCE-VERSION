import time
import os
from parser.parser    import parse_line
from detection.rules  import run_all_rules
from detection.ml_engine import detector
from alerts.alerts    import dispatch_alert
from storage.storage  import store_event

def tail_file(filepath: str):
    """
    Generator that yields new lines added to a file (like `tail -f`).
    """
    with open(filepath, "r") as f:
        f.seek(0, 2)  # seek to end
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                time.sleep(0.5)

def process_log_file(filepath: str):
    """
    Continuously read a log file, parse each line,
    run detection, and dispatch alerts.
    """
    print(f"[Collector] Monitoring: {filepath}")
    for raw_line in tail_file(filepath):
        event = parse_line(raw_line)
        if not event:
            continue

        # Store raw event
        store_event(event)

        # Rule-based detection
        rule_alerts = run_all_rules(event)
        for alert in rule_alerts:
            dispatch_alert(alert)

        # ML-based detection (web events only)
        if event.get("log_type") == "web":
            detector.add_training_sample(event)
            ml_alert = detector.predict(event)
            if ml_alert:
                dispatch_alert(ml_alert)

def start_collector(log_files: list[str]):
    """Start monitoring multiple log files (simple single-thread version)."""
    import threading
    threads = []
    for f in log_files:
        if os.path.exists(f):
            t = threading.Thread(target=process_log_file, args=(f,), daemon=True)
            t.start()
            threads.append(t)
        else:
            print(f"[Collector] Warning: {f} not found, skipping.")
    return threads