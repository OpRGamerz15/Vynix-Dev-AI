from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Nexora AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me"
    DATABASE_URL: str = "sqlite:///./nexora.db"
    JWT_SECRET_KEY: str = "change-me-jwt"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEFAULT_REQUESTS_PER_MINUTE: int = 20
    DEFAULT_REQUESTS_PER_DAY: int = 500
    MAX_CONCURRENT_REQUESTS: int = 5
    ENABLE_PAID_PROVIDERS: bool = False
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    INITIAL_ADMIN_EMAIL: str = "admin@nexora.local"
    INITIAL_ADMIN_PASSWORD: str = "change-me-immediately"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()