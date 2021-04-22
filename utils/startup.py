import logging

from constants import OUTPUT_FOLDER

__all__ = [
    "startup_initialize"
]


def startup_initialize() -> None:
    logging.info("Initialization started...")
    
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    
    logging.info("Initialization finished successfully!")
