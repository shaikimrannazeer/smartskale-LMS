"""Database connection and session configuration."""

from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create base class for models
Base = declarative_base()


@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Enable foreign key support for SQLite."""
    pass


def get_db() -> Generator[Session, None, None]:
    """Get database session for dependency injection.

    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
