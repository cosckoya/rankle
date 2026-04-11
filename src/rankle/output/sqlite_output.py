"""
SQLite database output backend - persists scan results to SQLite.

Uses ScanRepository to handle all database operations.
"""

from typing import Any

from sqlalchemy.orm import Session

from rankle.output.base import OutputBackend
from rankle.db.repository import ScanRepository


class SQLiteOutput(OutputBackend):
    """
    Persist scan results to SQLite database.

    Uses ScanRepository for all database operations. Session must be active
    when write() is called.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize SQLite output backend.

        Args:
            session: Active SQLAlchemy Session for database operations.
        """
        self.session = session
        self.repository = ScanRepository(session)

    def write(
        self,
        scan_id: str,
        results: dict[str, Any],
        metadata: dict[str, Any]
    ) -> None:
        """
        Persist scan results to database.

        Creates ScanModule and ScanResult records for each module's output.

        Args:
            scan_id: Scan ID (str, but will be stored as-is).
            results: Results dict with module names as keys.
                     Each value should be a list of result dicts or a single dict.
            metadata: Scan metadata (domain, duration, status, etc).
        """
        # Parse status from metadata
        status = metadata.get("status", "completed")
        duration_ms = metadata.get("duration_ms", 0)
        error_message = metadata.get("error_message")

        # Save each module's results
        for module_name, module_results in results.items():
            if not module_results:
                continue

            # Normalize to list of dicts
            result_list: list[dict[str, Any]] = []
            if isinstance(module_results, dict):
                result_list = [module_results]
            elif isinstance(module_results, list):
                result_list = [r for r in module_results if isinstance(r, dict) or True]
            else:
                # Fallback for non-dict results
                result_list = [{"value": str(module_results), "severity": "info"}]

            # Ensure each result has required fields
            normalized_results: list[dict[str, Any]] = []
            for result in result_list:
                if isinstance(result, dict):
                    # Set defaults for missing fields
                    result.setdefault("type", f"{module_name}_result")
                    result.setdefault("severity", "info")
                    normalized_results.append(result)
                else:
                    # Wrap non-dict results
                    normalized_results.append({
                        "value": str(result),
                        "type": f"{module_name}_result",
                        "severity": "info",
                    })

            # Save to database
            self.repository.save_module_result(
                scan_id=int(scan_id),
                module_name=module_name,
                results=normalized_results,
                status="ok"
            )

        # Finalize scan record
        self.repository.finalize_scan(
            scan_id=int(scan_id),
            status=status,
            duration_ms=duration_ms,
            error_message=error_message
        )

        # Commit session
        self.session.commit()
