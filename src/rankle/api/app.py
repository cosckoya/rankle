"""FastAPI application factory and configuration."""

import asyncio
import json
from contextlib import asynccontextmanager
from typing import Any, Generator

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from rankle.api.schemas import (
    ScanRequest,
    ScanResponse,
    ScanListResponse,
    ResultsQueryResponse,
    HealthResponse,
)
from rankle.db.engine import get_engine, create_all_tables, get_db_session
from rankle.db.repository import ScanRepository
from rankle.db.models import ScanResult
from config.settings import DATABASE_URL


# Global engine (initialized on startup)
_engine: Any = None


def get_db() -> Generator[Session, None, None]:
    """Dependency injection for database session."""
    global _engine
    if _engine is None:
        db_path = DATABASE_URL.replace("sqlite:///", "")
        _engine = get_engine(db_path)
        create_all_tables(_engine)

    with get_db_session(_engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Lifespan context manager for startup and shutdown events."""
    global _engine
    db_path = DATABASE_URL.replace("sqlite:///", "")
    _engine = get_engine(db_path)
    create_all_tables(_engine)
    yield
    # Cleanup on shutdown if needed
    if _engine:
        _engine.dispose()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Rankle API",
        description="Web Infrastructure Reconnaissance Tool - REST API",
        version="0.1-alpha",
        lifespan=lifespan,
    )

    # Health check
    @app.get("/health", response_model=HealthResponse)
    async def health_check() -> HealthResponse:  # noqa: ARG001
        """Check API and database health."""
        return HealthResponse(
            status="healthy",
            database="ok",
            version="0.1-alpha"
        )

    # Create scan
    @app.post("/api/v1/scans", response_model=ScanResponse)
    async def create_scan(  # noqa: ARG001
        request: ScanRequest,
        db: Session = Depends(get_db),
    ) -> ScanResponse:
        """Create a new scan job."""
        try:
            repo = ScanRepository(db)
            scan = repo.create_scan(request.domain, request.scan_type)
            db.commit()

            return ScanResponse(
                id=scan.id,
                domain=scan.domain,
                scan_type=scan.scan_type,
                scanned_at=scan.scanned_at,
                status=scan.status,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    # Get scan status
    @app.get("/api/v1/scans/{scan_id}", response_model=ScanResponse)
    async def get_scan(  # noqa: ARG001
        scan_id: int,
        db: Session = Depends(get_db),
    ) -> ScanResponse:
        """Get scan status and metadata."""
        repo = ScanRepository(db)
        scan = repo.get_scan(scan_id)

        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")

        from rankle.api.schemas import ModuleResultSchema
        modules = [
            ModuleResultSchema(
                module_name=m.module_name,
                status=m.status,
                result_count=m.result_count,
            )
            for m in scan.modules
        ]

        return ScanResponse(
            id=scan.id,
            domain=scan.domain,
            scan_type=scan.scan_type,
            scanned_at=scan.scanned_at,
            status=scan.status,
            duration_ms=scan.duration_ms,
            modules=modules,
            error_message=scan.error_message,
        )

    # List scans
    @app.get("/api/v1/scans", response_model=ScanListResponse)
    async def list_scans(  # noqa: ARG001
        limit: int = 100,
        offset: int = 0,
        db: Session = Depends(get_db),
    ) -> ScanListResponse:
        """List all scans (paginated)."""
        repo = ScanRepository(db)
        scans = repo.list_all_scans(limit=limit)

        return ScanListResponse(
            scans=[
                ScanResponse(
                    id=s.id,
                    domain=s.domain,
                    scan_type=s.scan_type,
                    scanned_at=s.scanned_at,
                    status=s.status,
                    duration_ms=s.duration_ms,
                )
                for s in scans
            ],
            total=len(scans),
        )

    # Get scan results
    @app.get("/api/v1/scans/{scan_id}/results", response_model=ResultsQueryResponse)
    async def get_scan_results(  # noqa: ARG001
        scan_id: int,
        module_name: str | None = None,
        limit: int = 100,
        db: Session = Depends(get_db),
    ) -> ResultsQueryResponse:
        """Get results for a specific scan (optionally filtered by module)."""
        from sqlalchemy import select
        from rankle.api.schemas import ScanResultResponse

        query = select(ScanResult).where(ScanResult.scan_id == scan_id)

        if module_name:
            query = query.where(ScanResult.module_name == module_name)

        query = query.limit(limit)
        results_list = db.scalars(query).all()

        return ResultsQueryResponse(
            results=[
                ScanResultResponse(
                    id=r.id,
                    scan_id=r.scan_id,
                    module_name=r.module_name,
                    result_type=r.result_type,
                    data=json.loads(r.data_json),
                    severity=r.severity,
                )
                for r in results_list
            ],
            total=len(results_list),
        )

    # WebSocket for real-time progress
    @app.websocket("/ws/progress/{scan_id}")
    async def websocket_progress(  # noqa: ARG001
        websocket: WebSocket,
        scan_id: int,
        db: Session = Depends(get_db),
    ) -> None:
        """WebSocket endpoint for real-time scan progress updates."""
        await websocket.accept()

        try:
            while True:
                repo = ScanRepository(db)
                scan = repo.get_scan(scan_id)

                if not scan:
                    await websocket.send_json({"error": "Scan not found"})
                    break

                if scan.progress:
                    progress_data = {
                        "scan_id": scan.id,
                        "current_module": scan.progress.current_module,
                        "progress_pct": scan.progress.progress_pct,
                        "completed_modules": scan.progress.completed_modules,
                        "total_modules": scan.progress.total_modules,
                    }
                    await websocket.send_json(progress_data)

                # Check if scan is complete
                if scan.status in ["completed", "error", "partial"]:
                    await websocket.send_json({
                        "status": "complete",
                        "scan_status": scan.status,
                        "duration_ms": scan.duration_ms,
                    })
                    break

                # Wait 500ms before next update
                await asyncio.sleep(0.5)

        except WebSocketDisconnect:
            pass
        except Exception as e:
            await websocket.send_json({"error": str(e)})
        finally:
            await websocket.close()

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
