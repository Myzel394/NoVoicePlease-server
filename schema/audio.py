from datetime import datetime
from typing import *

from pydantic import BaseModel

__all__ = [
    "StatusSchema", "InformationSchema", "DownloadedSchema", "TooLongSchema"
]


class StatusSchema(BaseModel):
    normal_full: bool
    normal_skipped_segments: bool
    instrumental_full: bool
    instrumental_skipped_segments: bool


class InformationSchema(BaseModel):
    non_audio_segments: List[
        Tuple[float, float]
    ]
    channel: str

    title: str
    description: str
    upload_date: datetime
    view_count: int
    like_count: Optional[int]
    dislike_count: Optional[int]
    tags: List[str]


class DownloadedSchema(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "stored_ids": [
                    "kJQP7kiw5Fk",
                    "dQw4w9WgXcQ"
                ]
            }
        }
    
    stored_ids: List[str]


class TooLongSchema(BaseModel):
    detail: str
