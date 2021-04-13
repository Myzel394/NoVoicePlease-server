from datetime import datetime

from pydantic.main import BaseConfig, BaseModel

__all__ = [
    "DefaultModel"
]


def convert_datetime_to_string(dt: datetime) -> str:
    return dt.isoformat()


class DefaultModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            datetime: convert_datetime_to_string
        }
