from typing import *

from pydantic import BaseModel

__all__ = [
    "ConfigSchema"
]


class ConfigSchema(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "version": "0.1.0",
                "segments_api_url": "https://sponsor.ajay.app/api/skipSegments",
                "segments_categories": [
                    "sponsor",
                    "intro",
                    "outro",
                    "selfpromo",
                    "interaction",
                    "music_offtopic"
                ],
                "default_audio_quality": 320,
                "min_audio_quality": 65,
                "max_audio_quality": 320,
                "default_skip_segments": True
            }
        }
    
    version: str
    segments_api_url: str
    segments_categories: List[str]
    default_audio_quality: int
    min_audio_quality: int
    max_audio_quality: int
    default_skip_segments: bool
