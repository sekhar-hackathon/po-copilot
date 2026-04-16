import datetime
from typing import List, Dict

class MaintenanceWorkOrder:
    def __init__(self, machine_id: str, bearing_id: str, failure_mode: str, recommended_action: str, downtime_estimate: int):
        self.machine_id = machine_id
        self.bearing_id = bearing_id
        self.failure_mode = failure_mode
        self.recommended_action = recommended_action
        self.downtime_estimate = downtime_estimate
        self.creation_date = datetime.datetime.now()

    def to_dict(self) -> Dict[str, str]:
        return {
            "machine_id": self.machine_id,
            "bearing_id": self.bearing_id,
            "failure_mode": self.failure_mode,
            "recommended_action": self.recommended_action,
            "downtime_estimate": str(self.downtime_estimate),
            "creation_date": self.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        }

class SAPPMInterface:
    def create_work_order(self, work_order_data: Dict[str, str]) -> bool:
        # Simulate interaction with SAP PM system
        print(f"Creating work order in SAP PM: {work_order_data}")
        return True

class MaintenanceWorkOrderGenerator:
    def __init__(self, sap_interface: SAPPMInterface):
        self.sap_interface = sap_interface

    def generate_work_orders(self, issues: List[Dict[str, str]]) -> List[MaintenanceWorkOrder]:
        work_orders = []
        for issue in issues:
            work_order = MaintenanceWorkOrder(
                machine_id=issue["machine_id"],
                bearing_id=issue["bearing_id"],
                failure_mode=issue["failure_mode"],
                recommended_action=issue["recommended_action"],
                downtime_estimate=int(issue["downtime_estimate"])
            )
            work_orders.append(work_order)
            self.sap_interface.create_work_order(work_order.to_dict())
        return work_orders
