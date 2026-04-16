import unittest
from src.reports.reliability_report_generator import ReliabilityReportGenerator

class TestReliabilityReportGenerator(unittest.TestCase):
    def setUp(self):
        self.data_source = [
            {'date': '2023-09-01', 'uptime': 720, 'downtime': 24},
            {'date': '2023-09-02', 'uptime': 715, 'downtime': 29},
        ]
        self.generator = ReliabilityReportGenerator(self.data_source)

    def test_generate_report(self):
        report = self.generator.generate_report()
        self.assertEqual(len(report), 2)
        self.assertAlmostEqual(report[0]['reliability'], 96.77, places=2)
        self.assertAlmostEqual(report[1]['reliability'], 96.10, places=2)

    def test_export_to_csv(self):
        report = self.generator.generate_report()
        self.generator.export_to_csv(report, 'test_reliability_report.csv')
        with open('test_reliability_report.csv', 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 3)  # Header + 2 data lines

if __name__ == '__main__':
    unittest.main()
