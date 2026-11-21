"""
Configuration module for the Curriculum Intelligence System (CIS).
Loads settings from environment variables using Pydantic Settings.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = "Curriculum Intelligence System"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Security & JWT
    SECRET_KEY: str = Field(
        default="cis-super-secret-production-grade-key-at-least-32-chars-long-2026",
        description="JWT secret key"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/cis_db",
        description="Primary async PostgreSQL URL. Falls back automatically to local SQLite when PostgreSQL is unavailable."
    )
    SQLITE_FALLBACK_URL: str = "sqlite+aiosqlite:///./cis_local.db"

    # LLM Provider Configuration
    LLM_PROVIDER: str = Field(default="gemini", description="gemini | openai | claude | local")
    LLM_API_KEY: Optional[str] = Field(default=None, description="API key for the selected LLM provider")
    LLM_MODEL: str = Field(default="gemini-2.0-flash", description="Default model identifier")

    # Embeddings Provider Configuration
    EMBEDDING_PROVIDER: str = Field(default="local", description="local | gemini | openai")
    EMBEDDING_API_KEY: Optional[str] = None
    EMBEDDING_MODEL: str = "text-embedding-004"
    EMBEDDING_DIMENSION: int = 768

    # External Data Integrations
    ADZUNA_APP_ID: Optional[str] = None
    ADZUNA_APP_KEY: Optional[str] = None

    WEB_SEARCH_PROVIDER: Optional[str] = None  # e.g. serpapi, tavily
    WEB_SEARCH_API_KEY: Optional[str] = None

    # MCP Server
    MCP_SERVER_URL: str = "http://localhost:8001"

    # OpenClaw Gateway Service
    OPENCLAW_GATEWAY_URL: str = "http://localhost:18789"
    OPENCLAW_GATEWAY_TOKEN: Optional[str] = None

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    # Upload and Document Processing
    UPLOAD_DIR: str = "data/uploads"
    MAX_UPLOAD_SIZE_MB: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
