from pathlib import Path

__all__ = [
    "BASE_FOLDER", "STATIC_FOLDER", "OUTPUT_FOLDER", "AUDIO_FILE_NAME", "INSTRUMENTAL_AUDIO_FILE_NAME"
]

BASE_FOLDER = Path(__file__).parent
STATIC_FOLDER = BASE_FOLDER / "static"
OUTPUT_FOLDER = STATIC_FOLDER / "output"

AUDIO_FILE_NAME = "audio.mp3"
INSTRUMENTAL_AUDIO_FILE_NAME = "instrumental.mp3"
