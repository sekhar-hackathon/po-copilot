from fastapi import APIRouter, HTTPException
from backend.app.services.report_generator import ReportGenerator

router = APIRouter()

@router.post("/generate-report")
async def generate_report(data: List[Dict], format: str):
    report_generator = ReportGenerator(data)
    mtbf = report_generator.calculate_mtbf()
    cost_savings = report_generator.calculate_cost_savings()

    if format == 'excel':
        file_path = 'monthly_report.xlsx'
        report_generator.generate_excel_report(file_path)
    elif format == 'pdf':
        file_path = 'monthly_report.pdf'
        report_generator.generate_pdf_report(file_path)
    else:
        raise HTTPException(status_code=400, detail="Invalid format")

    return {
        "file_path": file_path,
        "mtbf": mtbf,
        "cost_savings": cost_savings
    }
