import unittest
from src.data_quality_checks import DataQualityChecker

class TestDataQualityChecker(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = {
            'temperature': float,
            'humidity': float,
            'device_id': str
        }
        self.range_checks = {
            'temperature': {'min': -50.0, 'max': 100.0},
            'humidity': {'min': 0.0, 'max': 100.0}
        }
        self.checker = DataQualityChecker(self.schema, self.range_checks)

    def test_valid_data(self) -> None:
        data = {'temperature': 25.0, 'humidity': 45.0, 'device_id': 'sensor_123'}
        self.assertTrue(self.checker.check_data_quality(data))

    def test_missing_field(self) -> None:
        data = {'temperature': 25.0, 'humidity': 45.0}
        self.assertFalse(self.checker.check_data_quality(data))

    def test_incorrect_type(self) -> None:
        data = {'temperature': '25.0', 'humidity': 45.0, 'device_id': 'sensor_123'}
        self.assertFalse(self.checker.check_data_quality(data))

    def test_out_of_range(self) -> None:
        data = {'temperature': 150.0, 'humidity': 45.0, 'device_id': 'sensor_123'}
        self.assertFalse(self.checker.check_data_quality(data))

if __name__ == '__main__':
    unittest.main()
