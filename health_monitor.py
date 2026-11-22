
import platform
import socket
import psutil
from datetime import datetime

print("===================================")
print(" ENTERPRISE INFRASTRUCTURE MONITOR")
print("===================================")

hostname = socket.gethostname()

operating_system = platform.system()
timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
# Collect system performance metrics
cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage("C:\\").percent

# Display system information
print("Computer Name:", hostname)
print("Operating System:", operating_system)
print("Check Time:", timestamp)
print("CPU Usage:", cpu_usage, "%")
print("Memory Usage:", memory_usage, "%")
print("Disk Usage:", disk_usage, "%")


print("\n========== HEALTH STATUS ==========")

if cpu_usage >= 80:
    print("WARNING: High CPU usage!")
else:
    print("CPU Status: HEALTHY")

if memory_usage >= 80:
    print("WARNING: High memory usage!")
else:
    print("Memory Status: HEALTHY")

if disk_usage >= 80:
    print("WARNING: High disk usage!")
else:
    print("Disk Status: HEALTHY")



from pathlib import Path

# Create a folder for monitoring reports
reports_folder = Path("reports")
reports_folder.mkdir(exist_ok=True)

# Generate a unique filename using the current time
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
"""

# Save the report
report_path.write_text(report, encoding="utf-8")

print("\nReport saved to:", report_path)

