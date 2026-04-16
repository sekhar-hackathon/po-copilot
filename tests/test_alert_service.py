import unittest
from unittest.mock import patch
from src.services.alert_service import AlertService

class TestAlertService(unittest.TestCase):
    @patch('src.services.alert_service.requests.post')
    def test_send_push_notification(self, mock_post):
        AlertService.send_push_notification('Test push message')
        mock_post.assert_called_once()

    @patch('src.services.alert_service.requests.post')
    def test_send_sms(self, mock_post):
        AlertService.send_sms('+1234567890', 'Test SMS message')
        mock_post.assert_called_once()

    @patch('src.services.alert_service.requests.post')
    def test_send_email(self, mock_post):
        AlertService.send_email('test@example.com', 'Test email message')
        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()
