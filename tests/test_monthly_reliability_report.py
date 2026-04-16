import unittest
import pandas as pd
from src.reports.monthly_reliability_report import MonthlyReliabilityReport

class TestMonthlyReliabilityReport(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.data = pd.DataFrame({
            'uptime': [100, 200, 150],
            'failures': [2, 1, 3],
            'correct_predictions': [90, 180, 135],
            'total_predictions': [100, 200, 150],
            'initial_cost': [1000, 2000, 1500],
            'current_cost': [800, 1800, 1300]
        })
        self.report = MonthlyReliabilityReport(self.data)

    def test_calculate_mtbf(self):
        self.assertAlmostEqual(self.report.calculate_mtbf(), 75.0)

    def test_calculate_prediction_accuracy(self):
        self.assertAlmostEqual(self.report.calculate_prediction_accuracy(), 90.0)

    def test_calculate_cost_savings(self):
        self.assertAlmostEqual(self.report.calculate_cost_savings(), 600.0)

    def test_generate_pdf_report(self):
        # Test PDF generation (file creation)
        self.report.generate_pdf_report('test_report.pdf')
        with open('test_report.pdf', 'rb') as f:
            self.assertTrue(len(f.read()) > 0)

    def test_generate_excel_report(self):
        # Test Excel generation (file creation)
        self.report.generate_excel_report('test_report.xlsx')
        with open('test_report.xlsx', 'rb') as f:
            self.assertTrue(len(f.read()) > 0)

if __name__ == '__main__':
    unittest.main()
