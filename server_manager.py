
import json
from pathlib import Path

from connectivity_check import check_server
from incident_logger import log_connectivity_failure


# Load server information from JSON
def load_servers():
    config_file = Path(__file__).resolve().parent / "servers.json"

    with config_file.open("r", encoding="utf-8") as file:
        config = json.load(file)

    return config["servers"]


# Check connectivity and log failures
def monitor_server(server):
    server_name = server["name"]
    server_ip = server["host"]

    print("Checking:", server_name)

    if check_server(server_ip):
        print("Connectivity: REACHABLE")
        return True
    else:
        print("Connectivity: UNREACHABLE")
        log_connectivity_failure(server_name, server_ip)
        return False


# Main program
def main():
    servers = load_servers()

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
        monitor_server(server)
        print("--------------------------------------")


if __name__ == "__main__":
    main()
