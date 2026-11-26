
import json
import time
from pathlib import Path


# Five-minute alert cooldown
ALERT_COOLDOWN = 300

# Remember alert timestamps in memory
last_alert_times = {}

# Location of the persistent history file
ALERT_HISTORY_FILE = (
    Path(__file__).resolve().parent
    / "reports"
    / "alert_history.json"
)


def save_alert_history():
    """Save alert timestamps to a JSON file."""

    ALERT_HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    history = {}

    for alert_key, timestamp in last_alert_times.items():
        hostname, incident_type, severity = alert_key

        key = f"{hostname}|{incident_type}|{severity}"
        history[key] = timestamp

    with ALERT_HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def load_alert_history():
    """Restore previously saved alert timestamps."""

    if not ALERT_HISTORY_FILE.exists():
        return

    with ALERT_HISTORY_FILE.open("r", encoding="utf-8") as file:
        history = json.load(file)

    for key, timestamp in history.items():
        hostname, incident_type, severity = key.split("|", 2)

        alert_key = (hostname, incident_type, severity)
        last_alert_times[alert_key] = timestamp


def send_alert(incident):
    """Display an alert unless it is within its cooldown."""

    hostname = incident.get("hostname", "Unknown")
    severity = incident.get("severity", "UNKNOWN")

    incident_type = incident.get(
        "incident_type",
        incident.get("resource", "Unknown")
    )

    alert_key = (hostname, incident_type, severity)

    # Load previously saved alerts
    load_alert_history()

    current_time = time.time()
    previous_time = last_alert_times.get(alert_key)

    # Suppress duplicate alerts within five minutes
    if previous_time is not None:
        if current_time - previous_time < ALERT_COOLDOWN:
            print(
                "Duplicate alert suppressed:",
                hostname,
                incident_type
            )
            return

    # Display the alert
    print("========== INFRASTRUCTURE ALERT ==========")
    print("Server:", hostname)
    print("Severity:", severity)
    print("Incident:", incident_type)

    if severity == "CRITICAL":
        print("Priority: HIGH")
        print("Action: Immediate investigation recommended")

    elif severity == "WARNING":
        print("Priority: MEDIUM")
        print("Action: Investigation recommended")

    else:
        print("Priority: UNKNOWN")
        print("Action: Review incident details")

    print("==========================================")

    # Remember and save this alert
    last_alert_times[alert_key] = current_time
    save_alert_history()


if __name__ == "__main__":
    test_incident = {
        "hostname": "TEST-LINUX-SERVER",
        "incident_type": "CONNECTIVITY_FAILURE",
        "severity": "WARNING"
    }

    send_alert(test_incident)
