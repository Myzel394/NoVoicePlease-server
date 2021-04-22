from pathlib import Path

__all__ = [
    "BASE_FOLDER", "STATIC_FOLDER", "OUTPUT_FOLDER"
]

BASE_FOLDER = Path(__file__).parent
STATIC_FOLDER = BASE_FOLDER / "static"
OUTPUT_FOLDER = STATIC_FOLDER / "output"

DURATION_THRESHOLD = .1
