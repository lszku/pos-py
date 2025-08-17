"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_register_user(client: TestClient):
    """Test user registration."""
    user_data = {
        "email": "test_register@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "role": "cashier"
    }

    response = client.post("/auth/register", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["role"] == user_data["role"]
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_user(client: TestClient):
    """Test registering a user with existing email."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "role": "cashier"
    }

    # First registration should succeed
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Second registration should fail
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_user(client: TestClient):
    """Test user login."""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "password": "testpassword123",
        "full_name": "Login User",
        "role": "cashier"
    }

    client.post("/auth/register", json=user_data)

    # Then try to login
    login_data = {
        "username": "login@example.com",
        "password": "testpassword123"
    }

    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
