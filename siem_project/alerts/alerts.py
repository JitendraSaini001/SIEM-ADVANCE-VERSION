from datetime import datetime
from storage.storage import store_alert

SEVERITY_COLORS = {
    "CRITICAL": "\033[91m",  # red
    "HIGH":     "\033[93m",  # yellow
    "MEDIUM":   "\033[96m",  # cyan
    "LOW":      "\033[92m",  # green
}
RESET = "\033[0m"

def dispatch_alert(alert: dict):
    """
    Handle a triggered alert:
    1. Print to console (color-coded)
    2. Store in MongoDB
    (extend here: send email, Slack webhook, etc.)
    """
    alert["created_at"] = datetime.utcnow().isoformat()

    severity = alert.get("severity", "LOW")
    color    = SEVERITY_COLORS.get(severity, "")

    print(f"\n{color}[ALERT][{severity}] {alert['message']}{RESET}")
    print(f"  IP: {alert.get('source_ip')}  "
          f"Type: {alert.get('alert_type')}  "
          f"Time: {alert['created_at']}")

    # Remove nested event dict before storing (keep it clean)
    alert_to_store = {k: v for k, v in alert.items() if k != "event"}
    store_alert(alert_to_store)