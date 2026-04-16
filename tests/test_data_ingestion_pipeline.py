import unittest
from unittest.mock import patch, MagicMock
from src.data_ingestion_pipeline import SensorDataIngestionPipeline, simulate_sensor_data

class TestSensorDataIngestionPipeline(unittest.TestCase):
    @patch('src.data_ingestion_pipeline.InfluxDBClient')
    def test_ingest_data(self, MockInfluxDBClient):
        mock_client = MockInfluxDBClient.return_value
        pipeline = SensorDataIngestionPipeline(influx_host="localhost", influx_port=8086, influx_db="test_db")

        sensor_data = simulate_sensor_data()
        pipeline.ingest_data(sensor_data)

        self.assertEqual(mock_client.write_points.call_count, 1)

    @patch('src.data_ingestion_pipeline.InfluxDBClient')
    def test_archive_old_data(self, MockInfluxDBClient):
        mock_client = MockInfluxDBClient.return_value
        pipeline = SensorDataIngestionPipeline(influx_host="localhost", influx_port=8086, influx_db="test_db")

        pipeline.archive_old_data()

        mock_client.create_retention_policy.assert_called_once_with(name="archive_policy", duration="90d", replication="1", default=True)


if __name__ == '__main__':
    unittest.main()
