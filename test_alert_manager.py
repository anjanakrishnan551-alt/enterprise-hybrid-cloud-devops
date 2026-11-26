
import unittest
from unittest.mock import patch

from alert_manager import (
    send_alert,
    last_alert_times,
    ALERT_COOLDOWN
)


class TestAlertManager(unittest.TestCase):

    def setUp(self):
        # Clear previous alerts before each test
        last_alert_times.clear()

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
                unittest.mock.call(
                    "========== INFRASTRUCTURE ALERT =========="
                )
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
                unittest.mock.call(
                    "========== INFRASTRUCTURE ALERT =========="
                )
            ),
            2
        )


if __name__ == "__main__":
    unittest.main()
