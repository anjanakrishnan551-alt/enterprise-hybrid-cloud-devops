
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, call


from alert_manager import (
    send_alert,
    last_alert_times,
    ALERT_COOLDOWN,
    show_alert_statistics
)

class TestAlertManager(unittest.TestCase):

    def setUp(self):
        # Create a separate history file for each test
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.history_file = (
            Path(self.temp_dir.name) / "alert_history.json"
        )

        self.history_patch = patch(
            "alert_manager.ALERT_HISTORY_FILE",
            self.history_file
        )
        self.history_patch.start()
        self.addCleanup(self.history_patch.stop)

        last_alert_times.clear()
        self.addCleanup(last_alert_times.clear)

    def test_first_alert_is_displayed(self):
        incident = {
            "hostname": "TEST-SERVER",
            "resource": "CPU",
            "severity": "WARNING"
        }

        with patch("alert_manager.time.time", return_value=1000):
            with patch("builtins.print") as mock_print:
                send_alert(incident)

        mock_print.assert_any_call(
            "========== INFRASTRUCTURE ALERT =========="
        )
        mock_print.assert_any_call("Priority: MEDIUM")
        self.assertTrue(self.history_file.exists())

    def test_duplicate_alert_is_suppressed(self):
        incident = {
            "hostname": "TEST-SERVER",
            "resource": "CPU",
            "severity": "WARNING"
        }

        with patch("alert_manager.time.time", side_effect=[1000, 1100]):
            with patch("builtins.print") as mock_print:
                send_alert(incident)
                send_alert(incident)

        mock_print.assert_any_call(
            "Duplicate alert suppressed:", "TEST-SERVER", "CPU"
        )

        self.assertEqual(
            mock_print.call_args_list.count(
                call("========== INFRASTRUCTURE ALERT ==========")
            ),
            1
        )

    def test_alert_after_cooldown(self):
        incident = {
            "hostname": "TEST-SERVER",
            "resource": "CPU",
            "severity": "WARNING"
        }

        with patch(
            "alert_manager.time.time",
            side_effect=[1000, 1000 + ALERT_COOLDOWN + 1]
        ):
            with patch("builtins.print") as mock_print:
                send_alert(incident)
                send_alert(incident)

        self.assertEqual(
            mock_print.call_args_list.count(
                call("========== INFRASTRUCTURE ALERT ==========")
            ),
            2
        )

    def test_history_survives_restart(self):
        incident = {
            "hostname": "TEST-SERVER",
            "resource": "CPU",
            "severity": "WARNING"
        }

        with patch("alert_manager.time.time", return_value=1000):
            with patch("builtins.print"):
                send_alert(incident)

        # Simulate restarting Python by clearing memory
        last_alert_times.clear()

        with patch("alert_manager.time.time", return_value=1100):
            with patch("builtins.print") as mock_print:
                send_alert(incident)

        mock_print.assert_any_call(
            "Duplicate alert suppressed:", "TEST-SERVER", "CPU"
        )

    def test_alert_statistics(self):
        # Create sample alert history
        history = {
            "SERVER-01|CPU|WARNING": 1000,
            "SERVER-01|MEMORY|WARNING": 1100,
            "SERVER-02|CPU|CRITICAL": 1200
        }

        import json

        self.history_file.write_text(
            json.dumps(history),
            encoding="utf-8"
        )

        with patch("builtins.print") as mock_print:
            show_alert_statistics()

        mock_print.assert_any_call("Total unique alert keys:", 3)
        mock_print.assert_any_call("Servers with alerts:", 2)
        mock_print.assert_any_call("Cooldown period:", 300, "seconds")



if __name__ == "__main__":
    unittest.main()
