import subprocess
from pathlib import Path
from typing import *

import librosa

from constants import DURATION_THRESHOLD, TEMP_PATH
from . import generate_random_identifier
from .segments import get_segments, Segment

__all__ = [
    "trim_audio_with_segments", "trim_audio_from_sponsorblock"
]


# Input: [(10, 15)], 20
# Output: [(0, 10), (15, 20)]
def get_true_audio_segments(non_audio_segments: List[Segment], duration: float) -> List[Segment]:
    true_audio_segments = []
    
    # Gets times for previous true audio segments
    for index, segment in enumerate(non_audio_segments):
        is_first = index == 0
        
        start = 0 if is_first else non_audio_segments[index - 1][1]
        end = segment[0]
        true_audio_segments.append((start, end))
    
    # Gets the last audio segment
    last_segment = non_audio_segments[-1]
    start = last_segment[1]
    end = duration
    true_audio_segments.append((start, end))
    
    # Remove non-durational segments
    true_audio_segments = [
        segment
        for segment in true_audio_segments
        if segment[0] != segment[1]
    ]
    
    return true_audio_segments


def get_segments_as_duration(segments: List[Segment]) -> List[Segment]:
    return [
        (segment[0], duration)
        for segment in segments
        if (duration := segment[1] - segment[0]) > DURATION_THRESHOLD
    ]


def prepare_ffmpeg_trim_command(segments: List[Segment], filename: str, video_id: str) -> Tuple[str, List[Path]]:
    # Filenames of true audio segments
    filenames = [
        f"{video_id}_{index}_{start}_{duration}.wav"
        for index, (start, duration) in enumerate(segments)
    ]
    filenames_with_folder = [
        TEMP_PATH / name
        for name in filenames
    ]
    filenames_parts_command = " ".join([
        f"-ss {start} -t {duration} {path.absolute()}"
        for (start, duration), path in zip(segments, filenames_with_folder)
    ])
    command = f"ffmpeg -y -i ./{filename} {filenames_parts_command}"
    
    return command, filenames_with_folder


def prepare_ffmpeg_concatenate_command(files: List[Path], output: Path) -> Tuple[str, Path]:
    # Create list file
    content = "\n".join([
        f"file {file.absolute()}"
        for file in files
    ])
    file = TEMP_PATH / "list_files" / f"{generate_random_identifier()}.txt"
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content)
    
    command = f"ffmpeg -y -f concat -safe 0 -i {file.absolute()} -c copy {output.absolute()}"
    
    return command, file


def trim_audio_with_segments(
        segments: List[Segment],
        audio: Path,
        output: Path,
        video_id: str
) -> None:
    path = str(audio)
    folder = str(output.parent.absolute())
    
    duration = librosa.get_duration(filename=path)
    
    # Get true audio segments
    true_audio_segments = get_true_audio_segments(segments, duration)
    durations = get_segments_as_duration(true_audio_segments)
    
    # Cutout non-audio parts
    trim_command, files = prepare_ffmpeg_trim_command(
        segments=durations,
        video_id=video_id,
        filename=output.name
    )
    subprocess.run(trim_command, shell=True, cwd=folder)
    
    # Concatenate these parts together
    concatenate_command, list_file = prepare_ffmpeg_concatenate_command(
        files=files,
        output=output
    )
    subprocess.run(concatenate_command, shell=True, cwd=folder)
    
    # Clean up
    temp_files = files + [list_file]
    
    for file in temp_files:
        file.unlink(missing_ok=True)


def trim_audio_from_sponsorblock(
        audio: Path,
        output: Path,
        video_id: str
) -> None:
    segments = get_segments(video_id)
    
    if len(segments) > 0:
        trim_audio_with_segments(
            segments=segments,
            audio=audio,
            output=output,
            video_id=video_id
        )
