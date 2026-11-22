
import unittest
from health_monitor import check_incident


class TestHealthMonitor(unittest.TestCase):

    def test_healthy_cpu(self):
        result = check_incident("CPU", 25)
        self.assertEqual(result, "CPU Status: HEALTHY")

    def test_high_cpu(self):
        result = check_incident("CPU", 95)
        self.assertEqual(
            result,
            "WARNING: High CPU usage detected (95%)"
        )

    def test_threshold(self):
        result = check_incident("CPU", 80)
        self.assertEqual(
            result,
            "WARNING: High CPU usage detected (80%)"
        )

    def test_below_threshold(self):
        result = check_incident("CPU", 79)
        self.assertEqual(result, "CPU Status: HEALTHY")


if __name__ == "__main__":
    unittest.main()
