from fastapi import APIRouter

from . import download

router = APIRouter()

router.include_router(download.router, tags=["download_video"], prefix="/download-video")
