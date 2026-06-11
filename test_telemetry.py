import unittest
telemetry = __import__("telemetry")
from datetime import datetime

class TestTelemetry(unittest.TestCase):
    def test_log_scan_metadata(self):
        try:
            telemetry.log_scan_metadata('SQL Injection', 'Python', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Telemetry engine error: {e}")

if __name__ == "__main__":
    unittest.main()