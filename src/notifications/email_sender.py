class EmailSender:
    def send_email(self, recipients: list, subject: str, body: str):
        # Logic to send email
        for recipient in recipients:
            print(f"Email sent to {recipient}: Subject: {subject}, Body: {body}")
