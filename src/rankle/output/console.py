"""
Console output backend - pretty-prints results to stdout using rich.

Organizes output by module type with color-coded severity levels.
"""

import json
from typing import Any

from rankle.output.base import OutputBackend

try:
    from rich.console import Console
    from rich.table import Table

    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    Console = None  # type: ignore[misc, assignment]
    Table = None  # type: ignore[misc, assignment]


class ConsoleOutput(OutputBackend):
    """
    Pretty-print scan results to console with tables and colors.

    Severity colors:
    - critical: red
    - high: orange/yellow
    - medium: yellow
    - low: cyan
    - info: green
    """

    def __init__(self) -> None:
        """Initialize console with rich if available, fallback to print()."""
        if HAS_RICH and Console is not None:
            self.console: Any = Console()
        else:
            self.console = None

    def write(
        self,
        scan_id: str,
        results: dict[str, Any],
        metadata: dict[str, Any],
    ) -> None:
        """
        Print scan results to console.

        Args:
            scan_id: Scan identifier.
            results: Results dict with module names as keys.
            metadata: Scan metadata (domain, duration, etc).
        """
        if self.console is not None and HAS_RICH:
            self._print_rich(scan_id, results, metadata)
        else:
            self._print_plain(scan_id, results, metadata)

    def _print_rich(
        self,
        scan_id: str,
        results: dict[str, Any],
        metadata: dict[str, Any],
    ) -> None:
        """Print with rich tables and colors."""
        if self.console is None:
            return

        self.console.print(f"\n[bold cyan]Scan #{scan_id}[/bold cyan]")
        self.console.print(f"Domain: [bold]{metadata.get('domain', 'N/A')}[/bold]")
        self.console.print(f"Type: {metadata.get('scan_type', 'full')}")

        duration = metadata.get('duration_ms')
        if duration:
            self.console.print(f"Duration: {duration}ms")

        self.console.print()

        # Print each module's results
        for module_name, module_results in results.items():
            if not module_results:
                continue

            self.console.print(f"[bold]{module_name}[/bold]")

            if isinstance(module_results, list) and len(module_results) > 0:
                if isinstance(module_results[0], dict):
                    self._print_module_table(module_name, module_results)
                else:
                    # Simple list of strings/values
                    for item in module_results:
                        self.console.print(f"  • {item}")
            else:
                self.console.print(f"  {module_results}")

            self.console.print()

    def _print_module_table(
        self,
        module_name: str,
        results: list[Any],
    ) -> None:
        """Print results as a rich table."""
        if self.console is None or not results or not isinstance(results[0], dict):
            return
        if Table is None:
            return

        table = Table(title=f"{module_name} Results", show_header=True, header_style="bold")

        # Extract all unique keys from results
        all_keys: set[Any] = set()
        for result in results:
            if isinstance(result, dict):
                all_keys.update(result.keys())

        # Add columns
        for key in sorted(all_keys):
            if key == "severity":
                table.add_column(str(key), style="bold")
            else:
                table.add_column(str(key))

        # Add rows with color coding based on severity
        for result in results[:20]:  # Limit to 20 rows for readability
            row_values: list[str] = []
            severity: str = (
                result.get("severity", "info") if isinstance(result, dict) else "info"
            )

            # Map severity to style
            severity_style = self._get_severity_style(severity)

            for key in sorted(all_keys):
                value: Any = result.get(key, "") if isinstance(result, dict) else ""
                value_str = str(value)[:50]  # Truncate long values
                row_values.append(value_str)

            table.add_row(*row_values, style=severity_style)

        self.console.print(table)

        if len(results) > 20:
            self.console.print(f"  ... and {len(results) - 20} more")

    def _get_severity_style(self, severity: str) -> str:
        """Map severity level to rich style."""
        severity_map = {
            "critical": "red",
            "high": "orange1",
            "medium": "yellow",
            "low": "cyan",
            "info": "green",
        }
        return severity_map.get(severity, "white")

    def _print_plain(
        self,
        scan_id: str,
        results: dict[str, Any],
        metadata: dict[str, Any],
    ) -> None:
        """Fallback plain-text output."""
        print(f"\n=== Scan #{scan_id} ===")
        print(f"Domain: {metadata.get('domain', 'N/A')}")
        print(f"Type: {metadata.get('scan_type', 'full')}")

        duration = metadata.get('duration_ms')
        if duration:
            print(f"Duration: {duration}ms")

        print()

        for module_name, module_results in results.items():
            if not module_results:
                continue
            print(f"\n{module_name}:")
            print(json.dumps(module_results, indent=2, default=str))
