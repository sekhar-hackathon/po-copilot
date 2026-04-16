import unittest
import os
import json
from src.data_ingestion_pipeline import DataIngestionPipeline

class TestDataIngestionPipeline(unittest.TestCase):
    def setUp(self):
        self.source_directory = 'test_data/sensor'
        self.destination_file = 'test_data/processed/processed_data.json'
        os.makedirs(self.source_directory, exist_ok=True)
        os.makedirs(os.path.dirname(self.destination_file), exist_ok=True)
        
        # Create sample JSON files
        sample_data_1 = {'temperature': 22.5, 'humidity': 45}
        sample_data_2 = {'temperature': None, 'humidity': 50}
        with open(os.path.join(self.source_directory, 'data1.json'), 'w') as f:
            json.dump(sample_data_1, f)
        with open(os.path.join(self.source_directory, 'data2.json'), 'w') as f:
            json.dump(sample_data_2, f)

    def tearDown(self):
        # Clean up test files
        for filename in os.listdir(self.source_directory):
            file_path = os.path.join(self.source_directory, filename)
            os.remove(file_path)
        os.rmdir(self.source_directory)
        if os.path.exists(self.destination_file):
            os.remove(self.destination_file)
        os.rmdir(os.path.dirname(self.destination_file))

    def test_pipeline(self):
        pipeline = DataIngestionPipeline(self.source_directory, self.destination_file)
        pipeline.run()

        # Check if processed data file is created
        self.assertTrue(os.path.exists(self.destination_file))

        # Check contents of the processed data file
        with open(self.destination_file, 'r') as f:
            processed_data = json.load(f)
        expected_data = [{'temperature': 22.5, 'humidity': 45}]
        self.assertEqual(processed_data, expected_data)

if __name__ == '__main__':
    unittest.main()
