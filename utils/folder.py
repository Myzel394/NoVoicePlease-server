import random
import shutil
import string
from pathlib import Path
from typing import Set

import config
import constants
from constants import DELETE_AMOUNT_ON_DELETE_FUNCTION_CALL, TEMP_PATH

__all__ = [
    "get_downloaded_video_ids", "is_audio_downloaded", "is_audio_extracted", "build_audio_filename",
    "build_audio_output_path", "generate_random_identifier", "generate_temp_folder", "clear_up_downloads",
    "get_remaining_space", "clear_space_if_needed"
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
    return config.OUTPUT_FOLDER / video_id / filename


def generate_random_identifier() -> str:
    return "".join(random.choices(IDENTIFIER_ALLOWED_CHARACTERS, k=IDENTIFIER_LENGTH))


def generate_temp_folder() -> Path:
    return TEMP_PATH / generate_random_identifier()


def clear_up_downloads() -> None:
    downloaded_ids = get_downloaded_video_ids()
    delete_ids = random.sample(downloaded_ids, min(
        DELETE_AMOUNT_ON_DELETE_FUNCTION_CALL, len(downloaded_ids)))

    for delete_id in delete_ids:
        folder = config.OUTPUT_FOLDER / delete_id
        shutil.rmtree(str(folder))


def get_remaining_space() -> int:
    total, used, free = shutil.disk_usage("/")
    return free


def clear_space_if_needed() -> True:
    """Returns a boolean whether folders were deleted"""
    free_space = get_remaining_space()

    if free_space <= constants.DELETE_WHEN_LESS_AVAILABLE:
        clear_up_downloads()
        return True
    return False


def _does_file_exists(video_id: str, filename: str) -> bool:
    video_ids = get_downloaded_video_ids()

    if video_id not in video_ids:
        # Video not downloaded
        return False

    folder = config.OUTPUT_FOLDER / video_id
    audio_file = folder / filename

    if not audio_file.exists():
        # Folder probably emptied
        return False

    return True


def get_downloaded_video_ids() -> Set[str]:
    config.OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    return {
        folder.name for folder in config.OUTPUT_FOLDER.iterdir() if folder.is_dir()
    }


def is_audio_downloaded(video_id: str, skip_segments: bool) -> bool:
    return _does_file_exists(video_id, build_audio_filename(skip_segments, False))


def is_audio_extracted(video_id: str, skip_segments: bool) -> bool:
    return _does_file_exists(video_id, build_audio_filename(skip_segments, True))
