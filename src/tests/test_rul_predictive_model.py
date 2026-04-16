import unittest
import pandas as pd
import numpy as np
from models.rul_predictive_model import RULPredictiveModel

class TestRULPredictiveModel(unittest.TestCase):
    def setUp(self):
        # Create a small dataset for testing
        self.X = pd.DataFrame({
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100),
            'feature3': np.random.rand(100)
        })
        self.y = pd.Series(np.random.rand(100))
        self.model = RULPredictiveModel()

    def test_train(self):
        self.model.train(self.X, self.y)
        self.assertIsNotNone(self.model.model)

    def test_predict(self):
        self.model.train(self.X, self.y)
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), len(self.y))

    def test_save_and_load_model(self):
        self.model.train(self.X, self.y)
        self.model.save_model('test_model.pkl')
        self.model.load_model('test_model.pkl')
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), len(self.y))

if __name__ == '__main__':
    unittest.main()
