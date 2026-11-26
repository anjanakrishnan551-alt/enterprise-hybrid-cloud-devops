
import subprocess


# Connect to Linux through SSH and get its hostname

def run_ssh_command(command):
    """Execute a Linux command through SSH."""
    try:
        result = subprocess.run(
            [
                "ssh",
                "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=5",
                "anjana@127.0.0.1",
                command
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("SSH command timed out") from error
    except OSError as error:
        raise RuntimeError(f"Could not start SSH: {error}") from error

    if result.returncode != 0:
        raise RuntimeError(
            f"SSH command failed: {result.stderr.strip()}"
        )

    return result.stdout.strip()


def get_remote_hostname():
    result = subprocess.run(
        [
            "ssh",
            "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=5",
            "anjana@127.0.0.1",
            "hostname"
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode != 0:
        raise RuntimeError("SSH connection failed")

    return result.stdout.strip()


# Connect to Linux through SSH and collect memory information
def get_remote_memory():
    result = subprocess.run(
        [
            "ssh",
            "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=5",
            "anjana@127.0.0.1",
            "free", "-h"
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode != 0:
        raise RuntimeError("Failed to collect Linux memory information")

    return result.stdout.strip()



def get_remote_cpu():
    result = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
         "anjana@127.0.0.1", "top -bn2 -d 1 | grep 'Cpu(s)' | tail -1"],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        raise RuntimeError("Failed to collect CPU information")
    return result.stdout.strip()


def get_remote_disk():
    result = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
         "anjana@127.0.0.1", "df -h /"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        raise RuntimeError("Failed to collect disk information")
    return result.stdout.strip()


# Run the monitoring program
if __name__ == "__main__":
    hostname = get_remote_hostname()
    print("Remote Linux Server:", hostname)

    memory = get_remote_memory()
    print("\nRemote Linux Memory:")
    print(memory)


    print("\nRemote Linux CPU:")
    print(get_remote_cpu())

    print("\nRemote Linux Disk:")
    print(get_remote_disk())
