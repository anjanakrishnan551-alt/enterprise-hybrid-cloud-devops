
import json
from pathlib import Path


def show_dashboard():
    log_file = Path(__file__).resolve().parent / "reports" / "incidents.jsonl"

    print("========== INCIDENT DASHBOARD ==========")

    if not log_file.exists():
        print("No incidents recorded yet.")
        return

    total = 0
    cpu_incidents = 0
    connectivity_incidents = 0
    warning_incidents = 0
    critical_incidents = 0
    recent_incidents = []

    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            incident = json.loads(line)
            total += 1
            recent_incidents.append(incident)

            if incident.get("resource") == "CPU":
                cpu_incidents += 1

            if incident.get("incident_type") == "CONNECTIVITY_FAILURE":
                connectivity_incidents += 1

            if incident.get("severity") == "WARNING":
                warning_incidents += 1

            if incident.get("severity") == "CRITICAL":
                critical_incidents += 1

    print("Total incidents:", total)
    print("CPU incidents:", cpu_incidents)
    print("Connectivity incidents:", connectivity_incidents)

    print("\n========== SEVERITY SUMMARY ==========")
    print("Warnings:", warning_incidents)
    print("Critical:", critical_incidents)
    print("========================================")

    print("\n========== RECENT INCIDENTS ==========")

    for incident in recent_incidents[-3:][::-1]:
        print("Time:", incident.get("timestamp", "Unknown"))
        print("Server:", incident.get("hostname", "Unknown"))
        print("Severity:", incident.get("severity", "Unknown"))
        print("Type:", incident.get("incident_type", incident.get("resource", "Unknown")))
        print("--------------------------------------")



if __name__ == "__main__":
    show_dashboard()
