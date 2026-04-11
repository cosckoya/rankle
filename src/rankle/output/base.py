"""
Abstract base class for output backends.

All output backends inherit from OutputBackend and implement the write() method.
This allows pluggable output strategies: console, JSON file, SQLite DB, etc.
"""

from abc import ABC, abstractmethod
from typing import Any


class OutputBackend(ABC):
    """
    Abstract base class for scan output backends.

    Subclasses must implement write() to handle result persistence in their
    chosen format (console, JSON, database, etc).

    Example:
        >>> class MyBackend(OutputBackend):
        ...     def write(self, scan_id: str, results: dict, metadata: dict) -> None:
        ...         print(f"Scan {scan_id}: {results}")
    """

    @abstractmethod
    def write(
        self,
        scan_id: str,
        results: dict[str, Any],
        metadata: dict[str, Any]
    ) -> None:
        """
        Persist scan results using this backend.

        Args:
            scan_id: Unique identifier for the scan.
            results: Dictionary of module results. Keys are module names,
                     values are the module's output (typically list or dict).
            metadata: Metadata about the scan (domain, scan_type, duration_ms, etc).

        Raises:
            Exception: Backend-specific exceptions if write fails.
        """
        pass

    def __repr__(self) -> str:
        """Return backend class name for debugging."""
        return f"{self.__class__.__name__}()"
