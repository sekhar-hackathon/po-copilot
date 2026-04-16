import requests
from src.config.alert_config import AlertConfig

class AlertService:
    @staticmethod
    def send_push_notification(message: str) -> None:
        if AlertConfig.PUSH_NOTIFICATION_ENABLED:
            payload = AlertConfig.get_push_notification_payload(message)
            response = requests.post(AlertConfig.PUSH_NOTIFICATION_SERVICE_URL, json=payload)
            response.raise_for_status()

    @staticmethod
    def send_sms(phone_number: str, message: str) -> None:
        if AlertConfig.SMS_NOTIFICATION_ENABLED:
            payload = AlertConfig.get_sms_payload(phone_number, message)
            response = requests.post(AlertConfig.SMS_SERVICE_URL, json=payload)
            response.raise_for_status()

    @staticmethod
    def send_email(to_email: str, message: str) -> None:
        if AlertConfig.EMAIL_NOTIFICATION_ENABLED:
            payload = AlertConfig.get_email_payload(to_email, message)
            response = requests.post(AlertConfig.EMAIL_SERVICE_URL, json=payload)
            response.raise_for_status()
