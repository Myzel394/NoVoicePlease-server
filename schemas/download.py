from models import DefaultModel

__all__ = [
    "VideoDownloadResponse"
]


class VideoDownloadResponse(DefaultModel):
    file_url: str
    size: int
