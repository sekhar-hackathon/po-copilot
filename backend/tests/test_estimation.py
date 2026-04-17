import unittest
from app.services.estimation import Estimator

class TestEstimator(unittest.TestCase):

    def setUp(self):
        self.estimator = Estimator()

    def test_suggest_effort(self):
        self.assertEqual(self.estimator.suggest_effort('This is a complex task'), 5)
        self.assertEqual(self.estimator.suggest_effort('This is a medium task'), 3)
        self.assertEqual(self.estimator.suggest_effort('This is a simple task'), 1)

    def test_suggest_priority(self):
        self.assertEqual(self.estimator.suggest_priority('This is an urgent task'), 'High')
        self.assertEqual(self.estimator.suggest_priority('This is an important task'), 'Medium')
        self.assertEqual(self.estimator.suggest_priority('This is a routine task'), 'Low')

    def test_estimate(self):
        result = self.estimator.estimate('This is a complex and urgent task')
        self.assertEqual(result['effort'], 5)
        self.assertEqual(result['priority'], 'High')

if __name__ == '__main__':
    unittest.main()
