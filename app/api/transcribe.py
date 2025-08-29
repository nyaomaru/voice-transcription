import os, tempfile, shutil, logging, time
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.deps import get_whisper_model

log = logging.getLogger(__name__)
router = APIRouter()

# Maximum allowed upload size in bytes (10 MB)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024


class TranscribeResponse(BaseModel):
    text: str
    duration_ms: int


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(
    file: UploadFile = File(...),
    model = Depends(get_whisper_model),
):
    if file.content_type not in ("audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp4"):
        raise HTTPException(415, detail="Unsupported file type")

    # Determine the file size. Some UploadFile implementations expose a `size`
    # attribute; otherwise, fall back to measuring the underlying file object.
    size = getattr(file, "size", None)
    if size is None:
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)

    if size > MAX_UPLOAD_SIZE:
        raise HTTPException(413, detail="File too large")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        path = tmp.name

    start = time.time()
    try:
        result = model.transcribe(path)
    except Exception as e:
        log.exception("Whisper failed")
        raise HTTPException(500, detail="Transcription error") from e
    finally:
        os.remove(path)

    return JSONResponse(
        status_code=200,
        content={
            "text": result["text"],
            "duration_ms": int((time.time() - start) * 1000),
        },
    )
