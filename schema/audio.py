from typing import *

from pydantic import BaseModel

__all__ = [
    "StatusSchema",
    "DownloadedSchema"
]


class StatusSchema(BaseModel):
    normal_full: bool
    normal_skipped_segments: bool
    instrumental_full: bool
    instrumental_skipped_segments: bool


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
