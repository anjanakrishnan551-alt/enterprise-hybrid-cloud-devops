
import unittest
import subprocess
from unittest.mock import patch, MagicMock

from connectivity_check import check_server


class TestConnectivityCheck(unittest.TestCase):

    @patch("connectivity_check.subprocess.run")
    def test_server_reachable(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)

        result = check_server("127.0.0.1")

        self.assertTrue(result)

    @patch("connectivity_check.subprocess.run")
    def test_server_unreachable(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)

        result = check_server("127.0.0.1")

        self.assertFalse(result)

    @patch("connectivity_check.subprocess.run")
    def test_server_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="ping",
            timeout=5
        )

        result = check_server("127.0.0.1")

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
