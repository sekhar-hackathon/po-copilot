import unittest
import pandas as pd
from src.reports.monthly_reliability_report import ReliabilityReport

class TestReliabilityReport(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.data = pd.DataFrame({
            'uptime': [100, 200, 300],
            'failures': [1, 2, 1],
            'predicted': [1, 0, 1],
            'actual': [1, 0, 0],
            'cost_savings': [1000, 2000, 1500]
        })
        self.report = ReliabilityReport(self.data)

    def test_calculate_mtbf(self):
        self.assertAlmostEqual(self.report.calculate_mtbf(), 200.0)

    def test_calculate_prediction_accuracy(self):
        self.assertAlmostEqual(self.report.calculate_prediction_accuracy(), 66.66666666666666)

    def test_calculate_cost_savings(self):
        self.assertEqual(self.report.calculate_cost_savings(), 4500)

    def test_generate_report(self):
        expected_report = {
            'MTBF': 200.0,
            'Prediction Accuracy': 66.66666666666666,
            'Cost Savings': 4500
        }
        self.assertEqual(self.report.generate_report(), expected_report)

if __name__ == '__main__':
    unittest.main()
