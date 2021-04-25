import tempfile
from pathlib import Path

__all__ = [
    "BASE_FOLDER", "DURATION_THRESHOLD", "TEMP_PATH", "VERSION", "SPLEETER_SEPARATION_METHOD", "SPLEETER_TARGETED_FILE"
]

BASE_FOLDER = Path(__file__).parent.absolute()

DURATION_THRESHOLD = .1
TEMP_PATH = Path(tempfile.gettempdir()) / "yt_to_instrumental"
VERSION = "0.1.0"
SPLEETER_SEPARATION_METHOD = "spleeter:2stems"
SPLEETER_TARGETED_FILE = "accompaniment.wav"
