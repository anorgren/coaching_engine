import yaml
import os
import sys
import logging.config

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .config import settings
from .router import recommendation_router, behavior_router, timing_router, moderation_router
from .service import ContentDetectionFlaggedError
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# logging config to work with fastapi dev server
CONFIG_PATH = os.getenv("LOG_CFG", "log_conf.yaml")

if Path(CONFIG_PATH).is_file():
    with open(settings.LOG_CFG, "rt") as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
else:
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().warning(
        f"Logging configuration file not found: {CONFIG_PATH}, using basicConfig"
    )

app = FastAPI(
    title="Coaching Engine API",
    description="Prototyped Coaching Engine API",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: replace / strengthen before deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO: move exception handling into separate module and handle at route level
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions globally to avoid leaking impl. details"""
    return JSONResponse(
        content={
            "detail": "Unknown error occurred. Please contact responsible team.",
            "exception": str(exc),  # TODO: remove in prod or simplify + define error schema for all responses
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(ContentDetectionFlaggedError)
async def content_detection_flagged_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.flagged_categories},
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# app.include_router(coach_router.router)
app.include_router(recommendation_router.router)
app.include_router(behavior_router.router)
app.include_router(timing_router.router)
app.include_router(moderation_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
