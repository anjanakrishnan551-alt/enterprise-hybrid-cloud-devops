
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from incident_dashboard import show_dashboard


class TestIncidentDashboard(unittest.TestCase):

    def test_dashboard_counts_incidents(self):
        with tempfile.TemporaryDirectory() as temp_dir:

            reports_dir = Path(temp_dir) / "reports"
            reports_dir.mkdir()

            log_file = reports_dir / "incidents.jsonl"

            incidents = [
                {"resource": "CPU", "severity": "WARNING"},
                {"incident_type": "CONNECTIVITY_FAILURE"},
                {"incident_type": "CONNECTIVITY_FAILURE"}
            ]

            with log_file.open("w", encoding="utf-8") as file:
                for incident in incidents:
                    file.write(json.dumps(incident) + "\n")

            fake_module_path = str(
                Path(temp_dir) / "incident_dashboard.py"
            )

            with patch("incident_dashboard.__file__", fake_module_path):
                with patch("builtins.print") as mock_print:
                    show_dashboard()

            mock_print.assert_any_call("Total incidents:", 3)
            mock_print.assert_any_call("CPU incidents:", 1)
            mock_print.assert_any_call("Connectivity incidents:", 2)


if __name__ == "__main__":
    unittest.main()
