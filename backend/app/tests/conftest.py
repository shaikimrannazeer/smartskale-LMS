"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import create_app

# Use in-memory SQLite database for tests
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

Base.metadata.create_all(bind=engine)


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
