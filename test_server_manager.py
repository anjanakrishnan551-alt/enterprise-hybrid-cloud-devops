
import unittest
from unittest.mock import patch

from server_manager import monitor_server


class TestServerManager(unittest.TestCase):

    @patch("server_manager.log_connectivity_failure")
    @patch("server_manager.check_server")
    def test_unreachable_server(self, mock_check, mock_log):
        mock_check.return_value = False

        server = {
            "name": "TEST-LINUX-SERVER",
            "host": "192.0.2.10"
        }

        result = monitor_server(server)

        self.assertFalse(result)
        mock_check.assert_called_once_with("192.0.2.10")
        mock_log.assert_called_once_with(
            "TEST-LINUX-SERVER",
            "192.0.2.10"
        )

    @patch("server_manager.log_connectivity_failure")
    @patch("server_manager.check_server")
    def test_reachable_server(self, mock_check, mock_log):
        mock_check.return_value = True

        server = {
            "name": "TEST-WINDOWS-SERVER",
            "host": "127.0.0.1"
        }

        result = monitor_server(server)

        self.assertTrue(result)
        mock_check.assert_called_once_with("127.0.0.1")
        mock_log.assert_not_called()


if __name__ == "__main__":
    unittest.main()
