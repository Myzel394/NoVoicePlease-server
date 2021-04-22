from pathlib import Path
from constants import OUTPUT_FOLDER

__all__ = [
    "build_audio_filename", "build_audio_output_path"
]

SKIP_SEGMENTS_MAP = {
    True: "skipped",
    False: "full",
}

INSTRUMENTAL_MAP = {
    True: "instrumental",
    False: "normal"
}


def build_audio_filename(skip_segments: bool, instrumental: bool) -> str:
    return f"audio_{SKIP_SEGMENTS_MAP[skip_segments]}_{INSTRUMENTAL_MAP[instrumental]}.wav"


def build_audio_output_path(video_id: str, filename: str) -> Path:
    return OUTPUT_FOLDER / video_id / filename
