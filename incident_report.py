
import json
from datetime import datetime
from pathlib import Path

from incident_analyzer import get_incident_analysis


def generate_incident_report():
    project_folder = Path(__file__).resolve().parent
    log_file = project_folder / "reports" / "incidents.jsonl"

    if not log_file.exists():
        print("No incident history found.")
        return

    incidents = []

    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                incidents.append(json.loads(line))

    if not incidents:
        print("No incidents available.")
        return

    # Select the last recorded incident
    latest_incident = incidents[-1]

    # Get troubleshooting recommendations
    analysis = get_incident_analysis(latest_incident)

    # Build the report
    report_text = (
        "========== INCIDENT REPORT ==========\n"
        f"Incident time: {latest_incident.get('timestamp', 'Unknown')}\n"
        f"Server: {analysis['hostname']}\n"
        f"Problem: {analysis['problem']}\n"
        f"Severity: {analysis['severity']}\n"
        f"Recommended action: {analysis['recommended_action']}\n"
        "=====================================\n"
    )

    # Display the report
    print(report_text)

    # Create the reports folder if needed
    reports_folder = project_folder / "reports"
    reports_folder.mkdir(exist_ok=True)

    # Generate a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    report_file = reports_folder / f"incident_report_{timestamp}.txt"

    # Save the report
    report_file.write_text(report_text, encoding="utf-8")

    print("Report saved to:", report_file)


if __name__ == "__main__":
    generate_incident_report()
