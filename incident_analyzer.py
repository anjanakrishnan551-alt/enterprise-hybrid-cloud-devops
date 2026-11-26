
import json
from pathlib import Path


def get_incident_analysis(incident):
    incident_type = incident.get("incident_type", "")
    resource = incident.get("resource", "")

    if incident_type == "CONNECTIVITY_FAILURE":
        problem = "Network connectivity failure"
        recommended_action = "Check server, network and firewall"

    elif resource == "CPU":
        problem = "High CPU usage"
        recommended_action = "Investigate CPU-intensive processes"

    else:
        problem = "Unknown incident type"
        recommended_action = "Review incident details"

    result = {
        "hostname": incident.get("hostname", "Unknown"),
        "problem": problem,
        "severity": incident.get("severity", "UNKNOWN"),
        "recommended_action": recommended_action
    }

    return result



def analyze_incident(incident):
    incident_type = incident.get("incident_type", "")

    print("\n========== INCIDENT ANALYSIS ==========")
    print("Server:", incident.get("hostname", "Unknown"))

    if incident_type == "CONNECTIVITY_FAILURE":
        print("Problem: Network connectivity failure")

        print("\nPossible causes:")
        print("- Server may be offline")
        print("- Firewall may be blocking ICMP")
        print("- Network configuration issue")

        print("\nRecommended checks:")
        print("- Verify the server is running")
        print("- Check the IP address and network")
        print("- Review firewall rules")

    elif incident.get("resource") == "CPU":
        print("Problem: High CPU usage")

        print("\nPossible causes:")
        print("- A process may be using excessive CPU")
        print("- Too many applications may be running")
        print("- An application may be stuck in a loop")

        print("\nRecommended checks:")
        print("- Check CPU-intensive processes")
        print("- Review application logs")
        print("- Investigate unexpected CPU spikes")

    else:
        print("Problem: Unknown incident type")
        print("Recommended check: Review incident details")


def main():
    log_file = Path(__file__).resolve().parent / "reports" / "incidents.jsonl"

    if not log_file.exists():
        print("No incident history found.")
        return

    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                incident = json.loads(line)
                analyze_incident(incident)


if __name__ == "__main__":
    main()
