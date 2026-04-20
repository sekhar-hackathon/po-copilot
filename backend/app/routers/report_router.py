from fastapi import APIRouter, HTTPException
from backend.app.services.report_generator import ReportGenerator
import pandas as pd

router = APIRouter()

@router.post('/generate-report')
async def generate_report(data: dict):
    try:
        # Convert incoming data to DataFrame
        df = pd.DataFrame(data)
        report_generator = ReportGenerator(df)
        report_paths = report_generator.generate_monthly_report()
        return report_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
