import os
from typing import *

from youtube_dl import YoutubeDL

from constants import OUTPUT_FOLDER, AUDIO_FILE_NAME, INSTRUMENTAL_AUDIO_FILE_NAME
from .folder import build_audio_output_path

__all__ = [
    "get_downloaded_video_ids", "is_audio_downloaded", "is_video_extracted", "build_opts"
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
        folder.name for folder in os.scandir(OUTPUT_FOLDER) if folder.is_dir()
    }


def is_audio_downloaded(video_id: str) -> bool:
    return _does_file_exists(video_id, AUDIO_FILE_NAME)


def is_video_extracted(video_id: str) -> bool:
    return _does_file_exists(video_id, INSTRUMENTAL_AUDIO_FILE_NAME)


def build_opts(video_id: str, quality: int) -> dict:
    return {
        "format": 'bestaudio/best',
        "outtmpl": str(build_audio_output_path(video_id)),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": str(quality),
        }],
    }


def download_video(video_id: str, quality: int) -> None:
    options = build_opts(video_id, quality)
    
    with YoutubeDL(options) as downloader:
        downloader.download([video_id])
