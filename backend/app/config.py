from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "WriteFlow API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite+aiosqlite:///./linkedin_posts.db"

    # LLM Settings: "groq", "mock", "openai", "gemini", "anthropic"
    LLM_PROVIDER: str = "groq"

    # API Keys
    GROQ_API_KEY: Optional[str] = ""
    OPENAI_API_KEY: Optional[str] = ""
    GEMINI_API_KEY: Optional[str] = ""
    ANTHROPIC_API_KEY: Optional[str] = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
