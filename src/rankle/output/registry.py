"""
Output backend registry - factory for selecting and instantiating backends.

Provides a clean interface for getting the appropriate output backend.
"""

from typing import Any

from rankle.output.base import OutputBackend
from rankle.output.console import ConsoleOutput
from rankle.output.json_output import JSONOutput


class OutputRegistry:
    """
    Factory for instantiating output backends.

    Example:
        >>> backend = OutputRegistry.get_backend("console")
        >>> backend.write("scan_123", results, metadata)
    """

    # Mapping of backend names to their classes
    _backends: dict[str, type[OutputBackend]] = {
        "console": ConsoleOutput,
        "json": JSONOutput,
    }

    @staticmethod
    def get_backend(
        backend_type: str,
        **kwargs: Any
    ) -> OutputBackend:
        """
        Get an instance of the requested backend.

        Args:
            backend_type: Name of the backend ("console", "json", "sqlite").
            **kwargs: Additional arguments passed to backend constructor.

        Returns:
            Instantiated OutputBackend subclass.

        Raises:
            ValueError: If backend_type is not registered.

        Example:
            >>> backend = OutputRegistry.get_backend("json", output_dir="my_reports")
            >>> backend = OutputRegistry.get_backend("console")
        """
        if backend_type == "sqlite":
            # SQLite requires special handling due to session dependency
            from rankle.output.sqlite_output import SQLiteOutput
            if "session" not in kwargs:
                raise ValueError("SQLite backend requires 'session' argument")
            return SQLiteOutput(**kwargs)

        if backend_type not in OutputRegistry._backends:
            raise ValueError(
                f"Unknown backend: {backend_type}. "
                f"Available: {list(OutputRegistry._backends.keys())}"
            )

        backend_class = OutputRegistry._backends[backend_type]
        return backend_class(**kwargs)

    @staticmethod
    def list_backends() -> list[str]:
        """
        List all available backend names.

        Returns:
            List of backend identifiers.
        """
        return list(OutputRegistry._backends.keys()) + ["sqlite"]

    @staticmethod
    def register_backend(name: str, backend_class: type[OutputBackend]) -> None:
        """
        Register a custom backend.

        Allows extending the registry with user-defined backends.

        Args:
            name: Identifier for the backend.
            backend_class: Backend class (must inherit from OutputBackend).

        Raises:
            TypeError: If backend_class doesn't inherit from OutputBackend.

        Example:
            >>> class MyBackend(OutputBackend):
            ...     def write(self, scan_id, results, metadata): pass
            >>> OutputRegistry.register_backend("my_backend", MyBackend)
        """
        try:
            if not issubclass(backend_class, OutputBackend):
                raise TypeError(f"{backend_class} must inherit from OutputBackend")
        except TypeError as e:
            raise TypeError(f"{backend_class} must inherit from OutputBackend") from e
        OutputRegistry._backends[name] = backend_class
