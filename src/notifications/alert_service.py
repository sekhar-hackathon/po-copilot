from datetime import datetime
from typing import List

class AlertService:
    def __init__(self, push_notifier, sms_sender, email_sender, logger):
        self.push_notifier = push_notifier
        self.sms_sender = sms_sender
        self.email_sender = email_sender
        self.logger = logger

    def send_alerts(self, bearing_id: int, health_score: float, supervisors: List[str]):
        if health_score < 20.0:  # Assuming critical health score is below 20
            message = f"Critical alert for bearing {bearing_id}: Health score is {health_score}"
            self.push_notifier.send_push_notification(message)
            self.sms_sender.send_sms(supervisors, message)
            self.email_sender.send_email(supervisors, "Critical Health Score Alert", message)
            self.logger.log_alert(bearing_id, health_score, datetime.now())
