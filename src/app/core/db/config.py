from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class DBSettings(BaseSettings):
    DATABASE_URL: PostgresDsn
    DB_ECHO: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

db_settings = DBSettings()
