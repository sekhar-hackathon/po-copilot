
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from backend.app.config import EMAIL_CONFIG, TWILIO_CONFIG

class NotificationService:
    def __init__(self):
        self.email_config = EMAIL_CONFIG
        self.twilio_config = TWILIO_CONFIG

    def send_email(self, subject: str, body: str, to_email: str) -> None:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_config['sender_email']
        msg['To'] = to_email

        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['password'])
            server.sendmail(self.email_config['sender_email'], to_email, msg.as_string())

    def send_sms(self, body: str, to_phone: str) -> None:
        client = Client(self.twilio_config['account_sid'], self.twilio_config['auth_token'])
        message = client.messages.create(
            body=body,
            from_=self.twilio_config['from_phone'],
            to=to_phone
        )

    def notify(self, health_score: float, threshold: float, email: str, phone: str) -> None:
        if health_score < threshold:
            subject = "Critical Alert: Bearing Health Score"
            body = f"Alert! The bearing health score has dropped below the threshold. Current score: {health_score}"
            self.send_email(subject, body, email)
            self.send_sms(body, phone)
            self.log_acknowledgment(health_score, email, phone)

    def log_acknowledgment(self, health_score: float, email: str, phone: str) -> None:
        # Log the acknowledgment of the alert
        print(f"Alert acknowledged for health score {health_score}. Notifications sent to {email} and {phone}.")
