import pandas as pd
from fpdf import FPDF
from typing import List, Dict

class ReportGenerator:
    def __init__(self, data: List[Dict]):
        self.data = data

    def generate_excel_report(self, file_path: str) -> None:
        df = pd.DataFrame(self.data)
        df.to_excel(file_path, index=False)

    def generate_pdf_report(self, file_path: str) -> None:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for item in self.data:
            for key, value in item.items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
            pdf.cell(200, 10, txt="", ln=True)  # Add a blank line between records
        pdf.output(file_path)

    def calculate_mtbf(self) -> float:
        total_uptime = sum(item['uptime'] for item in self.data)
        total_failures = sum(item['failures'] for item in self.data)
        return total_uptime / total_failures if total_failures > 0 else 0

    def calculate_cost_savings(self) -> float:
        total_cost = sum(item['cost'] for item in self.data)
        total_savings = sum(item['savings'] for item in self.data)
        return total_savings - total_cost
