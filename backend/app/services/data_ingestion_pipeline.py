
import os
import time
import logging
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.ingest import KustoIngestClient, IngestionProperties, DataFormat

# Configure logging
logging.basicConfig(level=logging.INFO)

class DataIngestionPipeline:
    def __init__(self, cluster_url: str, database_name: str, table_name: str, client_id: str, client_secret: str, tenant_id: str):
        self.cluster_url = cluster_url
        self.database_name = database_name
        self.table_name = table_name

        # Create Kusto connection string
        kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
            cluster_url, client_id, client_secret, tenant_id
        )

        # Initialize Kusto client
        self.kusto_client = KustoClient(kcsb)
        self.ingest_client = KustoIngestClient(kcsb)

        # Define ingestion properties
        self.ingestion_properties = IngestionProperties(
            database=self.database_name,
            table=self.table_name,
            data_format=DataFormat.CSV,
            report_level=IngestionProperties.ReportLevel.FailuresOnly
        )

    def ingest_data(self, data: str):
        try:
            # Ingest data into Azure Data Explorer
            self.ingest_client.ingest_from_memory(data, self.ingestion_properties)
            logging.info(f"Data ingested successfully into {self.table_name}.")
        except Exception as e:
            logging.error(f"Failed to ingest data: {e}")

    def run(self):
        while True:
            # Simulate data fetching from sensors
            sensor_data = self.fetch_sensor_data()
            self.ingest_data(sensor_data)
            time.sleep(5)  # Wait for 5 seconds before fetching new data

    def fetch_sensor_data(self) -> str:
        # Placeholder for sensor data fetching logic
        # In a real scenario, this would interface with the sensor hardware or API
        return "timestamp,sensor_value\n2023-10-01T12:00:00Z,42"

if __name__ == "__main__":
    # Environment variables for Azure authentication
    CLUSTER_URL = os.getenv('AZURE_CLUSTER_URL')
    DATABASE_NAME = os.getenv('AZURE_DATABASE_NAME')
    TABLE_NAME = os.getenv('AZURE_TABLE_NAME')
    CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
    CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
    TENANT_ID = os.getenv('AZURE_TENANT_ID')

    # Initialize and run the data ingestion pipeline
    pipeline = DataIngestionPipeline(
        cluster_url=CLUSTER_URL,
        database_name=DATABASE_NAME,
        table_name=TABLE_NAME,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        tenant_id=TENANT_ID
    )
    pipeline.run()
