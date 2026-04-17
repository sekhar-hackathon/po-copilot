from fastapi import APIRouter
from backend.app.services.bearing_health import get_bearing_health_scores

router = APIRouter()

@router.get('/bearing-health-scores')
def bearing_health_scores():
    return get_bearing_health_scores()
