
import unittest
import subprocess
import ssh_monitor
from unittest.mock import patch, Mock

from ssh_monitor import get_remote_hostname


class TestSSHMonitor(unittest.TestCase):

    @patch("ssh_monitor.subprocess.run")
    def test_remote_hostname(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout="DESKTOP-51PBHDD\n",
            stderr=""
        )

        result = get_remote_hostname()

        self.assertEqual(result, "DESKTOP-51PBHDD")


    @patch("ssh_monitor.subprocess.run")
    def test_remote_cpu(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout="%Cpu(s): 0.1 us, 99.9 id",
            stderr=""
        )
        self.assertIn("Cpu(s)", ssh_monitor.get_remote_cpu())

    @patch("ssh_monitor.subprocess.run")
    def test_remote_memory(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Mem: 7.6Gi 603Mi",
            stderr=""
        )
        self.assertIn("Mem:", ssh_monitor.get_remote_memory())

    @patch("ssh_monitor.subprocess.run")
    def test_remote_disk(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout="/dev/sdd 1007G 1.6G 955G 1% /",
            stderr=""
        )
        self.assertIn("/dev/sdd", ssh_monitor.get_remote_disk())

    @patch("ssh_monitor.subprocess.run")
    def test_ssh_failure(self, mock_run):
        mock_run.return_value = Mock(
            returncode=255,
            stdout="",
            stderr="Permission denied"
        )
        with self.assertRaises(RuntimeError):
            ssh_monitor.run_ssh_command("hostname")

    @patch("ssh_monitor.subprocess.run")
    def test_ssh_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="ssh", timeout=15
        )
        with self.assertRaises(RuntimeError):
            ssh_monitor.run_ssh_command("hostname")


if __name__ == "__main__":
 
   unittest.main()
