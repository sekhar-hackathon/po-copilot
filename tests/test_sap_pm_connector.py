import unittest
from unittest.mock import patch, Mock
from src.integration.sap_pm_connector import SAPPMConnector

class TestSAPPMConnector(unittest.TestCase):
    @patch('src.integration.sap_pm_connector.requests.post')
    def test_create_work_order(self, mock_post):
        # Setup
        mock_response = Mock()
        mock_response.json.return_value = {"WorkOrderID": "12345"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        connector = SAPPMConnector(base_url="http://sap.example.com", username="user", password="pass")
        alert_data = {
            "id": "alert123",
            "description": "Test alert",
            "priority": "High",
            "equipment_id": "EQ123"
        }

        # Execute
        response = connector.create_work_order(alert_data)

        # Verify
        self.assertEqual(response, {"WorkOrderID": "12345"})
        mock_post.assert_called_once_with(
            "http://sap.example.com/sap/opu/odata/sap/ZCREATE_WORK_ORDER_SRV/WorkOrderSet",
            json={
                "AlertID": "alert123",
                "Description": "Test alert",
                "Priority": "High",
                "EquipmentID": "EQ123",
                "NotificationType": "M1"
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            auth=('user', 'pass')
        )

if __name__ == '__main__':
    unittest.main()
