from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    WHISPER_MODEL: str = "small.en"
    ALLOW_ORIGINS: List[AnyHttpUrl | str] = ["*"]  # Set to ["https://your.vercel.app"] for production

    class Config:
        env_file = ".env"

settings = Settings()
