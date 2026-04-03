import re
from datetime import datetime

# Regex patterns for common log formats
SSH_PATTERN = re.compile(
    r'(?P<timestamp>\w+\s+\d+\s+[\d:]+)\s+\S+\s+sshd.*?'
    r'(?P<status>Failed|Accepted)\s+password\s+for\s+'
    r'(?P<user>\S+)\s+from\s+(?P<source_ip>[\d.]+)'
)

WEB_PATTERN = re.compile(
    r'(?P<source_ip>[\d.]+)\s+-\s+-\s+\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>\w+)\s+(?P<path>\S+)\s+HTTP/[\d.]+"\s+'
    r'(?P<status_code>\d+)\s+(?P<bytes>\d+)'
)

GENERIC_PATTERN = re.compile(
    r'(?P<timestamp>[\d\-T:]+)\s+(?P<level>INFO|WARN|ERROR|CRITICAL)\s+'
    r'(?P<source_ip>[\d.]+)?\s*(?P<message>.*)'
)

def parse_ssh_log(line: str) -> dict | None:
    match = SSH_PATTERN.search(line)
    if match:
        d = match.groupdict()
        d["log_type"] = "ssh"
        d["failed"] = (d["status"] == "Failed")
        d["raw"] = line.strip()
        d["parsed_at"] = datetime.utcnow().isoformat()
        return d
    return None

def parse_web_log(line: str) -> dict | None:
    match = WEB_PATTERN.search(line)
    if match:
        d = match.groupdict()
        d["log_type"] = "web"
        d["status_code"] = int(d["status_code"])
        d["raw"] = line.strip()
        d["parsed_at"] = datetime.utcnow().isoformat()
        return d
    return None

def parse_line(line: str) -> dict | None:
    """Try all parsers, return first match."""
    return (parse_ssh_log(line) or 
            parse_web_log(line) or 
            None)