
import platform
import socket
import psutil
from datetime import datetime
from pathlib import Path
from incident_logger import log_incident


# Reusable function to detect high resource usage
def check_incident(resource, usage):
    if usage >= 80:
        return f"WARNING: High {resource} usage detected ({usage}%)"
    else:
        return f"{resource} Status: HEALTHY"


# Main monitoring program
def main():
    print("===================================")
    print(" ENTERPRISE INFRASTRUCTURE MONITOR")
    print("===================================")

    # Collect computer information
    hostname = socket.gethostname()
    operating_system = platform.system()
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    # Collect system performance metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # Select the correct system drive
    disk_path = "C:\\" if operating_system == "Windows" else "/"
    disk_usage = psutil.disk_usage(disk_path).percent

    # Display monitoring information
    print("Computer Name:", hostname)
    print("Operating System:", operating_system)
    print("Check Time:", timestamp)
    print("CPU Usage:", cpu_usage, "%")
    print("Memory Usage:", memory_usage, "%")
    print("Disk Usage:", disk_usage, "%")

    # Check system health
    cpu_status = check_incident("CPU", cpu_usage)
    memory_status = check_incident("Memory", memory_usage)
    disk_status = check_incident("Disk", disk_usage)


    # Record incidents only when thresholds are exceeded
    if cpu_usage >= 80:
        log_incident(hostname, "CPU", cpu_usage)

    if memory_usage >= 80:
        log_incident(hostname, "Memory", memory_usage)

    if disk_usage >= 80:
        log_incident(hostname, "Disk", disk_usage)


    print("\n========== HEALTH STATUS ==========")
    print(cpu_status)
    print(memory_status)
    print(disk_status)

    # Create reports folder
    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    # Generate report filename
    report_filename = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_folder / f"health_report_{report_filename}.txt"

    # Prepare the report
    report = f"""ENTERPRISE INFRASTRUCTURE HEALTH REPORT
Computer: {hostname}
Operating System: {operating_system}
Check Time: {timestamp}

CPU Usage: {cpu_usage}%
Memory Usage: {memory_usage}%
Disk Usage: {disk_usage}%

HEALTH STATUS
{cpu_status}
{memory_status}
{disk_status}
"""

    # Save the report
    report_path.write_text(report, encoding="utf-8")

    print("\nReport saved to:", report_path)


# Run main() only when this file is executed directly
if __name__ == "__main__":
    main()
