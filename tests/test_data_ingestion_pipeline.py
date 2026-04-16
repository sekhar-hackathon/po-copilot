import unittest
from unittest.mock import patch, MagicMock
from src.data_ingestion_pipeline import SensorDataIngestion

class TestSensorDataIngestion(unittest.TestCase):
    @patch('src.data_ingestion_pipeline.InfluxDBClient')
    def test_ingest_data(self, MockInfluxDBClient):
        mock_client = MockInfluxDBClient.return_value
        ingestion = SensorDataIngestion(db_host="localhost", db_port=8086, db_name="test_db")
        data = ingestion.generate_sensor_data(num_readings=10)
        ingestion.ingest_data(data)
        mock_client.write_points.assert_called_once_with(data)

    @patch('src.data_ingestion_pipeline.InfluxDBClient')
    def test_archive_old_data(self, MockInfluxDBClient):
        mock_client = MockInfluxDBClient.return_value
        ingestion = SensorDataIngestion(db_host="localhost", db_port=8086, db_name="test_db")
        ingestion.archive_old_data(retention_days=90)
        mock_client.create_retention_policy.assert_called_once_with(
            name="90_days_retention",
            duration="90d",
            replication='1',
            default=True
        )

if __name__ == '__main__':
    unittest.main()