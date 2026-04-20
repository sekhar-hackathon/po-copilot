import smtplib
from twilio.rest import Client
from backend.app.config import EMAIL_CONFIG, TWILIO_CONFIG

class NotificationService:
    def __init__(self):
        self.email_server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        self.email_server.starttls()
        self.email_server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
        self.twilio_client = Client(TWILIO_CONFIG['account_sid'], TWILIO_CONFIG['auth_token'])

    def send_email(self, to_address: str, subject: str, message: str) -> None:
        email_message = f"Subject: {subject}\n\n{message}"
        self.email_server.sendmail(EMAIL_CONFIG['from_address'], to_address, email_message)

    def send_sms(self, to_number: str, message: str) -> None:
        self.twilio_client.messages.create(
            body=message,
            from_=TWILIO_CONFIG['from_number'],
            to=to_number
        )

    def notify(self, email: str, phone_number: str, subject: str, message: str) -> None:
        self.send_email(email, subject, message)
        self.send_sms(phone_number, message)

    def log_acknowledgment(self, alert_id: str) -> None:
        # Log the acknowledgment of the alert
        print(f"Alert {alert_id} acknowledged.")
