import requests
from typing import Dict, Any

class SAPPMConnector:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = (username, password)

    def create_work_order(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a maintenance work order in SAP PM based on alert data.

        :param alert_data: Dictionary containing alert information.
        :return: Response from SAP PM API.
        """
        endpoint = f"{self.base_url}/sap/opu/odata/sap/ZCREATE_WORK_ORDER_SRV/WorkOrderSet"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # Construct the payload for the work order creation
        payload = {
            "AlertID": alert_data.get("id"),
            "Description": alert_data.get("description"),
            "Priority": alert_data.get("priority"),
            "EquipmentID": alert_data.get("equipment_id"),
            "NotificationType": "M1"  # Example notification type
        }
        response = requests.post(endpoint, json=payload, headers=headers, auth=self.auth)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
