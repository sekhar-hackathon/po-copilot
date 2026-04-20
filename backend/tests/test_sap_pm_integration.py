
import unittest
from app.services.sap_pm_integration import SAPPMIntegrationRequirements

class TestSAPPMIntegrationRequirements(unittest.TestCase):
    def setUp(self):
        self.sap_pm_integration = SAPPMIntegrationRequirements()

    def test_add_requirement(self):
        self.sap_pm_integration.add_requirement("Test requirement")
        self.assertIn("Test requirement", self.sap_pm_integration.get_requirements())

    def test_finalize_requirements(self):
        self.sap_pm_integration.add_requirement("Test requirement")
        self.sap_pm_integration.finalize_requirements()
        # Here we would check if the finalize logic works, e.g., sending to plant team
        # For now, we just check if the requirements are still accessible
        self.assertEqual(len(self.sap_pm_integration.get_requirements()), 1)

if __name__ == '__main__':
    unittest.main()
