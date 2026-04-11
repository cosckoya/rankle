"""
SQLAlchemy 2.x ORM models for Rankle scan persistence.

Four main tables:
- Scan: Master record for each reconnaissance scan
- ScanModule: Per-module execution status and result counts
- ScanResult: Individual result records (polymorphic by module_name)
- Progress: Real-time progress tracking during scan execution
"""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from typing import Any


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ORM models."""
    pass


class Scan(Base):
    """
    Master scan record.

    One Scan per reconnaissance run. Tracks domain, scan type, timestamp,
    duration, overall status, and optional error details.
    """
    __tablename__ = "scan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain: Mapped[str] = mapped_column(String(253), nullable=False, index=True)
    scan_type: Mapped[str] = mapped_column(String(50), nullable=False)
    scanned_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False, index=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # "completed" | "partial" | "error"
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    modules: Mapped[list["ScanModule"]] = relationship(
        "ScanModule",
        back_populates="scan",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    results: Mapped[list["ScanResult"]] = relationship(
        "ScanResult",
        back_populates="scan",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    progress: Mapped["Progress | None"] = relationship(
        "Progress",
        back_populates="scan",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin"
    )

    __table_args__ = (
        Index("idx_scan_domain", "domain"),
        Index("idx_scan_scanned_at", "scanned_at"),
    )


class ScanModule(Base):
    """
    Per-module execution record.

    Tracks which modules ran during a scan, their status, result count,
    and any errors encountered.
    """
    __tablename__ = "scan_module"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scan.id"), nullable=False, index=True)
    module_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # "ok" | "partial" | "error"
    result_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_detail: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    scan: Mapped[Scan] = relationship("Scan", back_populates="modules")

    __table_args__ = (
        Index("idx_module_scan_name", "scan_id", "module_name"),
    )


class ScanResult(Base):
    """
    Individual result record per detection/analysis.

    Polymorphic by module_name: each module type stores different result structures.
    data_json contains the full result payload (serialized).
    """
    __tablename__ = "scan_result"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scan.id"), nullable=False, index=True)
    module_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    result_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "dns_record", "ssl_cert", "technology", etc
    data_json: Mapped[str] = mapped_column(Text, nullable=False)  # Full result payload
    severity: Mapped[str | None] = mapped_column(String(20), nullable=True)  # "critical" | "high" | "medium" | "low" | "info"

    # Relationships
    scan: Mapped[Scan] = relationship("Scan", back_populates="results")

    __table_args__ = (
        Index("idx_result_scan_module", "scan_id", "module_name"),
    )


class Progress(Base):
    """
    Real-time progress tracking during scan execution.

    One record per active scan. Updated as modules complete.
    """
    __tablename__ = "progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scan.id"), nullable=False, unique=True, index=True)
    current_module: Mapped[str | None] = mapped_column(String(50), nullable=True)
    progress_pct: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0-100
    total_modules: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_modules: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    # Relationships
    scan: Mapped[Scan] = relationship("Scan", back_populates="progress")
