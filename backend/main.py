"""
StyleMI - Fashion Recommendation Engine
Main FastAPI application entry point.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import logging

from config import settings
from database.db import init_db
from api.recommendations import router as rec_router
from api.outfits import router as outfit_router
from api.users import router as user_router
from api.weather import router as weather_router
from api.feedback import router as feedback_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialise resources on startup, clean up on shutdown."""
    logger.info("Starting StyleMI Fashion Recommendation Engine...")
    # Initialise database
    await init_db()
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info("StyleMI started successfully.")
    yield
    logger.info("StyleMI shutting down...")


app = FastAPI(
    title="StyleMI - Fashion Recommendation Engine",
    description="AI-powered outfit recommendations based on occasion, weather, and personal style.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded images
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Register routers
app.include_router(rec_router, prefix="/api/recommend", tags=["Recommendations"])
app.include_router(outfit_router, prefix="/api/outfits", tags=["Outfits"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(weather_router, prefix="/api/weather", tags=["Weather"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"])


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "service": "StyleMI",
        "version": "1.0.0"
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to StyleMI Fashion Recommendation Engine",
        "docs": "/docs",
        "health": "/health"
    }
