from fastapi import APIRouter
from app.api.transcribe import router as transcribe_router
from app.api.health import router as health_router

router = APIRouter()
router.include_router(transcribe_router)
router.include_router(health_router)
