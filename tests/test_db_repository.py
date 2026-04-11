"""
Unit tests for ScanRepository database operations.

Uses SQLite in-memory database (:memory:) for fast, isolated testing.
"""

import json
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine

from rankle.db.engine import create_all_tables, get_db_session
from rankle.db.models import Scan, ScanModule, ScanResult, Progress
from rankle.db.repository import ScanRepository


@pytest.fixture
def db_engine():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:")
    create_all_tables(engine)
    return engine


@pytest.fixture
def repository(db_engine):
    """Create repository with test engine."""
    with get_db_session(db_engine) as session:
        yield ScanRepository(session)


class TestScanRepository:
    """Test ScanRepository CRUD operations."""

    @pytest.mark.db
    def test_create_scan(self, db_engine):
        """Test creating a scan record."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            scan = repo.create_scan("example.com", "full")

            assert scan.id is not None
            assert scan.domain == "example.com"
            assert scan.scan_type == "full"
            assert scan.status == "in_progress"

    @pytest.mark.db
    def test_get_scan(self, db_engine):
        """Test retrieving a scan record."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            created_scan = repo.create_scan("example.com", "full")
            scan_id = created_scan.id

        # Retrieve in new session
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            retrieved_scan = repo.get_scan(scan_id)

            assert retrieved_scan is not None
            assert retrieved_scan.domain == "example.com"

    @pytest.mark.db
    def test_save_module_result(self, db_engine):
        """Test saving module results."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            scan = repo.create_scan("example.com", "full")
            scan_id = scan.id

            results = [
                {"type": "A", "value": "192.0.2.1", "severity": "info"},
                {"type": "MX", "value": "mail.example.com", "severity": "info"},
            ]

            repo.save_module_result(scan_id, "dns_resolver", results, status="ok")

        # Verify in new session
        with get_db_session(db_engine) as session:
            from sqlalchemy import select
            scan_results = session.scalars(
                select(ScanResult).where(ScanResult.scan_id == scan_id)
            ).all()

            assert len(scan_results) == 2
            assert scan_results[0].module_name == "dns_resolver"
            assert scan_results[0].severity == "info"

    @pytest.mark.db
    def test_update_progress(self, db_engine):
        """Test updating scan progress."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            scan = repo.create_scan("example.com", "full")
            scan_id = scan.id

            repo.update_progress(
                scan_id,
                current_module="dns_resolver",
                progress_pct=25,
                completed_count=1,
                total_count=4,
            )

        # Verify
        with get_db_session(db_engine) as session:
            from sqlalchemy import select
            progress = session.scalars(
                select(Progress).where(Progress.scan_id == scan_id)
            ).first()

            assert progress is not None
            assert progress.current_module == "dns_resolver"
            assert progress.progress_pct == 25
            assert progress.completed_modules == 1

    @pytest.mark.db
    def test_finalize_scan(self, db_engine):
        """Test finalizing a scan."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            scan = repo.create_scan("example.com", "full")
            scan_id = scan.id

            repo.finalize_scan(scan_id, "completed", duration_ms=1234)

        # Verify
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            scan = repo.get_scan(scan_id)

            assert scan.status == "completed"
            assert scan.duration_ms == 1234

    @pytest.mark.db
    def test_get_scan_history(self, db_engine):
        """Test retrieving scan history for a domain."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)

            # Create multiple scans
            for i in range(3):
                scan = repo.create_scan("example.com", "full")
                repo.finalize_scan(scan.id, "completed", duration_ms=100)

        # Retrieve history
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            history = repo.get_scan_history("example.com", limit=10)

            assert len(history) == 3
            # Most recent first
            assert history[0].scanned_at >= history[1].scanned_at

    @pytest.mark.db
    def test_list_all_scans(self, db_engine):
        """Test listing all scans."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)

            # Create scans for different domains
            for domain in ["example.com", "test.org", "demo.io"]:
                scan = repo.create_scan(domain, "full")
                repo.finalize_scan(scan.id, "completed", duration_ms=100)

        # List all
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            all_scans = repo.list_all_scans(limit=10)

            assert len(all_scans) == 3

    @pytest.mark.db
    def test_cascade_delete_orphans(self, db_engine):
        """Test that deleting scan deletes related records."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            scan = repo.create_scan("example.com", "full")
            scan_id = scan.id

            results = [{"type": "A", "value": "192.0.2.1"}]
            repo.save_module_result(scan_id, "dns_resolver", results)
            repo.update_progress(scan_id, "dns_resolver", 50, 1, 2)

            # Delete scan
            session.delete(scan)
            session.commit()

        # Verify orphans deleted
        with get_db_session(db_engine) as session:
            from sqlalchemy import select, func
            result_count = session.scalars(
                select(func.count(ScanResult.id))
            ).first()
            module_count = session.scalars(
                select(func.count(ScanModule.id))
            ).first()
            progress_count = session.scalars(
                select(func.count(Progress.id))
            ).first()

            assert result_count == 0
            assert module_count == 0
            assert progress_count == 0
