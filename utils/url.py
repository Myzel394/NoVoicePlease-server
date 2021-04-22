__all__ = [
    "build_audio_url"
]

from .folder import build_audio_filename


def build_audio_url(video_id: str, skip_segments: bool, is_instrumental: bool) -> str:
    return f"/static/output/{video_id}/{build_audio_filename(skip_segments, is_instrumental)}"
