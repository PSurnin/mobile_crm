from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_SECRET_KEY: str = "default_secret"
    BOT_USERNAME: str = "бот"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
