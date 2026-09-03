"""Application configuration.

Values are read from environment variables (or a local ``.env`` file) by
``pydantic-settings``. Every setting has a safe default so the app can start
with no configuration at all: ``DATABASE_URL`` falls back to a local SQLite
file, which is what lets ``import app.main`` work with no database running.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "TaskFlow"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False

    # Database. Falls back to SQLite so the app runs with zero config.
    database_url: str = "sqlite:///./taskflow.db"

    # Auth / JWT
    secret_key: str = "dev-insecure-secret-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS: origins allowed to call the API from a browser.
    backend_cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
    ]


settings = Settings()
