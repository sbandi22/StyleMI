"""
StyleMI Configuration
Loads environment variables and defines application settings.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "StyleMI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./stylemi.db"
    OPENWEATHER_API_KEY: str = "demo_key"
    WEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"
    CLIP_MODEL: str = "ViT-B/32"
    UPLOAD_DIR: str = "backend/uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    RECOMMENDATION_LIMIT: int = 20
    SIMILARITY_THRESHOLD: float = 0.6
    ENSEMBLE_WEIGHTS: list = [0.30, 0.25, 0.20, 0.15, 0.10]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
