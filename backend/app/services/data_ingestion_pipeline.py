import paho.mqtt.client as mqtt
import time
from influxdb import InfluxDBClient

class DataIngestionPipeline:
    def __init__(self, mqtt_broker: str, mqtt_port: int, influxdb_host: str, influxdb_port: int, influxdb_user: str, influxdb_password: str, influxdb_dbname: str):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.influxdb_client = InfluxDBClient(host=influxdb_host, port=influxdb_port, username=influxdb_user, password=influxdb_password, database=influxdb_dbname)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker!")
        client.subscribe("sensor/data")

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()}")
        data_point = self.process_message(msg.payload.decode())
        self.store_data(data_point)

    def process_message(self, message: str) -> dict:
        # Process the incoming message and convert it to a format suitable for InfluxDB
        # Example message processing logic
        data = message.split(',')
        return {
            "measurement": "sensor_data",
            "tags": {
                "sensor_id": data[0]
            },
            "fields": {
                "value": float(data[1])
            },
            "time": data[2]
        }

    def store_data(self, data_point: dict):
        self.influxdb_client.write_points([data_point])

    def archive_old_data(self):
        # Archive data older than 90 days
        query = "DELETE FROM sensor_data WHERE time < now() - 90d"
        self.influxdb_client.query(query)

    def start(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.mqtt_broker, self.mqtt_port, 60)
        client.loop_start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            client.loop_stop()
            print("MQTT client stopped.")
