import csv
from datetime import datetime
from typing import List, Dict

class ReliabilityReportGenerator:
    def __init__(self, data_source: List[Dict[str, float]]):
        self.data_source = data_source

    def generate_report(self) -> List[Dict[str, float]]:
        # Process the data to calculate reliability metrics
        report_data = []
        for entry in self.data_source:
            uptime = entry.get('uptime', 0)
            downtime = entry.get('downtime', 0)
            total_time = uptime + downtime
            reliability = (uptime / total_time) * 100 if total_time > 0 else 0
            report_data.append({
                'date': entry['date'],
                'reliability': reliability
            })
        return report_data

    def export_to_csv(self, report_data: List[Dict[str, float]], file_path: str) -> None:
        # Export the report data to a CSV file
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'reliability'])
            writer.writeheader()
            for data in report_data:
                writer.writerow(data)

if __name__ == "__main__":
    # Example data source
    data_source = [
        {'date': '2023-09-01', 'uptime': 720, 'downtime': 24},
        {'date': '2023-09-02', 'uptime': 715, 'downtime': 29},
        # More data entries...
    ]

    generator = ReliabilityReportGenerator(data_source)
    report = generator.generate_report()
    generator.export_to_csv(report, f'reliability_report_{datetime.now().strftime("%Y_%m")}.csv')
