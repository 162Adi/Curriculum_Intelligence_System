"""
Database session management for Curriculum Intelligence System (CIS).
Provides robust SQLAlchemy Session factory for development (SQLite WAL mode) and production (PostgreSQL).
"""

import logging
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
import app.core.cython_compat  # noqa: F401
from app.core.config import settings
from app.models.base import Base

logger = logging.getLogger("cis.database")

# Always resolve database file to canonical project root: D:\OG_Agentic\cis_local.db
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CANONICAL_DB_FILE = (PROJECT_ROOT / "cis_local.db").resolve()
CANONICAL_SQLITE_URL = f"sqlite:///{CANONICAL_DB_FILE.as_posix()}"

# Resolve DB URL
target_url = settings.DATABASE_URL
if "sqlite" in target_url:
    effective_url = CANONICAL_SQLITE_URL
elif "postgresql+asyncpg" in target_url:
    effective_url = CANONICAL_SQLITE_URL
else:
    effective_url = target_url

engine = create_engine(
    effective_url,
    echo=False,
    connect_args={"check_same_thread": False, "timeout": 15.0} if "sqlite" in effective_url else {}
)

# Enable SQLite WAL (Write-Ahead Logging) for non-blocking concurrent reads and writes
if "sqlite" in effective_url:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.close()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for yielding database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables and initialize database schemas."""
    import app.models.users  # noqa: F401
    import app.models.curriculum  # noqa: F401
    import app.models.intelligence  # noqa: F401
    import app.models.approvals  # noqa: F401
    import app.models.agent_history  # noqa: F401

    Base.metadata.create_all(bind=engine)
    logger.info(f"Database schemas successfully initialized on {effective_url}.")
