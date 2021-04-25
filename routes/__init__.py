from fastapi import APIRouter

from . import audio, config

router = APIRouter()

router.include_router(audio.router, tags=["audio"], prefix="/audio")
router.include_router(config.router, tags=["config"], prefix="/config")
