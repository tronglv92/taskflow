"""
TaskFlow Backend Tests
Platform Engineering Bootcamp Reference Application

Students will learn testing in Week 3 and expand these tests throughout the bootcamp.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


def test_root_endpoint():
    """
    Test the root endpoint returns welcome message

    Week 3: Students learn basic API testing
    """
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to TaskFlow API"
    assert data["version"] == "0.1.0"


def test_health_check():
    """
    Test the health check endpoint

    Week 6: Students learn about health checks for containers and Kubernetes
    """
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "taskflow-backend"
    assert "timestamp" in data


def test_api_status():
    """
    Test the API status endpoint

    Week 3: Students learn about API versioning and status endpoints
    """
    response = client.get("/api/v1/status")
    assert response.status_code == 200

    data = response.json()
    assert data["api_version"] == "v1"
    assert data["status"] == "operational"
    assert "features" in data
    assert "database" in data


def test_cors_headers():
    """
    Test CORS headers are properly configured

    Week 3: Students learn about CORS for frontend-backend communication
    """
    response = client.options("/health")
    assert response.status_code == 200


# Week 4+: Task CRUD tests will be added
# Week 4+: Authentication tests will be added
# Week 5+: User management tests will be added
