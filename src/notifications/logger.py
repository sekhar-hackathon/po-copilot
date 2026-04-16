from datetime import datetime

class Logger:
    def log_alert(self, bearing_id: int, health_score: float, timestamp: datetime):
        # Logic to log the alert
        print(f"Alert logged for bearing {bearing_id} with health score {health_score} at {timestamp}")
