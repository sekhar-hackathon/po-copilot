import time
import threading
from typing import List, Dict
from influxdb import InfluxDBClient

class SensorDataIngestionPipeline:
    def __init__(self, influx_host: str, influx_port: int, influx_db: str):
        self.client = InfluxDBClient(host=influx_host, port=influx_port)
        self.client.create_database(influx_db)
        self.client.switch_database(influx_db)

    def ingest_data(self, sensor_data: List[Dict[str, float]]) -> None:
        json_body = [
            {
                "measurement": "sensor_data",
                "tags": {
                    "sensor_id": data["sensor_id"]
                },
                "time": data["timestamp"],
                "fields": {
                    "value": data["value"]
                }
            }
            for data in sensor_data
        ]
        self.client.write_points(json_body)

    def archive_old_data(self, retention_policy: str = "90d") -> None:
        self.client.create_retention_policy(name="archive_policy", duration=retention_policy, replication="1", default=True)

    def run(self, sensor_data_stream: List[Dict[str, float]]) -> None:
        while True:
            self.ingest_data(sensor_data_stream)
            time.sleep(1)


def simulate_sensor_data() -> List[Dict[str, float]]:
    # Simulate 10,000 sensor readings per second
    return [
        {
            "sensor_id": f"sensor_{i}",
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "value": i * 0.1
        }
        for i in range(10000)
    ]


def main() -> None:
    pipeline = SensorDataIngestionPipeline(influx_host="localhost", influx_port=8086, influx_db="sensor_data")
    pipeline.archive_old_data()

    # Simulate data ingestion in a separate thread
    threading.Thread(target=pipeline.run, args=(simulate_sensor_data(),), daemon=True).start()

    # Keep the main thread alive
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
