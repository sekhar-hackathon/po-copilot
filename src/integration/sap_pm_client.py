import requests
from typing import Dict

class SAPPMClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def create_work_order(self, work_order_data: Dict[str, str]) -> Dict[str, str]:
        """
        Sends a request to SAP PM to create a new work order.

        :param work_order_data: A dictionary containing work order details.
        :return: A dictionary with the response from SAP PM.
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(f'{self.base_url}/work-orders', json=work_order_data, headers=headers)
        response.raise_for_status()
        return response.json()
