import unittest
from unittest.mock import MagicMock
from src.notifications.alert_service import AlertService

class TestAlertService(unittest.TestCase):
    def setUp(self):
        self.push_notifier = MagicMock()
        self.sms_sender = MagicMock()
        self.email_sender = MagicMock()
        self.logger = MagicMock()
        self.alert_service = AlertService(self.push_notifier, self.sms_sender, self.email_sender, self.logger)

    def test_send_alerts_critical(self):
        supervisors = ['supervisor1@example.com', 'supervisor2@example.com']
        self.alert_service.send_alerts(bearing_id=1, health_score=15.0, supervisors=supervisors)

        self.push_notifier.send_push_notification.assert_called_once()
        self.sms_sender.send_sms.assert_called_once_with(supervisors, unittest.mock.ANY)
        self.email_sender.send_email.assert_called_once_with(supervisors, unittest.mock.ANY, unittest.mock.ANY)
        self.logger.log_alert.assert_called_once()

    def test_send_alerts_non_critical(self):
        supervisors = ['supervisor1@example.com', 'supervisor2@example.com']
        self.alert_service.send_alerts(bearing_id=1, health_score=25.0, supervisors=supervisors)

        self.push_notifier.send_push_notification.assert_not_called()
        self.sms_sender.send_sms.assert_not_called()
        self.email_sender.send_email.assert_not_called()
        self.logger.log_alert.assert_not_called()

if __name__ == '__main__':
    unittest.main()
