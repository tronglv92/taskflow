"""
TaskFlow Backend Tests
Platform Engineering Bootcamp Reference Application

The first four tests exercise the always-on endpoints with no database and no
environment. The rest use the `client` fixture (see conftest.py), which points
the app at a throwaway SQLite database.
"""

from fastapi.testclient import TestClient

from app.main import app

# Bare client (no fixture) for the DB-free endpoint tests.
plain_client = TestClient(app)


def test_root_endpoint():
    response = plain_client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Welcome to TaskFlow API"
    assert data["version"] == "0.1.0"


def test_health_check():
    response = plain_client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "taskflow-backend"
    assert "timestamp" in data


def test_api_status():
    response = plain_client.get("/api/v1/status")
    assert response.status_code == 200

    data = response.json()
    assert data["api_version"] == "v1"
    assert data["status"] == "operational"
    assert "features" in data
    assert "database" in data


def test_cors_headers():
    # A real CORS preflight: browsers send Origin + Access-Control-Request-Method.
    response = plain_client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


# --------------------------------------------------------------------------- #
# Database-backed tests (use the `client` fixture)
# --------------------------------------------------------------------------- #


def _register_and_login(client, email="alex@example.com", password="password123"):
    reg = client.post("/api/auth/register", json={"email": email, "password": password})
    assert reg.status_code == 201, reg.text
    tok = client.post("/api/auth/token", data={"username": email, "password": password})
    assert tok.status_code == 200, tok.text
    return tok.json()["access_token"]


def test_register_and_login(client):
    token = _register_and_login(client)
    assert token

    # Duplicate registration is rejected.
    dup = client.post(
        "/api/auth/register",
        json={"email": "alex@example.com", "password": "password123"},
    )
    assert dup.status_code == 400


def test_create_and_list_task(client):
    token = _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/tasks/",
        json={"title": "Ship the platform", "priority": "high"},
        headers=headers,
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["title"] == "Ship the platform"
    assert body["is_completed"] is False
    assert body["priority"] == "high"

    listed = client.get("/api/v1/tasks/", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_task_not_found_404(client):
    token = _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/tasks/999999", headers=headers)
    assert response.status_code == 404


def test_tasks_require_authentication(client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 401


def test_task_mutations_invalidate_redis_list_cache(client, monkeypatch):
    """Redis accelerates reads only; writes always invalidate cached lists."""
    from services import redis_cache

    invalidations = []
    monkeypatch.setattr(
        redis_cache, "invalidate_pattern", lambda pattern: invalidations.append(pattern)
    )
    token = _register_and_login(client, email="cache@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post("/api/v1/tasks/", json={"title": "Cache me"}, headers=headers)
    assert created.status_code == 201
    assert invalidations == ["taskflow:tasks:*"]

    updated = client.put(
        f"/api/v1/tasks/{created.json()['id']}",
        json={"is_completed": True},
        headers=headers,
    )
    assert updated.status_code == 200
    assert invalidations == ["taskflow:tasks:*", "taskflow:tasks:*"]
