import os
import json
from typing import List, Dict

class DataIngestionPipeline:
    def __init__(self, source_directory: str, destination_file: str):
        self.source_directory = source_directory
        self.destination_file = destination_file

    def read_sensor_data(self) -> List[Dict]:
        """
        Reads JSON files from the source directory and returns a list of sensor data.
        """
        sensor_data = []
        for filename in os.listdir(self.source_directory):
            if filename.endswith('.json'):
                file_path = os.path.join(self.source_directory, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    sensor_data.append(data)
        return sensor_data

    def process_data(self, data: List[Dict]) -> List[Dict]:
        """
        Processes the raw sensor data and returns the processed data.
        """
        # Example processing: filter out entries with missing values
        processed_data = [entry for entry in data if all(value is not None for value in entry.values())]
        return processed_data

    def store_data(self, data: List[Dict]):
        """
        Stores the processed data into the destination file.
        """
        with open(self.destination_file, 'w') as file:
            json.dump(data, file, indent=4)

    def run(self):
        """
        Executes the data ingestion pipeline.
        """
        raw_data = self.read_sensor_data()
        processed_data = self.process_data(raw_data)
        self.store_data(processed_data)

if __name__ == "__main__":
    pipeline = DataIngestionPipeline(source_directory='data/sensor', destination_file='data/processed/processed_data.json')
    pipeline.run()
