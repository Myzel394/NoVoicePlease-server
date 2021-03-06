import shutil
import subprocess
from pathlib import Path

from spleeter.separator import Separator

import constants
from . import add_metadata_from_youtube
from .folder import build_audio_filename, build_audio_output_path, generate_temp_folder

__all__ = [
    "extract_audio", "process_audio_extraction"
]

DEFAULT_SEPARATOR = Separator(constants.SPLEETER_SEPARATION_METHOD)
INSTRUMENTAL_FILENAME = constants.SPLEETER_TARGETED_FILE


async def extract_audio(
        audio: Path,
        output: Path,
) -> None:
    # Spleeter exports two audio files in a folder. We only need to get the `accompaniment.wav` file.
    
    # Just create a tmp folder where Spleeter can save the audio files and move the instrumental one to the correct
    # place
    folder = generate_temp_folder()
    
    DEFAULT_SEPARATOR.separate_to_file(
        str(audio.absolute()),
        str(folder.absolute())
    )
    
    # Find correct file
    child_directory = next(folder.iterdir())
    file = folder / child_directory / INSTRUMENTAL_FILENAME

    # Convert file
    subprocess.Popen(["ffmpeg", "-y", "-i", file.absolute(), output.absolute()]).wait()
    
    # Clean up
    shutil.rmtree(str(folder))


async def process_audio_extraction(
        video_id: str,
        skip_segments: bool,
) -> None:
    original_filename = build_audio_filename(skip_segments=skip_segments, instrumental=False)
    original_file_path = build_audio_output_path(video_id, filename=original_filename)
    
    instrumental_filename = build_audio_filename(skip_segments=skip_segments, instrumental=True)
    instrumental_file_path = build_audio_output_path(video_id, filename=instrumental_filename)
    
    await extract_audio(
        audio=original_file_path,
        output=instrumental_file_path,
    )

    await add_metadata_from_youtube(
        video_id=video_id,
        path=instrumental_file_path,
    )
