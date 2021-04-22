from fastapi import APIRouter, Path, Query
from starlette.responses import RedirectResponse

from utils import build_audio_url, is_audio_downloaded
from utils.download import process_audio_download

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
        video_id: str = Path(None, title="ID of the video (what you can see in the url)"),
        quality: int = Query(ge=65, le=320, default=320),
        skip_segments: bool = Query(True),
):
    redirect = RedirectResponse(url=build_audio_url(video_id, skip_segments))
    
    if is_audio_downloaded(video_id, skip_segments):
        return redirect
    
    process_audio_download(
        video_id=video_id,
        quality=quality,
        skip_segments=skip_segments
    )
    
    return redirect
