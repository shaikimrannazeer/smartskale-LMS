"""Test authentication endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import create_app
from app.models.user import UserRole

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Database session fixture."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Test client fixture."""
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_register_success(self, client: TestClient) -> None:
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "student",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "john@example.com"
        assert data["full_name"] == "John Doe"
        assert data["role"] == "student"

    def test_register_duplicate_email(self, client: TestClient) -> None:
        """Test registration with duplicate email."""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "student",
            },
        )

        # Second registration with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Jane Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "student",
            },
        )
        assert response.status_code == 409
        data = response.json()
        assert data["error_code"] == "CONFLICT"

    def test_register_invalid_password(self, client: TestClient) -> None:
        """Test registration with short password."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "short",
                "role": "student",
            },
        )
        assert response.status_code == 422

    def test_login_success(self, client: TestClient) -> None:
        """Test successful login."""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "student",
            },
        )

        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "john@example.com",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "john@example.com"

    def test_login_invalid_credentials(self, client: TestClient) -> None:
        """Test login with invalid credentials."""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "student",
            },
        )

        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "john@example.com",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401
        data = response.json()
        assert data["error_code"] == "UNAUTHORIZED"

    def test_login_nonexistent_user(self, client: TestClient) -> None:
        """Test login with non-existent email."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 401

    def test_get_current_user_success(self, client: TestClient) -> None:
        """Test getting current user with valid token."""
        # Register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "student",
            },
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "john@example.com",
                "password": "securepassword123",
            },
        )
        access_token = login_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "john@example.com"
        assert data["full_name"] == "John Doe"

    def test_get_current_user_no_token(self, client: TestClient) -> None:
        """Test accessing protected endpoint without token."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403

    def test_refresh_token_success(self, client: TestClient) -> None:
        """Test refreshing access token."""
        # Register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "student",
            },
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "john@example.com",
                "password": "securepassword123",
            },
        )
        refresh_token = login_response.json()["refresh_token"]

        # Refresh token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_logout(self, client: TestClient) -> None:
        """Test logout."""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
