from constants import OUTPUT_FOLDER

__all__ = [
    "build_audio_output_path"
]


def build_audio_output_path(video_id: str) -> str:
    return OUTPUT_FOLDER / video_id / "audio.mp3"
