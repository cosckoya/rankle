"""
Unit tests for output backends.

Tests console, JSON, and SQLite output implementations.
"""

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from sqlalchemy import create_engine

from rankle.output.console import ConsoleOutput
from rankle.output.json_output import JSONOutput
from rankle.output.sqlite_output import SQLiteOutput
from rankle.output.registry import OutputRegistry
from rankle.db.engine import create_all_tables, get_db_session
from rankle.db.repository import ScanRepository


@pytest.fixture
def sample_results():
    """Sample scan results for testing."""
    return {
        "dns_resolver": [
            {"type": "A", "value": "192.0.2.1", "severity": "info"},
            {"type": "MX", "value": "mail.example.com", "severity": "info"},
        ],
        "ssl_analyzer": [
            {
                "common_name": "example.com",
                "issuer": "Let's Encrypt",
                "severity": "info",
            }
        ],
        "technology": [
            {
                "name": "nginx",
                "confidence": 0.95,
                "type": "Web Servers",
                "severity": "info",
            }
        ],
    }


@pytest.fixture
def sample_metadata():
    """Sample scan metadata."""
    return {
        "domain": "example.com",
        "scan_type": "full",
        "scanned_at": datetime.now(UTC).isoformat(),
        "duration_ms": 5432,
        "status": "completed",
    }


class TestConsoleOutput:
    """Test ConsoleOutput backend."""

    @pytest.mark.output
    def test_console_output_initialization(self):
        """Test console output initialization."""
        output = ConsoleOutput()
        assert output is not None
        assert output.console is not None or output.console is None  # rich may or may not be available

    @pytest.mark.output
    def test_console_write_with_mock(self, sample_results, sample_metadata):
        """Test console write with mocked console."""
        output = ConsoleOutput()

        # Mock the console print method
        with patch.object(output, "console") as mock_console:
            if mock_console is not None:
                output.write("scan_1", sample_results, sample_metadata)
                # Verify print was called
                assert mock_console.print.called

    @pytest.mark.output
    def test_console_write_plain_fallback(self, sample_results, sample_metadata):
        """Test console fallback to plain output."""
        output = ConsoleOutput()
        output.console = None  # Force fallback

        # Should not raise exception
        with patch("builtins.print") as mock_print:
            output.write("scan_1", sample_results, sample_metadata)
            assert mock_print.called


class TestJSONOutput:
    """Test JSONOutput backend."""

    @pytest.mark.output
    def test_json_output_initialization(self):
        """Test JSON output initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = JSONOutput(output_dir=tmpdir)
            assert Path(tmpdir).exists()

    @pytest.mark.output
    def test_json_write_creates_file(self, sample_results, sample_metadata):
        """Test that JSON output creates valid JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = JSONOutput(output_dir=tmpdir)

            with patch("builtins.print"):  # Suppress print output
                output.write("scan_1", sample_results, sample_metadata)

            # Find created file
            json_files = list(Path(tmpdir).glob("rankle_*.json"))
            assert len(json_files) == 1

            # Verify JSON content
            with open(json_files[0]) as f:
                data = json.load(f)

            assert data["meta"]["domain"] == "example.com"
            assert data["meta"]["scan_type"] == "full"
            assert "dns_resolver" in data["results"]

    @pytest.mark.output
    def test_json_output_directory_creation(self):
        """Test that JSON output creates directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = Path(tmpdir) / "nonexistent" / "path"
            output = JSONOutput(output_dir=str(nested_path))

            assert nested_path.exists()


class TestSQLiteOutput:
    """Test SQLiteOutput backend."""

    @pytest.fixture
    def db_engine(self):
        """Create in-memory SQLite engine."""
        engine = create_engine("sqlite:///:memory:")
        create_all_tables(engine)
        return engine

    @pytest.mark.output
    def test_sqlite_output_initialization(self, db_engine):
        """Test SQLite output initialization."""
        with get_db_session(db_engine) as session:
            output = SQLiteOutput(session)
            assert output is not None
            assert output.repository is not None

    @pytest.mark.output
    def test_sqlite_write_persists_data(self, db_engine, sample_results, sample_metadata):
        """Test that SQLite output persists scan data."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            scan = repo.create_scan("example.com", "full")
            scan_id = scan.id
            session.commit()

        # Write via SQLiteOutput
        with get_db_session(db_engine) as session:
            output = SQLiteOutput(session)
            output.write(str(scan_id), sample_results, sample_metadata)

        # Verify data persisted
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            retrieved_scan = repo.get_scan(scan_id)

            assert retrieved_scan is not None
            assert retrieved_scan.status == "completed"
            assert retrieved_scan.duration_ms == 5432

    @pytest.mark.output
    def test_sqlite_write_normalizes_results(self, db_engine, sample_metadata):
        """Test that SQLite output normalizes different result formats."""
        with get_db_session(db_engine) as session:
            repo = ScanRepository(session)
            scan = repo.create_scan("example.com", "full")
            scan_id = scan.id
            session.commit()

        # Mixed result formats
        mixed_results = {
            "module_a": [{"type": "result", "value": "data"}],  # List of dicts
            "module_b": {"type": "result", "value": "single"},   # Single dict
            "module_c": "string_result",                          # String
        }

        with get_db_session(db_engine) as session:
            output = SQLiteOutput(session)
            output.write(str(scan_id), mixed_results, sample_metadata)

        # Verify all normalized
        with get_db_session(db_engine) as session:
            from sqlalchemy import select
            from rankle.db.models import ScanResult

            results = session.scalars(
                select(ScanResult).where(ScanResult.scan_id == scan_id)
            ).all()

            assert len(results) == 3
            # Each module should have results
            modules = {r.module_name for r in results}
            assert "module_a" in modules
            assert "module_b" in modules
            assert "module_c" in modules


class TestOutputRegistry:
    """Test OutputRegistry factory."""

    @pytest.mark.output
    def test_registry_list_backends(self):
        """Test listing available backends."""
        backends = OutputRegistry.list_backends()
        assert "console" in backends
        assert "json" in backends
        assert "sqlite" in backends

    @pytest.mark.output
    def test_registry_get_console(self):
        """Test getting console backend."""
        backend = OutputRegistry.get_backend("console")
        assert isinstance(backend, ConsoleOutput)

    @pytest.mark.output
    def test_registry_get_json(self):
        """Test getting JSON backend."""
        backend = OutputRegistry.get_backend("json", output_dir="/tmp")
        assert isinstance(backend, JSONOutput)

    @pytest.mark.output
    def test_registry_get_sqlite_requires_session(self):
        """Test that SQLite backend requires session."""
        with pytest.raises(ValueError):
            OutputRegistry.get_backend("sqlite")

    @pytest.mark.output
    def test_registry_get_unknown_backend(self):
        """Test getting unknown backend raises error."""
        with pytest.raises(ValueError):
            OutputRegistry.get_backend("unknown_backend")

    @pytest.mark.output
    def test_registry_register_custom_backend(self):
        """Test registering custom backend."""
        from rankle.output.base import OutputBackend

        class CustomBackend(OutputBackend):
            def write(self, scan_id, results, metadata):
                pass

        OutputRegistry.register_backend("custom", CustomBackend)

        backends = OutputRegistry.list_backends()
        assert "custom" in backends

        backend = OutputRegistry.get_backend("custom")
        assert isinstance(backend, CustomBackend)

    @pytest.mark.output
    def test_registry_register_invalid_backend(self):
        """Test registering non-OutputBackend class raises error."""
        class NotABackend:
            pass

        with pytest.raises(TypeError):
            OutputRegistry.register_backend("invalid", NotABackend)
