"""
Type aliases for Rankle project.

Provides readable type aliases for complex types used throughout the codebase.
Requires Python 3.12+ for PEP 695 'type' statement, or Python 3.10+ for TypeAlias.
"""

from typing import Any

# Python 3.10+ compatible type aliases using TypeAlias

# Results and responses
ScanResults = dict[str, Any]
"""Complete scan results dictionary from RankleScanner."""

DetectionResults = dict[str, Any]
"""Technology/CDN/WAF detection results."""

DNSRecords = dict[str, list[str]]
"""DNS records dictionary mapping record type to values."""

# Evidence and confidence
Evidence = list[dict[str, Any]]
"""List of evidence items with type, detail, and weight."""

# HTTP related
Headers = dict[str, str]
"""HTTP headers dictionary."""

Cookies = list[str]
"""List of cookie names."""

# Network related
IPAddresses = list[str]
"""List of IP addresses as strings."""

# Detection signatures
Signatures = dict[str, dict[str, Any]]
"""Detection signatures dictionary."""

# Configuration
ConfigDict = dict[str, Any]
"""Configuration dictionary."""

__all__ = [
    "ScanResults",
    "DetectionResults",
    "DNSRecords",
    "Evidence",
    "Headers",
    "Cookies",
    "IPAddresses",
    "Signatures",
    "ConfigDict",
]
