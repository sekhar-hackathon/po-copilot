import unittest
from unittest.mock import MagicMock
from src.services.work_order_service import WorkOrderService
from src.integration.sap_pm_client import SAPPMClient

class TestWorkOrderService(unittest.TestCase):
    def setUp(self):
        self.sap_pm_client = SAPPMClient(base_url='https://sap.example.com', api_key='dummy_api_key')
        self.sap_pm_client.create_work_order = MagicMock(return_value={'status': 'success'})
        self.work_order_service = WorkOrderService(sap_pm_client=self.sap_pm_client)

    def test_generate_work_order(self):
        response = self.work_order_service.generate_work_order(
            machine_id='M123',
            bearing_id='B456',
            failure_mode='Overheating',
            recommended_action='Replace bearing',
            estimated_downtime='2 hours'
        )
        self.sap_pm_client.create_work_order.assert_called_once_with({
            'machine_id': 'M123',
            'bearing_id': 'B456',
            'failure_mode': 'Overheating',
            'recommended_action': 'Replace bearing',
            'estimated_downtime': '2 hours'
        })
        self.assertEqual(response, {'status': 'success'})

if __name__ == '__main__':
    unittest.main()
