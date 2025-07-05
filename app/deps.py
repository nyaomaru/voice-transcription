import whisper
from functools import lru_cache
from .config import settings

@lru_cache  # Cache the model to avoid loading it multiple times
def get_whisper_model():
    return whisper.load_model(settings.WHISPER_MODEL)
