import pandas as pd
from fpdf import FPDF
from typing import List, Dict

class ReliabilityReport:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def calculate_mtbf(self) -> float:
        # Mean Time Between Failures (MTBF) calculation
        total_uptime = self.data['uptime'].sum()
        total_failures = self.data['failures'].sum()
        return total_uptime / total_failures if total_failures > 0 else float('inf')

    def calculate_prediction_accuracy(self) -> float:
        # Prediction accuracy calculation
        correct_predictions = self.data[self.data['predicted'] == self.data['actual']].shape[0]
        total_predictions = self.data.shape[0]
        return (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0.0

    def calculate_cost_savings(self) -> float:
        # Cost savings calculation
        total_savings = self.data['cost_savings'].sum()
        return total_savings

    def generate_report(self) -> Dict[str, float]:
        # Generate the report with calculated metrics
        return {
            'MTBF': self.calculate_mtbf(),
            'Prediction Accuracy': self.calculate_prediction_accuracy(),
            'Cost Savings': self.calculate_cost_savings()
        }

    def export_to_pdf(self, report: Dict[str, float], filename: str):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Monthly Reliability Report', ln=True, align='C')
        pdf.ln(10)
        for key, value in report.items():
            pdf.cell(0, 10, f'{key}: {value}', ln=True)
        pdf.output(filename)

    def export_to_excel(self, report: Dict[str, float], filename: str):
        df = pd.DataFrame([report])
        df.to_excel(filename, index=False)
