import unittest
from unittest.mock import MagicMock
from src.maintenance_work_order_generator import MaintenanceWorkOrderGenerator, SAPPMInterface

class TestMaintenanceWorkOrderGenerator(unittest.TestCase):
    def setUp(self):
        self.sap_interface = SAPPMInterface()
        self.sap_interface.create_work_order = MagicMock(return_value=True)
        self.generator = MaintenanceWorkOrderGenerator(self.sap_interface)

    def test_generate_work_orders(self):
        issues = [
            {
                "machine_id": "M123",
                "bearing_id": "B456",
                "failure_mode": "Overheating",
                "recommended_action": "Replace bearing",
                "downtime_estimate": "120"
            }
        ]
        work_orders = self.generator.generate_work_orders(issues)
        self.assertEqual(len(work_orders), 1)
        self.sap_interface.create_work_order.assert_called_once()
        self.assertEqual(work_orders[0].machine_id, "M123")
        self.assertEqual(work_orders[0].bearing_id, "B456")
        self.assertEqual(work_orders[0].failure_mode, "Overheating")
        self.assertEqual(work_orders[0].recommended_action, "Replace bearing")
        self.assertEqual(work_orders[0].downtime_estimate, 120)

if __name__ == '__main__':
    unittest.main()
