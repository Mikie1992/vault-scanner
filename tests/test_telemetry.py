# Test code goes here
import unittest
from vault_scanner_app.telemetry import telemetry_function

class TestTelemetry(unittest.TestCase):
    def test_telemetry_function(self):
        # Write your test case here
        self.assertEqual(telemetry_function(), expected_result)

if __name__ == '__main__':
    unittest.main()