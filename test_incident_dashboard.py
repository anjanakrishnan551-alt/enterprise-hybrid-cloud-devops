
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, call

from incident_dashboard import show_dashboard


class TestIncidentDashboard(unittest.TestCase):

    def test_dashboard_counts_incidents(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            reports_dir = Path(temp_dir) / "reports"
            reports_dir.mkdir()

            log_file = reports_dir / "incidents.jsonl"

            incidents = [
                {"resource": "CPU", "severity": "WARNING"},
                {
                    "incident_type": "CONNECTIVITY_FAILURE",
                    "severity": "WARNING"
                },
                {
                    "incident_type": "CONNECTIVITY_FAILURE",
                    "severity": "CRITICAL"
                }
            ]

            with log_file.open("w", encoding="utf-8") as file:
                for incident in incidents:
                    file.write(json.dumps(incident) + "\n")

            fake_path = str(Path(temp_dir) / "incident_dashboard.py")

            with patch("incident_dashboard.__file__", fake_path):
                with patch("builtins.print") as mock_print:
                    show_dashboard()

            mock_print.assert_any_call("Total incidents:", 3)
            mock_print.assert_any_call("CPU incidents:", 1)
            mock_print.assert_any_call("Connectivity incidents:", 2)
            mock_print.assert_any_call("Warnings:", 2)
            mock_print.assert_any_call("Critical:", 1)

    def test_recent_incidents(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            reports_dir = Path(temp_dir) / "reports"
            reports_dir.mkdir()

            log_file = reports_dir / "incidents.jsonl"

            incidents = [
                {
                    "hostname": f"TEST-SERVER-{number}",
                    "timestamp": f"2026-11-22T10:0{number}:00+00:00",
                    "severity": "WARNING",
                    "incident_type": "CONNECTIVITY_FAILURE"
                }
                for number in range(1, 5)
            ]

            with log_file.open("w", encoding="utf-8") as file:
                for incident in incidents:
                    file.write(json.dumps(incident) + "\n")

            fake_path = str(Path(temp_dir) / "incident_dashboard.py")

            with patch("incident_dashboard.__file__", fake_path):
                with patch("builtins.print") as mock_print:
                    show_dashboard()

            server_names = [
                item.args[1]
                for item in mock_print.call_args_list
                if len(item.args) == 2 and item.args[0] == "Server:"
            ]

            self.assertEqual(
                server_names,
                ["TEST-SERVER-4", "TEST-SERVER-3", "TEST-SERVER-2"]
            )

            mock_print.assert_any_call(
                "Time:", "2026-11-22T10:04:00+00:00"
            )
            mock_print.assert_any_call("Severity:", "WARNING")
            mock_print.assert_any_call("Type:", "CONNECTIVITY_FAILURE")


if __name__ == "__main__":
    unittest.main()
