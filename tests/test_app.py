import os
import sys
import types
import asyncio
from io import BytesIO

from fastapi import UploadFile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class DummyModel:
    """Simple stand-in for the Whisper model used in tests."""

    def transcribe(self, path: str):
        return {"text": "test transcription"}


def _load_model(name: str) -> DummyModel:
    return DummyModel()


# Inject a lightweight fake "whisper" module before the application imports it.
sys.modules["whisper"] = types.SimpleNamespace(load_model=_load_model)

from app.api import transcribe as transcribe_api  # noqa: E402
from main import health as root_health  # noqa: E402


def test_health_route():
    assert root_health() == {"status": "ok"}


def test_transcribe_success():
    with open("voice-test.mp3", "rb") as f:
        upload = UploadFile(
            filename="voice-test.mp3",
            file=BytesIO(f.read()),
            headers={"content-type": "audio/mpeg"},
        )

    result = asyncio.run(
        transcribe_api.transcribe(file=upload, model=DummyModel())
    )

    assert result.status_code == 200
    data = result.body
    # body is bytes; parse JSON
    import json

    data = json.loads(data)
    assert data["text"] == "test transcription"
    assert isinstance(data["duration_ms"], int)


def test_transcribe_unsupported_type():
    upload = UploadFile(
        filename="test.txt",
        file=BytesIO(b"data"),
        headers={"content-type": "text/plain"},
    )

    import pytest

    with pytest.raises(transcribe_api.HTTPException) as exc:
        asyncio.run(transcribe_api.transcribe(file=upload, model=DummyModel()))

    assert exc.value.status_code == 415


def test_transcribe_file_too_large():
    big_bytes = BytesIO(b"0" * (transcribe_api.MAX_UPLOAD_SIZE + 1))
    upload = UploadFile(
        filename="big.mp3",
        file=big_bytes,
        headers={"content-type": "audio/mpeg"},
    )

    import pytest

    with pytest.raises(transcribe_api.HTTPException) as exc:
        asyncio.run(transcribe_api.transcribe(file=upload, model=DummyModel()))

    assert exc.value.status_code == 413
