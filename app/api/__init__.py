from fastapi import APIRouter
from app.api.transcription import router as transcription_router
from app.api.health import router as health_router

router = APIRouter()
router.include_router(transcription_router)
router.include_router(health_router)
