import unittest
import pandas as pd
import numpy as np
from app.services.rul_prediction import RULPredictionModel

class TestRULPredictionModel(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.data = pd.DataFrame({
            'sensor_1': [0.1, 0.2, 0.3, 0.4],
            'sensor_2': [0.2, 0.3, 0.4, 0.5],
            'rul': [10, 20, 30, 40]
        })
        self.model = RULPredictionModel()

    def test_train(self):
        self.model.train(self.data, 'rul')
        self.assertTrue(hasattr(self.model, 'model'))

    def test_predict(self):
        self.model.train(self.data, 'rul')
        input_data = np.array([[0.15, 0.25]])
        prediction = self.model.predict(input_data)
        self.assertEqual(prediction.shape, (1,))

if __name__ == '__main__':
    unittest.main()
