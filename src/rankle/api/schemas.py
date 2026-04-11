"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    """Request to create a new scan."""
    domain: str = Field(..., description="Target domain to scan (e.g., example.com)")
    scan_type: str = Field(default="full", description="Type of scan: full, dns, ssl, etc")


class ModuleResultSchema(BaseModel):
    """Individual module result."""
    module_name: str
    status: str  # "ok", "partial", "error"
    result_count: int


class ScanResponse(BaseModel):
    """Response for scan status/details."""
    id: int
    domain: str
    scan_type: str
    scanned_at: datetime
    status: str
    duration_ms: Optional[int] = None
    modules: list[ModuleResultSchema] = []
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class ScanListResponse(BaseModel):
    """Response for listing scans."""
    scans: list[ScanResponse]
    total: int


class ScanResultResponse(BaseModel):
    """Individual scan result record."""
    id: int
    scan_id: int
    module_name: str
    result_type: str
    data: dict[str, Any]
    severity: Optional[str] = None

    class Config:
        from_attributes = True


class ResultsQueryResponse(BaseModel):
    """Response for querying results."""
    results: list[ScanResultResponse]
    total: int


class ProgressUpdate(BaseModel):
    """Real-time progress update via WebSocket."""
    scan_id: int
    current_module: str
    progress_pct: int
    completed_modules: int
    total_modules: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    database: str = "ok"
    version: str = "0.1-alpha"
