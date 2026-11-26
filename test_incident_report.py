
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from incident_report import generate_incident_report


class TestIncidentReport(unittest.TestCase):

    def test_report_generation(self):
        # Create a temporary test folder
        with tempfile.TemporaryDirectory() as temp_dir:
            project_folder = Path(temp_dir)
            reports_folder = project_folder / "reports"
            reports_folder.mkdir()

            # Create a fictional incident
            incident = {
                "timestamp": "2026-11-22T10:00:00+00:00",
                "hostname": "TEST-LINUX-SERVER",
                "incident_type": "CONNECTIVITY_FAILURE",
                "severity": "WARNING"
            }

            # Save the fictional incident to a test log
            log_file = reports_folder / "incidents.jsonl"
            log_file.write_text(
                json.dumps(incident) + "\n",
                encoding="utf-8"
            )

            # Make the report generator use our temporary folder
            fake_path = str(project_folder / "incident_report.py")

            with patch("incident_report.__file__", fake_path):
                with patch("builtins.print"):
                    generate_incident_report()

            # Find the generated report
            saved_reports = list(
                reports_folder.glob("incident_report_*.txt")
            )

            # Confirm exactly one report was saved
            self.assertEqual(len(saved_reports), 1)

            # Read the saved report
            report_text = saved_reports[0].read_text(
                encoding="utf-8"
            )

            # Check the report contents
            self.assertIn("TEST-LINUX-SERVER", report_text)
            self.assertIn(
                "Network connectivity failure",
                report_text
            )
            self.assertIn("Severity: WARNING", report_text)
            self.assertIn(
                "Check server, network and firewall",
                report_text
            )
            self.assertIn(
                "2026-11-22T10:00:00+00:00",
                report_text
            )


if __name__ == "__main__":
    unittest.main()

