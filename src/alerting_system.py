import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AlertingSystem:
    def __init__(self, email_config: dict, sms_config: dict, push_service: object):
        self.email_config = email_config
        self.sms_config = sms_config
        self.push_service = push_service

    def send_email(self, subject: str, message: str, to_email: str) -> None:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.email_config['from_email']
        msg['To'] = to_email

        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            server.login(self.email_config['smtp_user'], self.email_config['smtp_password'])
            server.sendmail(self.email_config['from_email'], [to_email], msg.as_string())
        logging.info(f'Email sent to {to_email}')

    def send_sms(self, message: str, to_number: str) -> None:
        client = Client(self.sms_config['account_sid'], self.sms_config['auth_token'])
        client.messages.create(
            body=message,
            from_=self.sms_config['from_number'],
            to=to_number
        )
        logging.info(f'SMS sent to {to_number}')

    def send_push_notification(self, message: str, user_id: str) -> None:
        self.push_service.send_notification(user_id, message)
        logging.info(f'Push notification sent to user {user_id}')

    def log_alert(self, alert_type: str, message: str) -> None:
        logging.info(f'Alert logged: {alert_type} - {message}')

    def escalate_alert(self, alert_type: str, message: str) -> None:
        # Placeholder for escalation logic
        logging.info(f'Escalation initiated for alert: {alert_type} - {message}')

    def handle_critical_alert(self, alert_type: str, message: str, user_id: str, to_email: str, to_number: str) -> None:
        self.send_email(f'Critical Alert: {alert_type}', message, to_email)
        self.send_sms(message, to_number)
        self.send_push_notification(message, user_id)
        self.log_alert(alert_type, message)
        self.escalate_alert(alert_type, message)

# Example usage
if __name__ == '__main__':
    email_config = {
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'smtp_user': 'user@example.com',
        'smtp_password': 'password',
        'from_email': 'alerts@example.com'
    }

    sms_config = {
        'account_sid': 'your_account_sid',
        'auth_token': 'your_auth_token',
        'from_number': '+1234567890'
    }

    class MockPushService:
        def send_notification(self, user_id: str, message: str) -> None:
            print(f'Push notification to {user_id}: {message}')

    push_service = MockPushService()

    alerting_system = AlertingSystem(email_config, sms_config, push_service)
    alerting_system.handle_critical_alert('Server Down', 'The main server is down!', 'user123', 'operator@example.com', '+0987654321')
