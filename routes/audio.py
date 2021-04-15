from youtube_dl import YoutubeDL
from fastapi import APIRouter, Query
from starlette.responses import RedirectResponse

from utils import build_audio_url, is_audio_downloaded, build_opts

__all__ = [
    "router"
]


router = APIRouter()


@router.get(
    "/audio/{video_id}",
    name="audio",
    response_description="Redirects to the static url of the audio file.",
    status_code=307,
)
async def download_audio(
    # VALIDATE VIDEO_ID!!!!! (using Depends probably)
    video_id: str,
    quality: int = Query(ge=65, le=320, default=320)
):
    redirect = RedirectResponse(url=build_audio_url(video_id))
    
    if is_audio_downloaded(video_id):
        return redirect
    
    options = build_opts(video_id, quality)
    
    with YoutubeDL(options) as downloader:
        downloader.download([video_id])
    
    return redirect

