"""src/config.py"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environvent connection Class"""

    env_name: str = "ENV_NAME"
    base_url: str = "BASE_URL"
    db_url: str = "DB_URL"
    secret: str = "SECRET"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Function to get settings from envirinment to project"""
    settings = Settings()
    return settings
