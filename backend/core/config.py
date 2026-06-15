from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
