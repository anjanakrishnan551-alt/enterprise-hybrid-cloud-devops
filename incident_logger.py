
import json
from datetime import datetime
from pathlib import Path
from alert_manager import send_alert


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
    send_alert(incident)

# Record network connectivity failures
def log_connectivity_failure(hostname, host):
    incident = {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "hostname": hostname,
        "host": host,
        "incident_type": "CONNECTIVITY_FAILURE",
        "severity": "WARNING",
        "message": "Server did not respond to ping"
    }

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    log_file = reports_folder / "incidents.jsonl"

    with log_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(incident) + "\n")

    print("Connectivity incident recorded:", hostname)
    send_alert(incident)

