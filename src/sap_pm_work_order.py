import datetime
from typing import Dict, Any

class SAPPMWorkOrder:
    def __init__(self, machine_id: str, bearing_id: str, predicted_failure_mode: str, recommended_action: str, estimated_downtime: float):
        self.machine_id = machine_id
        self.bearing_id = bearing_id
        self.predicted_failure_mode = predicted_failure_mode
        self.recommended_action = recommended_action
        self.estimated_downtime = estimated_downtime
        self.creation_date = datetime.datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the work order to a dictionary format suitable for SAP PM."""
        return {
            "machine_id": self.machine_id,
            "bearing_id": self.bearing_id,
            "predicted_failure_mode": self.predicted_failure_mode,
            "recommended_action": self.recommended_action,
            "estimated_downtime": self.estimated_downtime,
            "creation_date": self.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        }

    def create_in_sap_pm(self) -> bool:
        """Simulate the creation of a work order in SAP PM."""
        # This is a mock implementation. In a real scenario, this would involve
        # API calls to SAP PM system.
        work_order_data = self.to_dict()
        print(f"Creating work order in SAP PM: {work_order_data}")
        # Assume the work order creation is successful
        return True
