import asyncio
import json
import aiomysql
from typing import Dict, Any

async def validate_data(data: Dict[str, Any]) -> bool:
    """
    Validate sensor data.
    Returns True if data is valid, False otherwise.
    """
    # Example validation: Check if all required fields are present
    required_fields = {'sensor_id', 'timestamp', 'value'}
    if not required_fields.issubset(data.keys()):
        return False
    # Additional validation logic can be added here
    return True

async def ingest_data(data: Dict[str, Any], pool: aiomysql.Pool) -> None:
    """
    Ingest validated data into the database.
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO sensor_data (sensor_id, timestamp, value) VALUES (%s, %s, %s)",
                (data['sensor_id'], data['timestamp'], data['value'])
            )
            await conn.commit()

async def process_sensor_data(pool: aiomysql.Pool) -> None:
    """
    Process incoming sensor data.
    """
    # Simulate data ingestion from a source
    async for data in simulate_data_source():
        if validate_data(data):
            await ingest_data(data, pool)
        else:
            print(f"Malformed data rejected: {data}")

async def simulate_data_source() -> Dict[str, Any]:
    """
    Simulate a data source generating sensor data.
    """
    # This is a placeholder for actual data source logic
    while True:
        await asyncio.sleep(0.1)  # Simulate 10,000 readings per second
        yield {
            'sensor_id': 'sensor_123',
            'timestamp': '2023-10-01T12:00:00Z',
            'value': 42.0
        }

async def main() -> None:
    """
    Main function to set up the database connection and start processing.
    """
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='user', password='password',
                                      db='sensor_db', loop=asyncio.get_event_loop())
    await process_sensor_data(pool)

if __name__ == '__main__':
    asyncio.run(main())
