from fastapi import FastAPI # Removed Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from backend.src.core.config import get_settings
from backend.src.api import api_router
import logging

# Basic logging configuration for console output
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

settings = get_settings()

logger.info("Starting FastAPI application...")
logger.info(f"Loaded settings: APP_NAME='{settings.APP_NAME}', APP_VERSION='{settings.APP_VERSION}', DEBUG={settings.DEBUG}")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None
)

logger.info("Adding CORS Middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS Middleware added successfully.")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Test endpoint to check if the API is working.
    """
    logger.info("GET / request received at root route.")
    return {"message": "Welcome to VisualTagger API!"}

if settings.DEBUG:
    @app.get("/docs", include_in_schema=False)
    async def get_main_docs():
        logger.info("GET /docs request received. Redirecting to /api/docs.")
        return RedirectResponse(url="/api/docs")

    @app.get("/redoc", include_in_schema=False)
    async def get_main_redoc():
        logger.info("GET /redoc request received. Redirecting to /api/redoc.")
        return RedirectResponse(url="/api/redoc")

logger.info("Including main API router...")
app.include_router(api_router)
logger.info("Main API router included successfully.")
logger.info("FastAPI application configuration complete.")
