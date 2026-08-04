# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NewsFlow AI"
    app_env: str = "development"
    debug: bool = True

    api_v1_prefix: str = "/api/v1"

    database_url: str = ""
    redis_url: str = ""

    openai_api_key: str = ""
    # gemini_api_key: str = ""

    wordpress_url: str = ""
    wordpress_username: str = ""
    wordpress_application_password: str = ""

    cloudinary_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()