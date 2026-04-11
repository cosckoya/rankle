"""
Repository pattern for Scan-related database operations.

Provides high-level CRUD methods for Scan, ScanModule, ScanResult, and Progress records.
All operations are transactional and use context managers internally.
"""

import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, desc, and_
from sqlalchemy.orm import Session

from rankle.db.models import Scan, ScanModule, ScanResult, Progress


class ScanRepository:
    """
    Data access layer for scan-related operations.

    All methods handle session management internally. Use with engine:

    Example:
        >>> from rankle.db.engine import get_engine
        >>> engine = get_engine()
        >>> repo = ScanRepository(engine)
        >>> scan = repo.create_scan("example.com", "full")
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize repository with a session.

        Args:
            session: Active SQLAlchemy Session instance.
        """
        self.session = session

    def create_scan(self, domain: str, scan_type: str) -> Scan:
        """
        Create a new Scan record and commit.

        Args:
            domain: Target domain being scanned.
            scan_type: Type of scan (e.g., "full", "dns", "ssl").

        Returns:
            Created Scan instance with id populated.
        """
        scan = Scan(
            domain=domain,
            scan_type=scan_type,
            scanned_at=datetime.now(UTC),
            status="in_progress"
        )
        self.session.add(scan)
        self.session.flush()  # Flush to get the id
        return scan

    def get_scan(self, scan_id: int) -> Scan | None:
        """
        Retrieve a Scan record by id.

        Args:
            scan_id: Primary key of the Scan.

        Returns:
            Scan instance or None if not found.
        """
        stmt = select(Scan).where(Scan.id == scan_id)
        return self.session.scalars(stmt).first()

    def save_module_result(
        self,
        scan_id: int,
        module_name: str,
        results: list[dict[str, Any]],
        status: str = "ok"
    ) -> None:
        """
        Save results from a single module execution.

        Creates ScanModule record and individual ScanResult records.

        Args:
            scan_id: FK to parent Scan.
            module_name: Name of the module (e.g., "dns_resolver", "ssl_analyzer").
            results: List of result dicts. Each must have 'type' and 'severity' keys.
            status: Module execution status ("ok", "partial", "error").
        """
        # Create ScanModule record
        module_record = ScanModule(
            scan_id=scan_id,
            module_name=module_name,
            status=status,
            result_count=len(results)
        )
        self.session.add(module_record)
        self.session.flush()

        # Create ScanResult records
        for result_dict in results:
            result_type = result_dict.get("type", "unknown")
            severity = result_dict.get("severity", "info")

            result = ScanResult(
                scan_id=scan_id,
                module_name=module_name,
                result_type=result_type,
                data_json=json.dumps(result_dict, default=str),
                severity=severity
            )
            self.session.add(result)

        self.session.flush()

    def update_progress(
        self,
        scan_id: int,
        current_module: str,
        progress_pct: int,
        completed_count: int,
        total_count: int
    ) -> None:
        """
        Update progress for an active scan.

        Creates Progress record if it doesn't exist, otherwise updates it.

        Args:
            scan_id: FK to parent Scan.
            current_module: Name of module currently running.
            progress_pct: Progress percentage (0-100).
            completed_count: Number of completed modules.
            total_count: Total number of modules to run.
        """
        stmt = select(Progress).where(Progress.scan_id == scan_id)
        progress = self.session.scalars(stmt).first()

        if progress is None:
            progress = Progress(
                scan_id=scan_id,
                current_module=current_module,
                progress_pct=progress_pct,
                total_modules=total_count,
                completed_modules=completed_count,
                last_update=datetime.now(UTC)
            )
            self.session.add(progress)
        else:
            progress.current_module = current_module
            progress.progress_pct = progress_pct
            progress.completed_modules = completed_count
            progress.last_update = datetime.now(UTC)

        self.session.flush()

    def finalize_scan(
        self,
        scan_id: int,
        status: str,
        duration_ms: int,
        error_message: str | None = None
    ) -> None:
        """
        Mark a scan as complete and store final metadata.

        Args:
            scan_id: Primary key of the Scan to finalize.
            status: Final status ("completed", "partial", "error").
            duration_ms: Total scan duration in milliseconds.
            error_message: Optional error message if status is "error".
        """
        scan = self.get_scan(scan_id)
        if scan:
            scan.status = status
            scan.duration_ms = duration_ms
            scan.error_message = error_message
            self.session.flush()

    def get_scan_history(self, domain: str, limit: int = 10) -> list[Scan]:
        """
        Retrieve scan history for a domain (most recent first).

        Args:
            domain: Target domain to retrieve scans for.
            limit: Maximum number of scans to return.

        Returns:
            List of Scan instances ordered by scanned_at DESC.
        """
        stmt = (
            select(Scan)
            .where(Scan.domain == domain)
            .order_by(desc(Scan.scanned_at))
            .limit(limit)
        )
        return self.session.scalars(stmt).all()

    def list_all_scans(self, limit: int = 100) -> list[Scan]:
        """
        Retrieve all scans (most recent first).

        Args:
            limit: Maximum number of scans to return.

        Returns:
            List of Scan instances ordered by scanned_at DESC.
        """
        stmt = select(Scan).order_by(desc(Scan.scanned_at)).limit(limit)
        return self.session.scalars(stmt).all()

    def get_dns_changes(self, domain: str) -> list[dict[str, Any]]:
        """
        Compare last two scans for a domain and return changes.

        Args:
            domain: Target domain to analyze.

        Returns:
            List of change dicts with keys: "added", "removed", "changed".
        """
        scans = self.get_scan_history(domain, limit=2)
        if len(scans) < 2:
            return []

        latest_scan = scans[0]
        previous_scan = scans[1]

        # Get DNS results from latest scan
        latest_dns = self.session.scalars(
            select(ScanResult).where(
                and_(
                    ScanResult.scan_id == latest_scan.id,
                    ScanResult.module_name == "dns_resolver"
                )
            )
        ).all()

        # Get DNS results from previous scan
        previous_dns = self.session.scalars(
            select(ScanResult).where(
                and_(
                    ScanResult.scan_id == previous_scan.id,
                    ScanResult.module_name == "dns_resolver"
                )
            )
        ).all()

        latest_set = {r.data_json for r in latest_dns}
        previous_set = {r.data_json for r in previous_dns}

        changes = {
            "added": [json.loads(r) for r in (latest_set - previous_set)],
            "removed": [json.loads(r) for r in (previous_set - latest_set)],
        }

        return [changes] if changes["added"] or changes["removed"] else []
