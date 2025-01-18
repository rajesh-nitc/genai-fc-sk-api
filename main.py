import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from routers import health, prompt
from utils.http import http_client_lifespan

logger = logging.getLogger(__name__)

# Initialize the app
app = FastAPI(
    title=settings.APP_NAME,
    description=f"{settings.APP_NAME} with {settings.LLM_MODEL}",
    version="1.0.0",
    lifespan=http_client_lifespan,
)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log startup configuration
logger.info("FastAPI app starting...")
logger.info(f"Running in {settings.ENV.capitalize()} mode.")
logger.info("App is bound to host: 0.0.0.0, port: 8000")

# Include Routers
app.include_router(prompt.router, prefix="/api", tags=["Prompt"])
app.include_router(health.router, prefix="/api", tags=["Health"])
