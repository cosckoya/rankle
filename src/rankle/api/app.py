"""FastAPI application factory and configuration."""

import json
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from rankle.api.schemas import (
    ScanRequest,
    ScanResponse,
    ScanListResponse,
    ResultsQueryResponse,
    HealthResponse,
    ProgressUpdate,
)
from rankle.core.scanner import RankleScanner
from rankle.db.engine import get_engine, create_all_tables, get_db_session
from rankle.db.repository import ScanRepository
from rankle.db.models import Scan, ScanResult
from rankle.output.registry import OutputRegistry
from config.settings import DATABASE_URL


# Global engine (initialized on startup)
_engine = None


def get_db() -> Session:
    """Dependency injection for database session."""
    global _engine
    if _engine is None:
        db_path = DATABASE_URL.replace("sqlite:///", "")
        _engine = get_engine(db_path)
        create_all_tables(_engine)

    with get_db_session(_engine) as session:
        yield session


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Rankle API",
        description="Web Infrastructure Reconnaissance Tool - REST API",
        version="1.0.0",
    )

    # Initialize database on startup
    @app.on_event("startup")
    async def startup_event():
        global _engine
        db_path = DATABASE_URL.replace("sqlite:///", "")
        _engine = get_engine(db_path)
        create_all_tables(_engine)

    # Health check
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Check API and database health."""
        return HealthResponse(
            status="healthy",
            database="ok",
            version="1.0.0"
        )

    # Create scan
    @app.post("/api/v1/scans", response_model=ScanResponse)
    async def create_scan(request: ScanRequest, db: Session = Depends(get_db)):
        """Create a new scan job."""
        try:
            repo = ScanRepository(db)
            scan = repo.create_scan(request.domain, request.scan_type)
            db.commit()

            # TODO: Start async scan job (use background task)
            # For now, just return created scan record
            return ScanResponse(
                id=scan.id,
                domain=scan.domain,
                scan_type=scan.scan_type,
                scanned_at=scan.scanned_at,
                status=scan.status,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Get scan status
    @app.get("/api/v1/scans/{scan_id}", response_model=ScanResponse)
    async def get_scan(scan_id: int, db: Session = Depends(get_db)):
        """Get scan status and metadata."""
        repo = ScanRepository(db)
        scan = repo.get_scan(scan_id)

        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")

        modules = [
            {
                "module_name": m.module_name,
                "status": m.status,
                "result_count": m.result_count,
            }
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
    async def list_scans(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
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
    async def get_scan_results(
        scan_id: int,
        module_name: str = None,
        limit: int = 100,
        db: Session = Depends(get_db)
    ):
        """Get results for a specific scan (optionally filtered by module)."""
        from sqlalchemy import select, and_

        query = select(ScanResult).where(ScanResult.scan_id == scan_id)

        if module_name:
            query = query.where(ScanResult.module_name == module_name)

        query = query.limit(limit)
        results_list = db.scalars(query).all()

        return ResultsQueryResponse(
            results=[
                {
                    "id": r.id,
                    "scan_id": r.scan_id,
                    "module_name": r.module_name,
                    "result_type": r.result_type,
                    "data": json.loads(r.data_json),
                    "severity": r.severity,
                }
                for r in results_list
            ],
            total=len(results_list),
        )

    # WebSocket for real-time progress
    @app.websocket("/ws/progress/{scan_id}")
    async def websocket_progress(websocket: WebSocket, scan_id: int, db: Session = Depends(get_db)):
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
                import asyncio
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
