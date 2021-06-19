import asyncio
import shutil
import subprocess
from pathlib import Path

from PIL import Image
from youtube_dl import DownloadError, YoutubeDL

import config
import constants
from .audio_metadata import add_metadata_from_youtube
from .audio_trim import trim_audio_from_sponsorblock
from .folder import (
    _build_temp_thumbnail_path, build_audio_filename, build_audio_output_path, clear_disk_space,
)

__all__ = [
    "build_opts", "process_audio_download"
]


def build_opts(
        video_id: str,
        filename: str,
        quality: int
) -> dict:
    return {
        # No console output
        "quiet": True,
        "no_warnings": True,

        "writethumbnail": True,
        "format": "bestaudio/best",
        "outtmpl": str(build_audio_output_path(video_id, filename).absolute()),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": str(quality),
        }],
    }


async def convert_audio(file: Path) -> None:
    extension = file.suffix
    temp_file = file.parent / ("output" + extension)

    subprocess.Popen(["ffmpeg", "-y", "-i", file.absolute(), temp_file.absolute()]).wait()

    # Replace new file
    file.unlink()
    shutil.move(temp_file, file)


async def convert_thumbnail(file: Path) -> None:
    new_file = file.parent / "thumbnail.jpg"

    with Image.open(str(file.absolute())) as image:
        image.convert("RGB").save(new_file, quality=config.THUMBNAIL_JPEG_QUALITY)

    file.unlink()


async def download_audio(
        filename: str,
        video_id: str,
        quality: int
) -> bool:
    options = build_opts(
        video_id=video_id,
        filename=filename,
        quality=quality
    )

    clear_disk_space()

    with YoutubeDL(options) as downloader:
        for _ in range(constants.DOWNLOAD_RETRY_AMOUNT):
            try:
                downloader.download([video_id])
                return True
            except OSError:
                clear_disk_space()
            except DownloadError:
                # Let's try that again
                pass

    return False


async def download_and_extract_video(
        filename: str,
        video_id: str,
        quality: int
) -> None:
    succeeded = await download_audio(
        filename=filename,
        quality=quality,
        video_id=video_id
    )

    # Audio couldn't be downloaded
    if not succeeded:
        return

    file = build_audio_output_path(video_id=video_id, filename=filename)
    thumbnail = _build_temp_thumbnail_path(video_id=video_id, filename=filename)
    # Encode audio, otherwise it won't work with music_tag
    await asyncio.wait([
        convert_audio(file),
        convert_thumbnail(thumbnail)
    ])


async def process_audio_download(
        video_id: str,
        skip_segments: bool,
        quality: int = config.DEFAULT_AUDIO_QUALITY,
) -> None:
    filename = build_audio_filename(skip_segments, False)
    path = build_audio_output_path(video_id=video_id, filename=filename)
    
    path.parent.mkdir(exist_ok=True, parents=True)
    
    await download_and_extract_video(
        filename=filename,
        video_id=video_id,
        quality=quality
    )
    
    if skip_segments:
        await trim_audio_from_sponsorblock(
            audio=path,
            output=path,
            video_id=video_id
        )

    await add_metadata_from_youtube(
        video_id=video_id,
        path=path,
    )
