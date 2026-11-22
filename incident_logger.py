
import json
from datetime import datetime
from pathlib import Path


def log_incident(hostname, resource, usage):
    # Create the incident record
    incident = {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "hostname": hostname,
        "resource": resource,
        "usage_percent": usage,
        "severity": "WARNING",
        "message": f"High {resource} usage detected"
    }

    # Create the reports folder if needed
    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    # Choose where to save incidents
    log_file = reports_folder / "incidents.jsonl"

    # Append the incident as one JSON line
    with log_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(incident) + "\n")

    print("Incident recorded:", resource, usage, "%")
