
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

    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            incident = json.loads(line)
            total += 1

            if incident.get("resource") == "CPU":
                cpu_incidents += 1

            if incident.get("incident_type") == "CONNECTIVITY_FAILURE":
                connectivity_incidents += 1

    print("Total incidents:", total)
    print("CPU incidents:", cpu_incidents)
    print("Connectivity incidents:", connectivity_incidents)
    print("========================================")


if __name__ == "__main__":
    show_dashboard()
