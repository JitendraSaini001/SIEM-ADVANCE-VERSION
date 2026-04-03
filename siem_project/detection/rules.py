from collections import defaultdict
from datetime import datetime, timedelta

# Track failed logins per IP in memory
failed_logins = defaultdict(list)
port_scan_hits = defaultdict(list)

BRUTE_FORCE_THRESHOLD = 5      # 5 failures in 60 seconds
BRUTE_FORCE_WINDOW    = 60     # seconds
PORT_SCAN_THRESHOLD   = 10     # 10 different ports in 30 seconds
PORT_SCAN_WINDOW      = 30

def check_brute_force(event: dict) -> dict | None:
    """
    Detect brute-force: same IP failing login >= threshold times in window.
    """
    if event.get("log_type") != "ssh" or not event.get("failed"):
        return None

    ip  = event.get("source_ip", "unknown")
    now = datetime.utcnow()

    # Keep only events within the time window
    failed_logins[ip] = [
        t for t in failed_logins[ip]
        if (now - t).seconds < BRUTE_FORCE_WINDOW
    ]
    failed_logins[ip].append(now)

    if len(failed_logins[ip]) >= BRUTE_FORCE_THRESHOLD:
        return {
            "alert_type": "brute_force",
            "source_ip":  ip,
            "severity":   "HIGH",
            "message":    f"Brute force detected from {ip}: "
                          f"{len(failed_logins[ip])} failed logins in "
                          f"{BRUTE_FORCE_WINDOW}s",
            "event":      event
        }
    return None

def check_sql_injection(event: dict) -> dict | None:
    """
    Detect SQL injection patterns in web request paths.
    """
    if event.get("log_type") != "web":
        return None

    path = event.get("path", "")
    sqli_patterns = [
        "' OR '1'='1", "UNION SELECT", "DROP TABLE",
        "--", "xp_cmdshell", "sleep(", "benchmark("
    ]
    path_upper = path.upper()

    for pattern in sqli_patterns:
        if pattern.upper() in path_upper:
            return {
                "alert_type": "sql_injection",
                "source_ip":  event.get("source_ip", "unknown"),
                "severity":   "CRITICAL",
                "message":    f"SQL Injection attempt detected in path: {path}",
                "pattern":    pattern,
                "event":      event
            }
    return None

def check_xss(event: dict) -> dict | None:
    """Detect XSS patterns in web paths."""
    if event.get("log_type") != "web":
        return None

    path = event.get("path", "")
    xss_patterns = ["<script>", "javascript:", "onerror=", "onload=", "alert("]

    for pattern in xss_patterns:
        if pattern.lower() in path.lower():
            return {
                "alert_type": "xss_attempt",
                "source_ip":  event.get("source_ip", "unknown"),
                "severity":   "HIGH",
                "message":    f"XSS attempt detected: {path[:100]}",
                "event":      event
            }
    return None

def run_all_rules(event: dict) -> list[dict]:
    """Run every rule. Return list of triggered alerts."""
    alerts = []
    for check_fn in [check_brute_force, check_sql_injection, check_xss]:
        result = check_fn(event)
        if result:
            alerts.append(result)
    return alerts