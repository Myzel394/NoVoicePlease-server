import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SETTINGS_SUFFIX = "YT2I"


def value(name: str, default: str) -> str:
    return os.getenv(f"{SETTINGS_SUFFIX}_{name}", default)


# !!!ATTENTION!!!
# THE SERVER ASSUMES THAT ALL SETTINGS ARE CONFIGURED CORRECTLY!
# YOU NEED TO CHECK WHETHER ALL SETTINGS ARE CORRECT YOURSELF! (if you are not a hacker, you will probably do them
# all correct)
# !!!ATTENTION!!!

OUTPUT_FOLDER = Path(value("OUTPUT_FOLDER", "./static/output"))
SPLEETER_SEPARATION_METHOD = value("SPLEETER_SEPARATION_METHOD", "spleeter:2stems")
SPLEETER_TARGETED_FILE = value("SPLEETER_TARGETED_FILE", "accompaniment.wav")
SEGMENTS_API_URL = value("SEGMENTS_API_URL", "https://sponsor.ajay.app/api/skipSegments")
SEGMENTS_CATEGORIES = values("SEGMENTS_CATEGORIES", "sponsor,intro,outro,selfpromo,interaction,music_offtopic") \
    .split(",")
IS_DEBUG = bool(values("DEBUG", "1"))
DEFAULT_AUDIO_QUALITY = int(values("DEFAULT_AUDIO_QUALITY", "320"))
MIN_AUDIO_QUALITY = int(values("MIN_AUDIO_QUALITY", "65"))
MAX_AUDIO_QUALITY = int(values("MAX_AUDIO_QUALITY", "320"))
DEFAULT_SKIP_SEGMENTS = bool(values("DEFAULT_SKIP_SEGMENTS", "1"))