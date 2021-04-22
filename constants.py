import tempfile
from pathlib import Path

__all__ = [
    "BASE_FOLDER", "DURATION_THRESHOLD", "TEMP_PATH"
]

BASE_FOLDER = Path(__file__).parent

DURATION_THRESHOLD = .1
TEMP_PATH = Path(tempfile.gettempdir()) / "yt_to_instrumental"
