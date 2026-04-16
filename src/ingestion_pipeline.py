import asyncio
import json
from typing import Dict, Any
import aiohttp
import logging
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-token"
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "sensor_data"

async def fetch_sensor_data(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()

async def validate_data(data: Dict[str, Any]) -> bool:
    # Basic validation: check for required fields and types
    required_fields = {"sensor_id": str, "timestamp": str, "value": float}
    for field, field_type in required_fields.items():
        if field not in data or not isinstance(data[field], field_type):
            logging.warning(f"Malformed data: {data}")
            return False
    return True

async def ingest_data(data: Dict[str, Any], influx_client: InfluxDBClient):
    point = Point("sensor_reading") \
        .tag("sensor_id", data["sensor_id"]) \
        .field("value", data["value"]) \
        .time(data["timestamp"])
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

async def process_data(url: str):
    async with aiohttp.ClientSession() as session:
        async with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as influx_client:
            while True:
                try:
                    data = await fetch_sensor_data(session, url)
                    if await validate_data(data):
                        await ingest_data(data, influx_client)
                except Exception as e:
                    logging.error(f"Error processing data: {e}")

async def main():
    sensor_data_url = "http://sensor-data-source/api/readings"
    await asyncio.gather(*(process_data(sensor_data_url) for _ in range(10)))  # Simulate handling 10,000 readings per second

if __name__ == "__main__":
    asyncio.run(main())
