
import platform
import socket
import psutil

print("===================================")
print(" ENTERPRISE INFRASTRUCTURE MONITOR")
print("===================================")

hostname = socket.gethostname()
operating_system = platform.system()

# Collect system performance metrics
cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage("C:\\").percent

# Display system information
print("Computer Name:", hostname)
print("Operating System:", operating_system)
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
