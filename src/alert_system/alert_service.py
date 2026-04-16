from typing import List
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
import requests

class AlertService:
    def __init__(self, email_config: dict, sms_config: dict, push_config: dict):
        self.email_config = email_config
        self.sms_config = sms_config
        self.push_config = push_config

    def send_email(self, recipients: List[str], subject: str, message: str):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.email_config['sender']
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.sendmail(self.email_config['sender'], recipients, msg.as_string())

    def send_sms(self, phone_numbers: List[str], message: str):
        client = Client(self.sms_config['account_sid'], self.sms_config['auth_token'])
        for number in phone_numbers:
            client.messages.create(
                body=message,
                from_=self.sms_config['from_number'],
                to=number
            )

    def send_push_notification(self, device_tokens: List[str], message: str):
        headers = {
            'Authorization': f'Bearer {self.push_config['api_key']}',
            'Content-Type': 'application/json'
        }
        payload = {
            'tokens': device_tokens,
            'notification': {
                'title': 'Critical Alert',
                'body': message
            }
        }
        requests.post(self.push_config['api_url'], json=payload, headers=headers)

    def escalate_alert(self, alert_id: str):
        # Logic to escalate alert if not acknowledged
        pass
