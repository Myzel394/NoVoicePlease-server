from youtube_dl import YoutubeDL

import config
import constants
from .audio_trim import trim_audio_from_sponsorblock
from .folder import (
    build_audio_filename, build_audio_output_path, clear_space_if_needed,
)

__all__ = [
    "build_opts", "process_audio_download"
]


def build_opts(video_id: str, filename: str, quality: int) -> dict:
    return {
        "format": 'bestaudio/best',
        "quiet": True,
        "no_warnings": True,
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

    clear_space_if_needed()

    with YoutubeDL(options) as downloader:
        def download():
            downloader.download([video_id])

        for _ in range(constants.DOWNLOAD_RETRY_AMOUNT):
            try:
                download()
            except OSError:
                clear_space_if_needed()


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
