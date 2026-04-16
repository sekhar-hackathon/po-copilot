import unittest
from data_ingestion import validate_data

class TestDataIngestion(unittest.TestCase):
    def test_validate_data(self):
        valid_data = {
            'sensor_id': 'sensor_123',
            'timestamp': '2023-10-01T12:00:00Z',
            'value': 42.0
        }
        invalid_data = {
            'sensor_id': 'sensor_123',
            'value': 42.0
        }

        self.assertTrue(validate_data(valid_data))
        self.assertFalse(validate_data(invalid_data))

if __name__ == '__main__':
    unittest.main()
