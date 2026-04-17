import unittest
from unittest.mock import MagicMock
from app.services.data_ingestion_pipeline import DataIngestionPipeline

class TestDataIngestionPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = DataIngestionPipeline(
            mqtt_broker='localhost',
            mqtt_port=1883,
            influxdb_host='localhost',
            influxdb_port=8086,
            influxdb_user='user',
            influxdb_password='password',
            influxdb_dbname='test_db'
        )
        self.pipeline.influxdb_client = MagicMock()

    def test_process_message(self):
        message = "sensor1,23.5,2023-10-01T00:00:00Z"
        expected_data_point = {
            "measurement": "sensor_data",
            "tags": {
                "sensor_id": "sensor1"
            },
            "fields": {
                "value": 23.5
            },
            "time": "2023-10-01T00:00:00Z"
        }
        data_point = self.pipeline.process_message(message)
        self.assertEqual(data_point, expected_data_point)

    def test_store_data(self):
        data_point = {
            "measurement": "sensor_data",
            "tags": {
                "sensor_id": "sensor1"
            },
            "fields": {
                "value": 23.5
            },
            "time": "2023-10-01T00:00:00Z"
        }
        self.pipeline.store_data(data_point)
        self.pipeline.influxdb_client.write_points.assert_called_once_with([data_point])

    def test_archive_old_data(self):
        self.pipeline.archive_old_data()
        self.pipeline.influxdb_client.query.assert_called_once_with("DELETE FROM sensor_data WHERE time < now() - 90d")

if __name__ == '__main__':
    unittest.main()
