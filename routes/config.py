from fastapi import APIRouter

from config import (
    DEFAULT_AUDIO_QUALITY, DEFAULT_SKIP_SEGMENTS, MAX_AUDIO_QUALITY, MIN_AUDIO_QUALITY, SEGMENTS_API_URL,
    SEGMENTS_CATEGORIES,
)
from constants import VERSION
from schema import ConfigSchema

__all__ = [
    "router"
]

router = APIRouter()


@router.get(
    "/server",
    response_model=ConfigSchema
)
async def config():
    return {
        "version": VERSION,
        "segments_api_url": SEGMENTS_API_URL,
        "segments_categories": SEGMENTS_CATEGORIES,
        "default_audio_quality": DEFAULT_AUDIO_QUALITY,
        "min_audio_quality": MIN_AUDIO_QUALITY,
        "max_audio_quality": MAX_AUDIO_QUALITY,
        "default_skip_segments": DEFAULT_SKIP_SEGMENTS
    }
