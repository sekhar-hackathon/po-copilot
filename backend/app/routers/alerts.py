from fastapi import APIRouter, HTTPException
from backend.app.services.notification_service import NotificationService

router = APIRouter()
notification_service = NotificationService()

@router.post("/alerts/notify")
async def notify_maintenance_supervisor(alert_id: str, email: str, phone_number: str, subject: str, message: str):
    try:
        notification_service.notify(email, phone_number, subject, message)
        notification_service.log_acknowledgment(alert_id)
        return {"status": "success", "message": "Notification sent and acknowledgment logged."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
