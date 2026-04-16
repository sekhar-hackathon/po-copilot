import asyncio
import pytest
from aiohttp import web
from src.ingestion_pipeline import validate_data, ingest_data
from influxdb_client import InfluxDBClient

@pytest.mark.asyncio
async def test_validate_data():
    valid_data = {"sensor_id": "sensor_1", "timestamp": "2023-10-01T12:00:00Z", "value": 23.5}
    invalid_data = {"sensor_id": "sensor_1", "timestamp": "2023-10-01T12:00:00Z"}  # Missing value
    assert await validate_data(valid_data) is True
    assert await validate_data(invalid_data) is False

@pytest.mark.asyncio
async def test_ingest_data(mocker):
    mock_write_api = mocker.Mock()
    mock_influx_client = mocker.Mock(write_api=lambda: mock_write_api)
    data = {"sensor_id": "sensor_1", "timestamp": "2023-10-01T12:00:00Z", "value": 23.5}
    await ingest_data(data, mock_influx_client)
    mock_write_api.write.assert_called_once()
