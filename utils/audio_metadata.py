from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import *

import music_tag
from async_lru import alru_cache

from .invidious import instance
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
        "artist": result.get("author"),

        "comment": result.get("description"),
        "genre": result.get("genre", result.get("categories")),
        "year": datetime.utcfromtimestamp(result["published"]).year,
        "title": result["title"],
    }


async def map_youtubedl_result_to_information(result, video_id: str):
    non_audio_segments = await get_segments(video_id)

    return {
        "channel": result.get("author"),

        "title": result["title"],
        "description": result["descriptionHtml"],
        "upload_date": datetime.utcfromtimestamp(result["published"]),
        "view_count": result["viewCount"],
        "like_count": result.get("likeCount"),
        "dislike_count": result.get("dislikeCount"),
        "tags": result.get("keywords", []),

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


@alru_cache()
async def download_video_information(video_id: str):
    endpoint = f"/api/v1/videos/{video_id}"

    result = instance.get(endpoint)

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
