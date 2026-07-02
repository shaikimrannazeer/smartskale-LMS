"""Tests for health check endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["application"] == "SmartSkale LMS"
    assert data["version"] == "1.0.0"
