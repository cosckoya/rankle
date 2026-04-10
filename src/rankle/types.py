"""Type aliases for Rankle project.

Provides readable type aliases for complex types used throughout the codebase.
Requires Python 3.11+ for modern type syntax (dict[str, Any], str | None).
"""

from typing import Any, TypeAlias


# ============================================================================
# Scan Results & Detection
# ============================================================================

ScanResults: TypeAlias = dict[str, Any]
"""Complete scan results dictionary from RankleScanner including all modules."""

DetectionResults: TypeAlias = dict[str, Any]
"""Technology/CDN/WAF detection results with confidence scores."""

AnalysisResult: TypeAlias = dict[str, Any]
"""Generic analysis result from any module or detector."""

# ============================================================================
# DNS & Network
# ============================================================================

DNSRecords: TypeAlias = dict[str, list[str]]
"""DNS records dictionary mapping record type (A, MX, NS, etc.) to values."""

IPAddresses: TypeAlias = list[str]
"""List of IP addresses as strings."""

Subdomains: TypeAlias = list[str]
"""List of discovered subdomains."""

# ============================================================================
# Evidence & Confidence
# ============================================================================

Evidence: TypeAlias = list[dict[str, Any]]
"""List of evidence items with type, detail, and weight for confidence scoring."""

ConfidenceScore: TypeAlias = float
"""Confidence score as float between 0.0 (low) and 1.0 (high)."""

# ============================================================================
# HTTP Related
# ============================================================================

Headers: TypeAlias = dict[str, str]
"""HTTP headers dictionary."""

Cookies: TypeAlias = dict[str, str]
"""HTTP cookies dictionary."""

HTTPMethods: TypeAlias = list[str]
"""Allowed HTTP methods (GET, POST, OPTIONS, etc.)."""

# ============================================================================
# Technology Detection
# ============================================================================

TechDetection: TypeAlias = dict[str, dict[str, Any]]
"""Technology detection result: {tech_name: {confidence, version, category, evidence}}."""

CVEList: TypeAlias = list[dict[str, Any]]
"""List of CVE entries with metadata."""

# ============================================================================
# Configuration & Signatures
# ============================================================================

Signatures: TypeAlias = dict[str, dict[str, Any]]
"""Detection signatures dictionary (patterns, regex, etc.)."""

ConfigDict: TypeAlias = dict[str, Any]
"""Configuration dictionary."""

# ============================================================================
# Optional/Nullable Types
# ============================================================================

OptionalStr: TypeAlias = str | None
"""Optional string type."""

OptionalInt: TypeAlias = int | None
"""Optional integer type."""

OptionalDict: TypeAlias = dict[str, Any] | None
"""Optional dictionary type."""

OptionalList: TypeAlias = list[str] | None
"""Optional list of strings."""

__all__ = [
    "AnalysisResult",
    "CVEList",
    "ConfidenceScore",
    "ConfigDict",
    "Cookies",
    "DNSRecords",
    "DetectionResults",
    "Evidence",
    "HTTPMethods",
    "Headers",
    "IPAddresses",
    "OptionalDict",
    "OptionalInt",
    "OptionalList",
    "OptionalStr",
    "ScanResults",
    "Signatures",
    "Subdomains",
    "TechDetection",
]
