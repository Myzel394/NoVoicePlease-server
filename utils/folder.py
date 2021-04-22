import random
import string
from pathlib import Path

from constants import OUTPUT_FOLDER, TEMP_PATH

__all__ = [
    "build_audio_filename", "build_audio_output_path", "generate_random_identifier", "generate_temp_folder"
]

# Allowed characters for folders and file names
IDENTIFIER_ALLOWED_CHARACTERS = string.ascii_letters + string.digits
IDENTIFIER_LENGTH = 63

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


def generate_random_identifier() -> str:
    return "".join(random.choices(IDENTIFIER_ALLOWED_CHARACTERS, k=IDENTIFIER_LENGTH))


def generate_temp_folder() -> Path:
    return TEMP_PATH / generate_random_identifier()
