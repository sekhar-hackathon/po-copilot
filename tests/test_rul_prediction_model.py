import unittest
import pandas as pd
import numpy as np
from src.models.rul_prediction_model import RULPredictionModel

class TestRULPredictionModel(unittest.TestCase):
    def setUp(self):
        self.model = RULPredictionModel()
        self.features = pd.DataFrame(np.random.rand(100, 10))
        self.target = pd.Series(np.random.rand(100))

    def test_train(self):
        self.model.train(self.features, self.target)
        self.assertIsNotNone(self.model.model)

    def test_predict(self):
        self.model.train(self.features, self.target)
        predictions = self.model.predict(self.features)
        self.assertEqual(len(predictions), len(self.features))

    def test_save_and_load_model(self):
        self.model.train(self.features, self.target)
        self.model.save_model('test_model.pkl')
        new_model = RULPredictionModel()
        new_model.load_model('test_model.pkl')
        predictions = new_model.predict(self.features)
        self.assertEqual(len(predictions), len(self.features))

if __name__ == '__main__':
    unittest.main()
