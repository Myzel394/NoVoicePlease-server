import config
from .folder import build_audio_filename

__all__ = [
    "build_audio_url"
]


def build_audio_url(video_id: str, skip_segments: bool, is_instrumental: bool) -> str:
    return "/" + str(config.OUTPUT_FOLDER / video_id / build_audio_filename(skip_segments, is_instrumental))
