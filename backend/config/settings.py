from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API
    api_title: str = "Legal Aid Case Continuity Agent"
    api_version: str = "0.1.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: Optional[str] = None
    database_echo: bool = False

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Hindsight Integration
    hindsight_api_key: Optional[str] = None
    hindsight_api_url: Optional[str] = None


settings = Settings()

