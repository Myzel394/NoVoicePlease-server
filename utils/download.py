from typing import *

from youtube_dl import YoutubeDL

import config
from constants import OUTPUT_FOLDER
from .audio_trim import trim_audio_from_sponsorblock
from .folder import build_audio_filename, build_audio_output_path

__all__ = [
    "get_downloaded_video_ids", "is_audio_downloaded", "is_audio_extracted", "build_opts", "process_audio_download"
]


def _does_file_exists(video_id: str, filename: str) -> bool:
    video_ids = get_downloaded_video_ids()
    
    if video_id not in video_ids:
        # Video not downloaded
        return False
    
    folder = OUTPUT_FOLDER / video_id
    audio_file = folder / filename
    
    if not audio_file.exists():
        # Folder probably emptied
        return False
    
    return True


def get_downloaded_video_ids() -> Set[str]:
    return {
        folder.name for folder in config.OUTPUT_FOLDER.iterdir() if folder.is_dir()
    }


def is_audio_downloaded(video_id: str, skip_segments: bool) -> bool:
    return _does_file_exists(video_id, build_audio_filename(skip_segments, False))


def is_audio_extracted(video_id: str, skip_segments: bool) -> bool:
    return _does_file_exists(video_id, build_audio_filename(skip_segments, True))


def build_opts(video_id: str, filename: str, quality: int) -> dict:
    return {
        "format": 'bestaudio/best',
        "outtmpl": str(build_audio_output_path(video_id, filename).absolute()),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": str(quality),
        }],
    }


def download_and_extract_video(filename: str, video_id: str, quality: int) -> None:
    options = build_opts(
        video_id=video_id,
        filename=filename,
        quality=quality
    )
    
    with YoutubeDL(options) as downloader:
        downloader.download([video_id])


def process_audio_download(
        video_id: str,
        skip_segments: bool,
        quality: int = config.DEFAULT_AUDIO_QUALITY,
) -> None:
    filename = build_audio_filename(skip_segments, False)
    path = build_audio_output_path(video_id=video_id, filename=filename)
    
    path.parent.mkdir(exist_ok=True, parents=True)
    
    download_and_extract_video(
        filename=filename,
        video_id=video_id,
        quality=quality
    )
    
    if skip_segments:
        trim_audio_from_sponsorblock(
            audio=path,
            output=path,
            video_id=video_id
        )
