"""Simple tests for main application without Docker dependencies."""

from app.main import app
from fastapi.testclient import TestClient


def test_root_endpoint():
    """Test root endpoint."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to POS API"
    assert data["version"] == "0.1.0"


def test_health_check():
    """Test health check endpoint."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
