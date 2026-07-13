"""
TaskFlow Backend API
Platform Engineering Bootcamp Reference Application

This is the main entry point for the TaskFlow FastAPI backend.
Students will build and expand this application throughout the bootcamp.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Create FastAPI application
app = FastAPI(
    title="TaskFlow API",
    description="Task Management Platform - Platform Engineering Bootcamp Reference Application",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vue.js dev server
        "http://localhost:3000",  # Alternative dev port
        "http://localhost:8080",  # Alternative dev port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - Welcome message

    This endpoint provides basic information about the TaskFlow API.
    Students will expand this throughout the bootcamp.
    """
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

    Students will enhance this in later weeks with database connectivity checks,
    external service health, and more detailed metrics.
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

    Provides detailed information about the API's current state.
    This will be expanded in later weeks to include:
    - Database connection status
    - Cache status
    - External service dependencies
    - Performance metrics
    """
    return {
        "api_version": "v1",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "development",
        "features": {
            "tasks": "pending",  # Week 3+
            "authentication": "pending",  # Week 4+
            "users": "pending",  # Week 4+
        },
        "database": {
            "status": "not_configured",  # Week 4+
            "type": "postgresql"
        }
    }


# Week 3+: Tasks API endpoints will be added here
# Week 4+: Authentication endpoints will be added here
# Week 5+: User management endpoints will be added here
# Week 7+: Advanced features and integrations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
