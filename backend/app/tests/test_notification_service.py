import unittest
from unittest.mock import patch
from backend.app.services.notification_service import NotificationService

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        self.notification_service = NotificationService()

    @patch('backend.app.services.notification_service.Client')
    def test_send_sms(self, MockClient):
        mock_twilio_client = MockClient.return_value
        self.notification_service.send_sms('+1234567890', 'Test Message')
        mock_twilio_client.messages.create.assert_called_once_with(
            body='Test Message',
            from_='YourTwilioNumber',
            to='+1234567890'
        )

    @patch('smtplib.SMTP')
    def test_send_email(self, MockSMTP):
        mock_smtp = MockSMTP.return_value
        self.notification_service.send_email('test@example.com', 'Test Subject', 'Test Message')
        mock_smtp.sendmail.assert_called_once()

    def test_log_acknowledgment(self):
        with patch('builtins.print') as mock_print:
            self.notification_service.log_acknowledgment('alert123')
            mock_print.assert_called_once_with('Alert alert123 acknowledged.')

if __name__ == '__main__':
    unittest.main()
