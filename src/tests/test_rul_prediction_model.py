import unittest
import pandas as pd
import numpy as np
from src.models.rul_prediction_model import RULPredictionModel

class TestRULPredictionModel(unittest.TestCase):
    def setUp(self):
        self.model = RULPredictionModel(alert_thresholds={'typeA': 50, 'typeB': 30})
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'RUL': [50, 40, 30, 20, 10]
        })

    def test_train(self):
        self.model.train(self.data, target_column='RUL')
        predictions = self.model.predict(self.data.drop(columns=['RUL']))
        self.assertEqual(len(predictions), len(self.data))

    def test_alerts(self):
        predictions = np.array([60, 45, 25, 15, 5])
        alerts = self.model.check_alerts(predictions, 'typeA')
        self.assertEqual(alerts, [2, 3, 4])

if __name__ == '__main__':
    unittest.main()
