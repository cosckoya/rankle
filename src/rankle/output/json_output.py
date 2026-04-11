"""
JSON file output backend - exports scan results to JSON files.

Files are saved in reports/ directory with timestamp and domain in filename.
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from rankle.output.base import OutputBackend


class JSONOutput(OutputBackend):
    """
    Write scan results to JSON file in reports/ directory.

    File naming: reports/{domain}_{timestamp}.json
    """

    def __init__(self, output_dir: str = "reports") -> None:
        """
        Initialize JSON output backend.

        Args:
            output_dir: Directory to write JSON files to. Defaults to "reports".
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def write(
        self,
        scan_id: str,
        results: dict[str, Any],
        metadata: dict[str, Any]
    ) -> None:
        """
        Write results to JSON file.

        Args:
            scan_id: Scan identifier (used in logging, not filename).
            results: Results dict with module names as keys.
            metadata: Scan metadata (domain, duration, etc).
        """
        domain = metadata.get("domain", "unknown")
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        # Construct filename
        filename = f"rankle_{domain}_{timestamp}.json"
        filepath = self.output_dir / filename

        # Prepare output structure
        output_data = {
            "meta": {
                "scan_id": scan_id,
                "domain": domain,
                "scan_type": metadata.get("scan_type", "full"),
                "scanned_at": metadata.get("scanned_at", datetime.now(UTC).isoformat()),
                "duration_ms": metadata.get("duration_ms"),
            },
            "results": results,
        }

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, default=str)

        # Log (using print as fallback, ideally logger)
        print(f"✓ Results exported to {filepath}")
