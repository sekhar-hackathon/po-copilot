import unittest
from unittest.mock import MagicMock
from alerting_system import AlertingSystem

class TestAlertingSystem(unittest.TestCase):
    def setUp(self):
        email_config = {
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'smtp_user': 'user@example.com',
            'smtp_password': 'password',
            'from_email': 'alerts@example.com'
        }

        sms_config = {
            'account_sid': 'your_account_sid',
            'auth_token': 'your_auth_token',
            'from_number': '+1234567890'
        }

        self.mock_push_service = MagicMock()
        self.alerting_system = AlertingSystem(email_config, sms_config, self.mock_push_service)

    def test_send_email(self):
        self.alerting_system.send_email('Test Subject', 'Test Message', 'test@example.com')
        # No exception means success

    def test_send_sms(self):
        self.alerting_system.send_sms('Test Message', '+0987654321')
        # No exception means success

    def test_send_push_notification(self):
        self.alerting_system.send_push_notification('Test Message', 'user123')
        self.mock_push_service.send_notification.assert_called_once_with('user123', 'Test Message')

    def test_log_alert(self):
        with self.assertLogs(level='INFO') as log:
            self.alerting_system.log_alert('Test Alert', 'Test Message')
            self.assertIn('INFO:root:Alert logged: Test Alert - Test Message', log.output)

    def test_escalate_alert(self):
        with self.assertLogs(level='INFO') as log:
            self.alerting_system.escalate_alert('Test Alert', 'Test Message')
            self.assertIn('INFO:root:Escalation initiated for alert: Test Alert - Test Message', log.output)

    def test_handle_critical_alert(self):
        self.alerting_system.handle_critical_alert('Test Alert', 'Test Message', 'user123', 'test@example.com', '+0987654321')
        self.mock_push_service.send_notification.assert_called_once_with('user123', 'Test Message')

if __name__ == '__main__':
    unittest.main()
