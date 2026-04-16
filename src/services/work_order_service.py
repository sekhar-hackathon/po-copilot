from typing import Dict
from src.integration.sap_pm_client import SAPPMClient

class WorkOrderService:
    def __init__(self, sap_pm_client: SAPPMClient):
        self.sap_pm_client = sap_pm_client

    def generate_work_order(self, machine_id: str, bearing_id: str, failure_mode: str, recommended_action: str, estimated_downtime: str) -> Dict[str, str]:
        """
        Generates a work order and sends it to SAP PM.

        :param machine_id: ID of the machine.
        :param bearing_id: ID of the bearing.
        :param failure_mode: Description of the failure mode.
        :param recommended_action: Recommended action to resolve the issue.
        :param estimated_downtime: Estimated downtime for the repair.
        :return: Response from SAP PM.
        """
        work_order_data = {
            'machine_id': machine_id,
            'bearing_id': bearing_id,
            'failure_mode': failure_mode,
            'recommended_action': recommended_action,
            'estimated_downtime': estimated_downtime
        }
        return self.sap_pm_client.create_work_order(work_order_data)
