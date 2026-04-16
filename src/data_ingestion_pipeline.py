import time
import random
from typing import List, Dict
from influxdb import InfluxDBClient

class SensorDataIngestion:
    def __init__(self, db_host: str, db_port: int, db_name: str):
        self.client = InfluxDBClient(host=db_host, port=db_port)
        self.client.create_database(db_name)
        self.client.switch_database(db_name)

    def ingest_data(self, data: List[Dict]):
        # Write data to InfluxDB
        self.client.write_points(data)

    def generate_sensor_data(self, num_readings: int) -> List[Dict]:
        # Simulate sensor data generation
        data = []
        for _ in range(num_readings):
            data_point = {
                "measurement": "sensor_readings",
                "tags": {
                    "sensor_id": f"sensor_{random.randint(1, 100)}"
                },
                "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                "fields": {
                    "value": random.uniform(20.0, 30.0)
                }
            }
            data.append(data_point)
        return data

    def archive_old_data(self, retention_days: int):
        # Set retention policy to archive data older than specified days
        self.client.create_retention_policy(
            name="90_days_retention",
            duration=f"{retention_days}d",
            replication='1',
            default=True
        )

if __name__ == "__main__":
    ingestion = SensorDataIngestion(db_host="localhost", db_port=8086, db_name="sensor_data")
    ingestion.archive_old_data(retention_days=90)
    
    while True:
        # Simulate continuous data ingestion
        sensor_data = ingestion.generate_sensor_data(num_readings=10000)
        ingestion.ingest_data(sensor_data)
        time.sleep(1)  # Ingest every second