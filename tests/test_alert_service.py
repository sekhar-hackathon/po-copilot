import unittest
from unittest.mock import patch
from alert_system.alert_service import AlertService

class TestAlertService(unittest.TestCase):
    def setUp(self):
        self.email_config = {
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'username': 'user@example.com',
            'password': 'password',
            'sender': 'alerts@example.com'
        }
        self.sms_config = {
            'account_sid': 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'auth_token': 'your_auth_token',
            'from_number': '+1234567890'
        }
        self.push_config = {
            'api_key': 'your_api_key',
            'api_url': 'https://api.pushservice.com/send'
        }
        self.alert_service = AlertService(self.email_config, self.sms_config, self.push_config)

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        self.alert_service.send_email(['recipient@example.com'], 'Test Subject', 'Test Message')
        mock_smtp.assert_called_with('smtp.example.com', 587)

    @patch('twilio.rest.Client')
    def test_send_sms(self, mock_client):
        self.alert_service.send_sms(['+19876543210'], 'Test SMS Message')
        mock_client.return_value.messages.create.assert_called()

    @patch('requests.post')
    def test_send_push_notification(self, mock_post):
        self.alert_service.send_push_notification(['device_token'], 'Test Push Message')
        mock_post.assert_called()

if __name__ == '__main__':
    unittest.main()
