import os

from dotenv import load_dotenv
from fastapi import FastAPI

from routes import router

load_dotenv()


def get_application() -> FastAPI:
    debug = bool(os.getenv("DEBUG", 1))
    
    application = FastAPI(
        debug=debug,
        title="YT2Instrumental",
    )
    
    application.include_router(router)

    return application


app = get_application()
