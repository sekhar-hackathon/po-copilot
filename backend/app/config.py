import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    ado_org_url: str = os.getenv("ADO_ORG_URL", "")
    ado_pat: str = os.getenv("ADO_PAT", "")
    ado_project: str = os.getenv("ADO_PROJECT", "")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_owner: str = os.getenv("GITHUB_OWNER", "")
    github_repo: str = os.getenv("GITHUB_REPO", "po-copilot")
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    upload_dir: str = "./uploads"


settings = Settings()
