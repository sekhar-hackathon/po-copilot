import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataQualityChecker:
    def __init__(self, schema: Dict[str, Any], range_checks: Dict[str, Dict[str, float]]) -> None:
        """
        Initialize the data quality checker with schema and range checks.

        :param schema: A dictionary defining expected types for each field.
        :param range_checks: A dictionary defining min and max values for each field.
        """
        self.schema = schema
        self.range_checks = range_checks

    def check_data_quality(self, data: Dict[str, Any]) -> bool:
        """
        Check the quality of the data based on schema and range checks.

        :param data: A dictionary of data to be checked.
        :return: True if data is valid, False otherwise.
        """
        for field, expected_type in self.schema.items():
            if field not in data:
                logging.error(f"Missing field: {field}")
                return False
            if not isinstance(data[field], expected_type):
                logging.error(f"Field {field} has incorrect type: expected {expected_type}, got {type(data[field])}")
                return False

        for field, checks in self.range_checks.items():
            value = data.get(field)
            if value is not None:
                if 'min' in checks and value < checks['min']:
                    logging.error(f"Field {field} is below minimum: {value} < {checks['min']}")
                    return False
                if 'max' in checks and value > checks['max']:
                    logging.error(f"Field {field} is above maximum: {value} > {checks['max']}")
                    return False

        logging.info("Data passed quality checks")
        return True
