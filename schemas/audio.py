from models import DefaultModel

__all__ = [
    "AudioDownloadResponse"
]


class AudioDownloadResponse(DefaultModel):
    file_url: str
    size: int
