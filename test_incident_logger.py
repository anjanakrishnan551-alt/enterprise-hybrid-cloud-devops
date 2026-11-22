
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from incident_logger import log_incident


class TestIncidentLogger(unittest.TestCase):

    def test_incident_is_saved(self):
        with TemporaryDirectory() as temp_dir:
            with patch("incident_logger.Path") as mock_path:
                mock_path.return_value = Path(temp_dir)

                log_incident("TEST-SERVER", "CPU", 95)

                log_file = Path(temp_dir) / "incidents.jsonl"

                self.assertTrue(log_file.exists())

                with log_file.open("r", encoding="utf-8") as file:
                    incident = json.loads(file.readline())

                self.assertEqual(incident["hostname"], "TEST-SERVER")
                self.assertEqual(incident["resource"], "CPU")
                self.assertEqual(incident["usage_percent"], 95)
                self.assertEqual(incident["severity"], "WARNING")


if __name__ == "__main__":
    unittest.main()
