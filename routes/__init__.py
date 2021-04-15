from fastapi import APIRouter

from . import audio

router = APIRouter()

router.include_router(audio.router, tags=["audio"])
