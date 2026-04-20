from fastapi import APIRouter, HTTPException
from backend.app.services.notification_service import NotificationService

router = APIRouter()
notification_service = NotificationService()

@router.post("/alerts/notify")
async def notify_critical_alert(bearing_id: str, health_score: float, threshold: float, phone_number: str, email: str):
    """Endpoint to notify when a bearing health score is below threshold"""
    if health_score < threshold:
        message = f"Critical Alert: Bearing {bearing_id} health score is {health_score}, below threshold {threshold}."
        try:
            notification_service.send_sms(phone_number, message)
            notification_service.send_email(email, "Critical Bearing Alert", message)
            notification_service.log_acknowledgment(bearing_id)
            return {"status": "success", "message": "Notifications sent."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"status": "ok", "message": "Health score is above threshold."}
