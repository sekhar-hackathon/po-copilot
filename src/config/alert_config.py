class AlertConfig:
    PUSH_NOTIFICATION_ENABLED = True
    SMS_NOTIFICATION_ENABLED = True
    EMAIL_NOTIFICATION_ENABLED = True

    PUSH_NOTIFICATION_SERVICE_URL = 'https://api.pushservice.com/send'
    SMS_SERVICE_URL = 'https://api.smsservice.com/send'
    EMAIL_SERVICE_URL = 'https://api.emailservice.com/send'

    EMAIL_FROM_ADDRESS = 'alerts@company.com'
    EMAIL_SUBJECT = 'Critical Bearing Health Alert'

    @staticmethod
    def get_push_notification_payload(message: str) -> dict:
        return {
            'title': 'Critical Alert',
            'body': message
        }

    @staticmethod
    def get_sms_payload(phone_number: str, message: str) -> dict:
        return {
            'to': phone_number,
            'message': message
        }

    @staticmethod
    def get_email_payload(to_email: str, message: str) -> dict:
        return {
            'from': AlertConfig.EMAIL_FROM_ADDRESS,
            'to': to_email,
            'subject': AlertConfig.EMAIL_SUBJECT,
            'body': message
        }
