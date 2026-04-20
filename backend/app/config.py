from pydantic import BaseSettings

class Settings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

settings = Settings()
