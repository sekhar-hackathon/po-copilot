import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from backend.app.config import settings

class NotificationService:
    def __init__(self):
        self.twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password

    def send_sms(self, to_number: str, message: str) -> None:
        """Send SMS using Twilio API"""
        self.twilio_client.messages.create(
            body=message,
            from_=settings.twilio_phone_number,
            to=to_number
        )

    def send_email(self, to_email: str, subject: str, message: str) -> None:
        """Send email using SMTP"""
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = to_email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_user, to_email, msg.as_string())

    def log_acknowledgment(self, alert_id: str) -> None:
        """Log acknowledgment of alert"""
        # This function would ideally log to a database or a file
        print(f"Alert {alert_id} acknowledged.")
