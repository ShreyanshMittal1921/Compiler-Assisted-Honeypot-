import json
from datetime import datetime

LOG_FILE = "logs.json"

def log_attack(data):
    """Append one attack entry to logs.json."""
    log_entry = {
        "time":  datetime.now().strftime("%H:%M:%S"),   # e.g. 14:32:07
        "date":  datetime.now().strftime("%Y-%m-%d"),   # e.g. 2025-06-01
        "input": str(data)
    }

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

    print(f"[HONEYPOT] Attack logged: {data}")
