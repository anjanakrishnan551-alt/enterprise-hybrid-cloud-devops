
import platform
import subprocess


def check_server(host):
    count_flag = "-n" if platform.system() == "Windows" else "-c"

    try:
        result = subprocess.run(
            ["ping", count_flag, "1", host],
            capture_output=True,
            text=True,
            timeout=5
        )

        return result.returncode == 0

    except (subprocess.TimeoutExpired, OSError):
        return False


if __name__ == "__main__":
    print("Checking local computer...")

    if check_server("127.0.0.1"):
        print("Server Status: REACHABLE")
    else:
        print("Server Status: UNREACHABLE")
