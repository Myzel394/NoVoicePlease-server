import tempfile
from pathlib import Path

__all__ = [
    "BASE_FOLDER", "STATIC_FOLDER", "OUTPUT_FOLDER", "DURATION_THRESHOLD", "TEMP_PATH"
]

BASE_FOLDER = Path(__file__).parent
STATIC_FOLDER = BASE_FOLDER / "static"
# TODO: Automatically create using parents=True
OUTPUT_FOLDER = STATIC_FOLDER / "output"

DURATION_THRESHOLD = .1
TEMP_PATH = Path(tempfile.gettempdir()) / "yt_to_instrumental"
