import unittest
from src.sap_pm_work_order import SAPPMWorkOrder

class TestSAPPMWorkOrder(unittest.TestCase):
    def test_work_order_creation(self):
        """Test the creation of a work order and its conversion to dictionary."""
        work_order = SAPPMWorkOrder(
            machine_id="M123",
            bearing_id="B456",
            predicted_failure_mode="Overheating",
            recommended_action="Replace bearing",
            estimated_downtime=2.5
        )
        work_order_dict = work_order.to_dict()
        self.assertEqual(work_order_dict["machine_id"], "M123")
        self.assertEqual(work_order_dict["bearing_id"], "B456")
        self.assertEqual(work_order_dict["predicted_failure_mode"], "Overheating")
        self.assertEqual(work_order_dict["recommended_action"], "Replace bearing")
        self.assertEqual(work_order_dict["estimated_downtime"], 2.5)

    def test_create_in_sap_pm(self):
        """Test the mock creation of a work order in SAP PM."""
        work_order = SAPPMWorkOrder(
            machine_id="M123",
            bearing_id="B456",
            predicted_failure_mode="Overheating",
            recommended_action="Replace bearing",
            estimated_downtime=2.5
        )
        self.assertTrue(work_order.create_in_sap_pm())

if __name__ == '__main__':
    unittest.main()
