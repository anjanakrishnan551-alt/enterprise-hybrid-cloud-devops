
def send_alert(incident):
    hostname = incident.get("hostname", "Unknown")
    severity = incident.get("severity", "UNKNOWN")
    incident_type = incident.get(
        "incident_type",
        incident.get("resource", "Unknown")
    )

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
