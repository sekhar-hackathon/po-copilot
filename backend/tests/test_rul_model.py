import unittest
import numpy as np
from app.services.rul_model import RULModelPrototype

class TestRULModelPrototype(unittest.TestCase):
    def setUp(self):
        self.model = RULModelPrototype()
        self.X = np.random.rand(100, 10)  # 100 samples, 10 features
        self.y = np.random.rand(100)  # 100 target values

    def test_train(self):
        try:
            self.model.train(self.X, self.y)
        except Exception as e:
            self.fail(f'Training failed with exception {e}')

    def test_predict(self):
        self.model.train(self.X, self.y)
        predictions = self.model.predict(self.X)
        self.assertEqual(predictions.shape, (100,))

if __name__ == '__main__':
    unittest.main()
