
import json
from pathlib import Path
from connectivity_check import check_server

# Locate our server configuration file
config_file = Path(__file__).resolve().parent / "servers.json"

# Read the JSON configuration
with config_file.open("r", encoding="utf-8") as file:
    config = json.load(file)

# Get the list of servers
servers = config["servers"]

# Select only servers enabled for monitoring
enabled_servers = []

for server in servers:
    if server["enabled"]:
        enabled_servers.append(server)

print("Total configured servers:", len(servers))
print("Enabled servers:", len(enabled_servers))


print("========== SERVER INVENTORY ==========")

for server in enabled_servers:
    print("Name:", server["name"])
    print("IP Address:", server["host"])
    print("Operating System:", server["type"])
    print("Environment:", server["environment"])
    print("Enabled:", server["enabled"])
    print("--------------------------------------")


print("\n========== CONNECTIVITY STATUS ==========")

for server in enabled_servers:
    server_name = server["name"]
    server_ip = server["host"]

    print("Checking:", server_name)

    if check_server(server_ip):
        print("Connectivity: REACHABLE")
    else:
        print("Connectivity: UNREACHABLE")

    print("--------------------------------------")

