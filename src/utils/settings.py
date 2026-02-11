from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

# Set up PATH
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "src" / "templates"
STATIC_DIR = BASE_DIR / "src" / "static"

def get_env_file() -> str:
    return find_dotenv(".env", raise_error_if_not_found=False)

class Settings(BaseSettings):
    """
    Application settings that can be configured via:
    1. Environment variables (highest priority)
    2. .env file
    3. Default values (lowest priority)
    
    Environment variable names are automatically derived from field names.
    For example: postgres_db -> POSTGRES_DB, postgres_user -> POSTGRES_USER
    """

    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        case_sensitive=False,
        extra="ignore",
    )

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()