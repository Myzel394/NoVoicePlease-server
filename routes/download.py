from enum import Enum

from fastapi import APIRouter, Path, Query

from schemas import VideoDownloadResponse

__all__ = [
    "router"
]

router = APIRouter()

def build_opts(quality: int) -> dict:
    return {
        "format": 'bestaudio/best',
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": str(quality),
        }],
    }


@router.get(
    "/{video_id}",
    response_model=VideoDownloadResponse,
    name="download-audio"
)
async def download_audio(
    video_id: str,
    quality: int = Query(ge=65, le=320, default=320)
):
    youtube_dl_options = build_opts(quality)
    
    print(youtube_dl_options)
