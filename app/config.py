from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    WHISPER_MODEL: str = "small.en"
    ALLOW_ORIGINS: List[AnyHttpUrl | str] = []  # e.g., ["https://your.vercel.app"] in production

    class Config:
        env_file = ".env"

settings = Settings()
