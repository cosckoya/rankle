"""
Database engine factory and session management for Rankle.

Provides:
- Engine creation with sensible defaults
- Session factory and context manager
- Table creation on first run
"""

import contextlib
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from rankle.db.models import Base


def get_engine(db_path: str = "rankle.db") -> Engine:
    """
    Create and return a SQLAlchemy engine.

    Args:
        db_path: Path to SQLite database file. Defaults to "rankle.db" in current directory.

    Returns:
        Configured SQLAlchemy Engine with SQLite backend, connection pooling, and pre-ping enabled.

    Example:
        >>> engine = get_engine("rankle.db")
        >>> create_all_tables(engine)
    """
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(
        db_url,
        echo=False,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
    return engine


def get_session_factory(engine: Engine) -> sessionmaker[Session]:
    """
    Create a session factory bound to the given engine.

    Args:
        engine: SQLAlchemy Engine instance.

    Returns:
        Configured sessionmaker that can be called to create new sessions.

    Example:
        >>> engine = get_engine()
        >>> SessionLocal = get_session_factory(engine)
        >>> session = SessionLocal()
    """
    return sessionmaker(bind=engine, expire_on_commit=False)


@contextlib.contextmanager
def get_db_session(engine: Engine) -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Automatically handles session creation, commit, and cleanup.

    Args:
        engine: SQLAlchemy Engine instance.

    Yields:
        SQLAlchemy Session instance.

    Example:
        >>> engine = get_engine()
        >>> with get_db_session(engine) as session:
        ...     user = session.query(Scan).first()
    """
    SessionLocal = get_session_factory(engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_all_tables(engine: Engine) -> None:
    """
    Create all tables if they don't already exist.

    Uses SQLAlchemy's `create_all()` which is idempotent.

    Args:
        engine: SQLAlchemy Engine instance.

    Example:
        >>> engine = get_engine()
        >>> create_all_tables(engine)
    """
    Base.metadata.create_all(engine)
