import os
import sys
import types
import json
import asyncio
from io import BytesIO

import pytest
from fastapi import UploadFile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class DummyModel:
    """Simple stand-in for the Whisper model used in tests."""

    def transcribe(self, path: str):
        return {"text": "test transcription"}


def _load_model(name: str) -> "DummyModel":
    return DummyModel()


# Inject a lightweight fake "whisper" module before the application imports it.
sys.modules["whisper"] = types.SimpleNamespace(load_model=_load_model)

from app.api import transcribe as transcribe_api  # noqa: E402
from main import health as root_health  # noqa: E402


@pytest.fixture
def dummy_model() -> DummyModel:
    return DummyModel()


@pytest.fixture
def upload_factory():
    def _factory(data: bytes, filename: str, content_type: str) -> UploadFile:
        return UploadFile(
            filename=filename,
            file=BytesIO(data),
            headers={"content-type": content_type},
        )

    return _factory


def test_health_route():
    assert root_health() == {"status": "ok"}


def test_transcribe_success(upload_factory, dummy_model):
    with open("voice-test.mp3", "rb") as f:
        upload = upload_factory(f.read(), "voice-test.mp3", "audio/mpeg")

    result = asyncio.run(
        transcribe_api.transcribe(file=upload, model=dummy_model)
    )

    assert result.status_code == 200
    data = json.loads(result.body)
    assert data["text"] == "test transcription"
    assert isinstance(data["duration_ms"], int)


@pytest.mark.parametrize(
    "data,filename,content_type,expected_status",
    [
        (b"data", "test.txt", "text/plain", 415),
        (
            b"0" * (transcribe_api.MAX_UPLOAD_SIZE + 1),
            "big.mp3",
            "audio/mpeg",
            413,
        ),
    ],
)
def test_transcribe_invalid_uploads(
    data, filename, content_type, expected_status, upload_factory, dummy_model
):
    upload = upload_factory(data, filename, content_type)

    with pytest.raises(transcribe_api.HTTPException) as exc:
        asyncio.run(transcribe_api.transcribe(file=upload, model=dummy_model))

    assert exc.value.status_code == expected_status
