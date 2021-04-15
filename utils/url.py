__all__ = [
    "build_audio_url"
]


def build_audio_url(video_id: str) -> str:
    return f"/static/output/{video_id}/audio.mp3"
