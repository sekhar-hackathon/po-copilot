class SMSSender:
    def send_sms(self, recipients: list, message: str):
        # Logic to send SMS
        for recipient in recipients:
            print(f"SMS sent to {recipient}: {message}")
