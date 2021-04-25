import os
from pathlib import Path

from dotenv import load_dotenv

from constants import BASE_FOLDER

load_dotenv()

SETTINGS_SUFFIX = "YT2I"


def value(name: str, default: str) -> str:
    return os.getenv(f"{SETTINGS_SUFFIX}_{name}", default)


# !!!ATTENTION!!!
# THE SERVER ASSUMES THAT ALL SETTINGS ARE CONFIGURED CORRECTLY!
# YOU NEED TO CHECK WHETHER ALL SETTINGS ARE CORRECT YOURSELF! (if you are not a hacker, you will probably do them
# all correct)
# !!!ATTENTION!!!

OUTPUT_FOLDER = Path.cwd().joinpath(value("OUTPUT_FOLDER", "./static/output")).relative_to(BASE_FOLDER)
SEGMENTS_API_URL = value("SEGMENTS_API_URL", "https://sponsor.ajay.app/api/skipSegments")
SEGMENTS_CATEGORIES = value("SEGMENTS_CATEGORIES", "sponsor,intro,outro,selfpromo,interaction,music_offtopic") \
    .split(",")
IS_DEBUG = bool(int(value("DEBUG", "0")))
DEFAULT_AUDIO_QUALITY = int(value("DEFAULT_AUDIO_QUALITY", "320"))
MIN_AUDIO_QUALITY = int(value("MIN_AUDIO_QUALITY", "65"))
MAX_AUDIO_QUALITY = int(value("MAX_AUDIO_QUALITY", "320"))
DEFAULT_SKIP_SEGMENTS = bool(int(value("DEFAULT_SKIP_SEGMENTS", "1")))
