
from fastapi import APIRouter, HTTPException
from backend.app.services.notification_service import NotificationService

router = APIRouter()
notification_service = NotificationService()

@router.post("/alerts")
async def create_alert(health_score: float, threshold: float, email: str, phone: str):
    try:
        notification_service.notify(health_score, threshold, email, phone)
        return {"message": "Alert processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
