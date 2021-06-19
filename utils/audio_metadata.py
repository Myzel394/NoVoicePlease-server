from datetime import datetime
from pathlib import Path
from typing import *

import music_tag
from youtube_dl import YoutubeDL

from .folder import build_thumbnail_path
from .audio_trim import get_segments

__all__ = [
    "download_video_information",
    "add_metadata",
    "map_youtubedl_result_to_metadata",
    "add_metadata_from_youtube",
    "map_youtubedl_result_to_information"
]


AUDIO_INFORMATION_YDL_OPTIONS = {
    # No console output
    "quiet": True,
    "no_warnings": True,
}


def map_youtubedl_result_to_metadata(result):
    return {
        "album": result.get("album"),
        "artist": result.get("artist", result.get("channel")),
        "composer": result.get("creator"),
        "comment": result.get("description"),
        "genre": result["categories"][0] if result.get("categories") else None,
        "year": result["upload_date"][:4],
        "title": result["title"],
    }


async def map_youtubedl_result_to_information(result, video_id: str):
    non_audio_segments = await get_segments(video_id)

    return {
        "album": result.get("album"),
        "artist": result.get("artist", result.get("channel")),
        "composer": result.get("creator"),

        "title": result["title"],
        "description": result["description"],
        "categories": result["categories"],
        "upload_date": datetime.strptime(result["upload_date"], "%Y%m%d"),
        "view_count": result["view_count"],
        "like_count": result.get("like_count"),
        "dislike_count": result.get("dislike_count"),

        "non_audio_segments": non_audio_segments
    }


async def add_metadata(
        file: Path,
        thumbnail: Optional[Path] = None,

        album: Optional[str] = None,
        artist: Optional[str] = None,
        composer: Optional[str] = None,
        comment: Optional[str] = None,
        genre: Optional[str] = None,
        year: Optional[int] = None,

        title: Optional[str] = None,
):
    music = music_tag.load_file(str(file.absolute()))

    tags = {
        "album": album,
        "title": title,
        "albumartist": artist,
        "composer": composer,
        "comment": comment,
        "genre": genre,
        "year": year,
        "tracktitle": title,
    }

    for name, value in tags.items():
        if value is not None:
            music[name] = value

    if thumbnail:
        with thumbnail.open("rb") as opened_image:
            music["artwork"] = opened_image.read()

    music.save()


async def download_video_information(video_id: str):
    with YoutubeDL(AUDIO_INFORMATION_YDL_OPTIONS) as downloader:
        result = downloader.extract_info(
            video_id,
            download=False,
        )

    return result


async def add_metadata_from_youtube(video_id: str, path: Path) -> None:
    thumbnail = build_thumbnail_path(video_id=video_id)

    video_information = await download_video_information(video_id=video_id)
    metadata = map_youtubedl_result_to_metadata(video_information)
    await add_metadata(
        file=path,
        thumbnail=thumbnail,
        **metadata,
    )
