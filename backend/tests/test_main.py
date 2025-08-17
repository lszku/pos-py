"""Tests for main application."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to POS API"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
