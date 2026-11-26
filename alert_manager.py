
import time

# Remember when each alert was last displayed
last_alert_times = {}

# Five-minute cooldown (300 seconds)
ALERT_COOLDOWN = 300

def send_alert(incident):
    hostname = incident.get("hostname", "Unknown")
    severity = incident.get("severity", "UNKNOWN")
    incident_type = incident.get(
        "incident_type",
        incident.get("resource", "Unknown")
    )

    # Create a unique key for this alert
    alert_key = (hostname, incident_type, severity)

    current_time = time.time()

    # Check whether the same alert was recently displayed
    previous_time = last_alert_times.get(alert_key)

    if previous_time is not None:
        if current_time - previous_time < ALERT_COOLDOWN:
            print("Duplicate alert suppressed:", hostname, incident_type)
            return

    # Record the time of this alert
    last_alert_times[alert_key] = current_time


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


if __name__ == "__main__":
    test_incident = {
        "hostname": "TEST-LINUX-SERVER",
        "incident_type": "CONNECTIVITY_FAILURE",
        "severity": "WARNING"
    }

    send_alert(test_incident)
