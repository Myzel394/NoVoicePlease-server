from pydantic import BaseModel

__all__ = [
    "StatusSchema"
]


class StatusSchema(BaseModel):
    normal_full: bool
    normal_skipped_segments: bool
    instrumental_full: bool
    instrumental_skipped_segments: bool
