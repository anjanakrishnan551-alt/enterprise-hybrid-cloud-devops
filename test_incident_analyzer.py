
import unittest
from unittest.mock import patch

from incident_analyzer import analyze_incident, get_incident_analysis

class TestIncidentAnalyzer(unittest.TestCase):

    def test_cpu_incident(self):
        incident = {
            "hostname": "TEST-SERVER",
            "resource": "CPU",
            "usage_percent": 95,
            "severity": "WARNING"
        }

        with patch("builtins.print") as mock_print:
            analyze_incident(incident)

        mock_print.assert_any_call("Problem: High CPU usage")
        mock_print.assert_any_call("- Check CPU-intensive processes")

    def test_connectivity_incident(self):
        incident = {
            "hostname": "TEST-LINUX-SERVER",
            "incident_type": "CONNECTIVITY_FAILURE",
            "severity": "WARNING"
        }

        with patch("builtins.print") as mock_print:
            analyze_incident(incident)

        mock_print.assert_any_call(
            "Problem: Network connectivity failure"
        )
        mock_print.assert_any_call("- Review firewall rules")

    def test_unknown_incident(self):
        incident = {
            "hostname": "TEST-SERVER",
            "incident_type": "UNKNOWN"
        }

        with patch("builtins.print") as mock_print:
            analyze_incident(incident)

        mock_print.assert_any_call("Problem: Unknown incident type")
        mock_print.assert_any_call(
            "Recommended check: Review incident details"
        )

    def test_structured_cpu_analysis(self):
        incident = {
            "hostname": "TEST-SERVER",
            "resource": "CPU",
            "severity": "WARNING"
        }

        result = get_incident_analysis(incident)

        self.assertEqual(result["hostname"], "TEST-SERVER")
        self.assertEqual(result["problem"], "High CPU usage")
        self.assertEqual(result["severity"], "WARNING")
        self.assertEqual(
            result["recommended_action"],
            "Investigate CPU-intensive processes"
        )

    def test_structured_connectivity_analysis(self):
        incident = {
            "hostname": "TEST-LINUX-SERVER",
            "incident_type": "CONNECTIVITY_FAILURE",
            "severity": "WARNING"
        }

        result = get_incident_analysis(incident)

        self.assertEqual(
            result["problem"],
            "Network connectivity failure"
        )
        self.assertEqual(
            result["recommended_action"],
            "Check server, network and firewall"
        )


if __name__ == "__main__":
    unittest.main()
