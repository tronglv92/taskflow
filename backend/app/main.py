"""
TaskFlow Backend API
Platform Engineering Bootcamp Reference Application

Entry point for the TaskFlow FastAPI backend. The app object is served with
``uvicorn app.main:app`` (local/dev) or ``uvicorn main:app`` (container, where
``app/`` is copied to the working directory). The sys.path line below makes the
root-anchored imports (``from routes import ...``) resolve in both layouts.
"""

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from core.config import settings
from database import engine, init_db
from routes import auth, projects, tasks

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Best-effort table creation for local/SQLite runs. Never fatal."""
    try:
        init_db()
    except Exception as exc:  # pragma: no cover - depends on runtime DB
        logger.warning("Skipping table creation (database unavailable): %s", exc)
    yield


# Create FastAPI application
app = FastAPI(
    title="TaskFlow API",
    description="Task Management Platform - Platform Engineering Bootcamp Reference Application",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint - welcome message and basic API information."""
    return {
        "message": "Welcome to TaskFlow API",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "development",
        "bootcamp": "Platform Engineering Bootcamp - TeKanAid Academy"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint

    This endpoint is used by:
    - Docker health checks
    - Kubernetes liveness probes
    - Load balancers
    - Monitoring systems
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "taskflow-backend",
        "version": "0.1.0"
    }


@app.get("/api/v1/status")
async def api_status():
    """
    API status endpoint

    Reports the API's current state, including a best-effort database check.
    The database check is wrapped so this endpoint never returns 500 when the
    database is down.
    """
    database_connected = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        database_connected = True
    except Exception:
        database_connected = False

    return {
        "api_version": "v1",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "features": {
            "tasks": "available",
            "authentication": "available",
            "users": "available",
            "projects": "available",
        },
        "database": {
            "status": "connected" if database_connected else "unavailable",
            "type": "postgresql"
            if settings.database_url.startswith("postgres")
            else "sqlite",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
