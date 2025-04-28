from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    # Application Settings
    APP_ENV: str = "dev"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # External Services
    OPENAI_API_KEY: str = ""  # Will be loaded from environment variable

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_CFG: str = "log_conf.yaml"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Export settings
__all__ = ["settings"]
