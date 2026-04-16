import pandas as pd
from fpdf import FPDF

class MonthlyReliabilityReport:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def calculate_mtbf(self) -> float:
        # Mean Time Between Failures (MTBF) calculation
        total_uptime = self.data['uptime'].sum()
        total_failures = self.data['failures'].sum()
        return total_uptime / total_failures if total_failures > 0 else float('inf')

    def calculate_prediction_accuracy(self) -> float:
        # Prediction accuracy calculation
        correct_predictions = self.data['correct_predictions'].sum()
        total_predictions = self.data['total_predictions'].sum()
        return (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0.0

    def calculate_cost_savings(self) -> float:
        # Cost savings calculation
        initial_cost = self.data['initial_cost'].sum()
        current_cost = self.data['current_cost'].sum()
        return initial_cost - current_cost

    def generate_pdf_report(self, filename: str):
        # Generate PDF report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Monthly Reliability Report", ln=True, align='C')
        pdf.cell(200, 10, txt=f"MTBF: {self.calculate_mtbf():.2f} hours", ln=True)
        pdf.cell(200, 10, txt=f"Prediction Accuracy: {self.calculate_prediction_accuracy():.2f}%", ln=True)
        pdf.cell(200, 10, txt=f"Cost Savings: ${self.calculate_cost_savings():.2f}", ln=True)
        pdf.output(filename)

    def generate_excel_report(self, filename: str):
        # Generate Excel report
        report_data = {
            'MTBF': [self.calculate_mtbf()],
            'Prediction Accuracy (%)': [self.calculate_prediction_accuracy()],
            'Cost Savings ($)': [self.calculate_cost_savings()]
        }
        report_df = pd.DataFrame(report_data)
        report_df.to_excel(filename, index=False)
