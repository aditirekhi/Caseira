import os

from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env", env_ignore_empty=True, extra="ignore"
)


class DataBaseSettings(BaseSettings):
    POSTGRES_PASSWORD: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: str = ""
    POSTGRES_DB: str = ""

    model_config = _base_config

    @property
    def connection_url(self):
        print("-------------------------------- Entering connection_url")
        DATABASE_URL = os.getenv("DATABASE_URL")
        if DATABASE_URL:
            if DATABASE_URL.startswith("postgresql://"):
                return DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
            return DATABASE_URL
        else:
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class SecuritySettings(BaseSettings):
    JWT_ALGORITHM: str = ""
    JWT_SECRET_KEY: str = ""

    model_config = _base_config


db_settings = DataBaseSettings()
jwt_settings = SecuritySettings()
