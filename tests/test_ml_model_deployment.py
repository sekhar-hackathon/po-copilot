import unittest
from datetime import datetime, timedelta
from src.ml_model_deployment import MLModelDeployment

class TestMLModelDeployment(unittest.TestCase):
    def setUp(self):
        self.deployment = MLModelDeployment(model_name='TestModel')

    def test_retrain_model(self):
        self.deployment.retrain_model()
        self.assertTrue(datetime.now() - self.deployment.last_trained < timedelta(seconds=1))

    def test_should_retrain(self):
        self.deployment.last_trained = datetime.now() - timedelta(days=31)
        self.assertTrue(self.deployment.should_retrain())

    def test_set_and_get_alert_threshold(self):
        self.deployment.set_alert_threshold('TypeA', 0.75)
        self.assertEqual(self.deployment.get_alert_threshold('TypeA'), 0.75)

    def test_ab_test(self):
        model_a = {'name': 'ModelA', 'performance': 0.8}
        model_b = {'name': 'ModelB', 'performance': 0.82}
        winner = self.deployment.ab_test(model_a, model_b)
        self.assertEqual(winner, 'ModelB')

if __name__ == '__main__':
    unittest.main()
