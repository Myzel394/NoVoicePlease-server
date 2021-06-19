from pprint import pprint

from fastapi import HTTPException

import config
from utils import download_video_information

__all__ = [
    "raise_for_length"
]


async def is_video_too_long(video_id: str) -> bool:
    result = await download_video_information(video_id)

    return result["lengthSeconds"] > config.MAX_AUDIO_LENGTH


async def raise_for_length(video_id: str) -> None:
    """Raises a fastapi HTTPException if the given video for `video_id` is too long."""

    if await is_video_too_long(video_id):
        raise HTTPException(
           status_code=400,
           detail=f"Given video is too long. The max length for this server is {config.MAX_AUDIO_LENGTH} seconds."
        )
