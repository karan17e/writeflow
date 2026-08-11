import logging
from typing import Optional, List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"
BACKEND_ENV_FILE = BASE_DIR / "backend" / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "WriteFlow API"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = "*"

    DATABASE_URL: str = "sqlite+aiosqlite:///./linkedin_posts.db"

    # LLM Provider: "groq", "openai", "gemini", "anthropic", "mock"
    LLM_PROVIDER: str = "groq"

    # API Keys (Never return or expose to frontend)
    GROQ_API_KEY: Optional[str] = ""
    OPENAI_API_KEY: Optional[str] = ""
    GEMINI_API_KEY: Optional[str] = ""
    ANTHROPIC_API_KEY: Optional[str] = ""

    model_config = SettingsConfigDict(
        env_file=(str(BACKEND_ENV_FILE), str(ENV_FILE), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        origins = [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
            "https://writeflow-git-main-karan-de-bande.vercel.app",
            "https://writeflow-karan-de-bande.vercel.app",
            "https://writeflow.vercel.app",
        ]
        if self.ALLOWED_ORIGINS:
            custom_origins = [o.strip().rstrip("/") for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]
            for co in custom_origins:
                if co != "*" and co not in origins:
                    origins.append(co)
        return origins


settings = Settings()

# Setup central logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("writeflow")
