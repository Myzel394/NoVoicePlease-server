from fastapi import APIRouter, Path, Query
from starlette.responses import RedirectResponse

import config
from schema import DownloadedSchema, InformationSchema, StatusSchema, TooLongSchema
from utils import (
    build_audio_url, download_video_information, get_downloaded_video_ids, is_audio_downloaded, is_audio_extracted,
    map_youtubedl_result_to_information, process_audio_download, process_audio_extraction, raise_for_length,
)

__all__ = [
    "router"
]

TOO_LONG_RESPONSE = {
    400: {
        "model": TooLongSchema,
        "description": "Video is too long."
    }
}

router = APIRouter()


@router.get(
    "/download/{video_id}",
    name="Audio download",
    response_description="Downloads the audio of the video and redirects to the static url of the downloaded audio "
                         "file.",
    status_code=307,
    responses=TOO_LONG_RESPONSE
)
async def download_audio(
        video_id: str = Path(
            None,
            title="ID of the video (what you can see in the url)",
            # TODO: Check if id is given using api
            regex=r"^[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]$"
        ),
        quality: int = Query(ge=config.MIN_AUDIO_QUALITY, le=config.MAX_AUDIO_QUALITY,
                             default=config.DEFAULT_AUDIO_QUALITY),
        skip_segments: bool = config.DEFAULT_SKIP_SEGMENTS,
):
    redirect = RedirectResponse(url=build_audio_url(video_id, skip_segments, False))

    if is_audio_downloaded(video_id, skip_segments):
        return redirect

    await raise_for_length(video_id)

    await process_audio_download(
        video_id=video_id,
        skip_segments=skip_segments,
        quality=quality,
    )
    
    return redirect


@router.get(
    "/extract/instrumental/{video_id}",
    name="Instrumental extraction",
    response_description="Extracts the instrumental part of the audio of the video. The audio will automatically be "
                         "downloaded with default settings if hasn't been downloaded before.",
    status_code=307,
    responses=TOO_LONG_RESPONSE
)
async def extract_instrumental(
        video_id: str = Path(
            None,
            title="ID of the video (what you can see in the url)",
            # TODO: Check if id is given using api
            regex=r"^[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]$"
        ),
        skip_segments: bool = config.DEFAULT_SKIP_SEGMENTS,
):
    redirect = RedirectResponse(url=build_audio_url(video_id, skip_segments, True))
    
    if is_audio_extracted(video_id, skip_segments):
        return redirect

    await raise_for_length(video_id)

    if not is_audio_downloaded(video_id, skip_segments):
        await process_audio_download(
            video_id=video_id,
            skip_segments=skip_segments,
        )
    
    await process_audio_extraction(
        video_id=video_id,
        skip_segments=skip_segments
    )
    
    return redirect


@router.get(
    "/status/{video_id}",
    name="Returns what files are available for that video",
    status_code=200,
    response_model=StatusSchema,
)
async def status(
        video_id: str = Path(
            None,
            title="ID of the video (what you can see in the url)",
            # TODO: Check if id is given using api
            regex=r"^[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]$"
        ),
):
    return {
        "normal_full": is_audio_downloaded(video_id, skip_segments=False),
        "normal_skipped_segments": is_audio_downloaded(video_id, skip_segments=True),
        "instrumental_full": is_audio_extracted(video_id, skip_segments=False),
        "instrumental_skipped_segments": is_audio_extracted(video_id, skip_segments=True)
    }


@router.get(
    "/information/{video_id}",
    name="Returns information about a given video",
    status_code=200,
    response_model=InformationSchema,
    responses=TOO_LONG_RESPONSE
)
async def status(
        video_id: str = Path(
            None,
            title="ID of the video (what you can see in the url)",
            # TODO: Check if id is given using api
            regex=r"^[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]$"
        ),
):
    await raise_for_length(video_id)

    video_info_result = await download_video_information(video_id)
    video_information = await map_youtubedl_result_to_information(result=video_info_result, video_id=video_id)

    return video_information


@router.get(
    "/downloaded",
    response_model=DownloadedSchema,
)
async def config():
    return {
        "stored_ids": get_downloaded_video_ids()
    }
