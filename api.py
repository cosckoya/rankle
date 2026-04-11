#!/usr/bin/env python3
"""Rankle API Server entry point.

Run with:
  uv run python api.py

API will be available at http://localhost:8000
Docs at http://localhost:8000/docs
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rankle.api.app import create_app
import uvicorn


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=False,
    )
