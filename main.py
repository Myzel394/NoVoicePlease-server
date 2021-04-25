from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import config
from routes import router


def get_application() -> FastAPI:
    application = FastAPI(
        debug=config.IS_DEBUG,
        title="YT2Instrumental",
    )
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=[],
    )
    
    application.include_router(router)
    
    application.mount("/static", StaticFiles(directory="static"), name="static")
    application.mount("/", StaticFiles(directory="static"), name="static-direct")
    
    return application


app = get_application()

if __name__ == "__main__":
    if config.IS_DEBUG:
        import uvicorn
        
        uvicorn.run(app, port=5612)
