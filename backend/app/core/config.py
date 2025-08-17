"""Configuration settings for the backend."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database
    database_url: str = "postgresql+asyncpg://pos_user:pos_password@localhost:5432/pos_db"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Google OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"

    # Application
    app_name: str = "POS System"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Redis (for session storage)
    redis_url: str = "redis://localhost:6379"

    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
