from datetime import datetime, timedelta
from threading import Timer
from alert_service import AlertService

class AlertManager:
    def __init__(self, alert_service: AlertService):
        self.alert_service = alert_service
        self.pending_alerts = {}

    def create_alert(self, alert_id: str, recipients: dict, message: str):
        self.alert_service.send_email(recipients['emails'], 'Critical Bearing Alert', message)
        self.alert_service.send_sms(recipients['phones'], message)
        self.alert_service.send_push_notification(recipients['device_tokens'], message)
        self.schedule_escalation(alert_id)

    def schedule_escalation(self, alert_id: str):
        escalation_time = datetime.now() + timedelta(minutes=30)
        timer = Timer((escalation_time - datetime.now()).total_seconds(), self.escalate_alert, [alert_id])
        self.pending_alerts[alert_id] = timer
        timer.start()

    def escalate_alert(self, alert_id: str):
        if alert_id in self.pending_alerts:
            self.alert_service.escalate_alert(alert_id)
            del self.pending_alerts[alert_id]

    def acknowledge_alert(self, alert_id: str):
        if alert_id in self.pending_alerts:
            self.pending_alerts[alert_id].cancel()
            del self.pending_alerts[alert_id]
