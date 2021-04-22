# noinspection PyUnresolvedReferences
import import_check

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import config
from routes import router


def get_application() -> FastAPI:
    application = FastAPI(
        debug=config.IS_DEBUG,
        title="YT2Instrumental",
    )
    
    application.include_router(router)
    
    application.mount("/static", StaticFiles(directory="static"), name="static")
    
    return application


app = get_application()

if __name__ == "__main__":
    if config.IS_DEBUG:
        import uvicorn
        
        uvicorn.run(app)
