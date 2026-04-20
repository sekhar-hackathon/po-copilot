import unittest
from unittest.mock import patch
from backend.app.services.notification_service import NotificationService

class TestNotificationService(unittest.TestCase):
    @patch('backend.app.services.notification_service.smtplib.SMTP')
    @patch('backend.app.services.notification_service.Client')
    def test_notify(self, mock_twilio_client, mock_smtp):
        notification_service = NotificationService()
        notification_service.notify('test@example.com', '+1234567890', 'Test Subject', 'Test Message')
        mock_smtp.return_value.sendmail.assert_called_once()
        mock_twilio_client.return_value.messages.create.assert_called_once()

    @patch('builtins.print')
    def test_log_acknowledgment(self, mock_print):
        notification_service = NotificationService()
        notification_service.log_acknowledgment('alert123')
        mock_print.assert_called_once_with('Alert alert123 acknowledged.')

if __name__ == '__main__':
    unittest.main()
