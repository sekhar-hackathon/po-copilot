
import unittest
from unittest.mock import patch
from backend.app.services.notification_service import NotificationService

class TestNotificationService(unittest.TestCase):
    @patch('backend.app.services.notification_service.smtplib.SMTP')
    @patch('backend.app.services.notification_service.Client')
    def test_notify(self, mock_twilio_client, mock_smtp):
        notification_service = NotificationService()
        notification_service.notify(health_score=50, threshold=60, email='test@example.com', phone='+1234567890')

        # Check email sending
        mock_smtp.assert_called_once()
        mock_smtp.return_value.sendmail.assert_called_once()

        # Check SMS sending
        mock_twilio_client.assert_called_once()
        mock_twilio_client.return_value.messages.create.assert_called_once()

if __name__ == '__main__':
    unittest.main()
