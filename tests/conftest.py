"""Shared pytest fixtures and configuration for Rankle tests.

This module provides base fixtures for:
- Domain and URL fixtures
- Mock HTTP responses
- Mock DNS responses
- Session and result fixtures
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest
import requests
from dns.rdataclass import IN
from dns.rdatatype import A, AAAA, CNAME, MX, NS, TXT
from dns.resolver import NXDOMAIN, Answer


# ============================================================================
# DOMAIN FIXTURES
# ============================================================================


@pytest.fixture
def valid_domain() -> str:
    """Fixture: valid domain name."""
    return "example.com"


@pytest.fixture
def invalid_domain() -> str:
    """Fixture: invalid domain name."""
    return "invalid domain"


@pytest.fixture
def google_domain() -> str:
    """Fixture: Google domain for integration tests."""
    return "google.com"


@pytest.fixture
def test_domains() -> list[str]:
    """Fixture: multiple test domains."""
    return ["example.com", "google.com", "github.com"]


@pytest.fixture
def test_subdomains() -> list[str]:
    """Fixture: test subdomains."""
    return ["www.example.com", "mail.example.com", "api.example.com"]


# ============================================================================
# HTTP RESPONSE FIXTURES
# ============================================================================


@pytest.fixture
def mock_http_response_dict() -> dict[str, Any]:
    """Fixture: sample HTTP response data."""
    return {
        "status_code": 200,
        "headers": {
            "Server": "Apache/2.4.41",
            "X-Powered-By": "PHP/7.4.3",
            "Content-Type": "text/html; charset=UTF-8",
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Strict-Transport-Security": "max-age=31536000",
        },
        "content": b"<html><head><meta name='generator' content='WordPress 6.4'/></head></html>",
        "cookies": {"wordpress_logged_in": "test_value"},
        "ip": "93.184.216.34",
    }


@pytest.fixture
def mock_html_wordpress() -> bytes:
    """Fixture: WordPress HTML snippet."""
    return b"""
    <html>
    <head>
        <meta name="generator" content="WordPress 6.4" />
        <link rel="stylesheet" href="/wp-content/themes/twentytwentythree/style.css" />
    </head>
    <body>
        <script src="/wp-includes/js/jquery/jquery.js"></script>
    </body>
    </html>
    """


@pytest.fixture
def mock_html_react() -> bytes:
    """Fixture: React application HTML snippet."""
    return b"""
    <html>
    <head>
        <meta name="react-app" content="true" />
    </head>
    <body>
        <div id="root"></div>
        <script src="/static/js/main.abc123.js"></script>
        <script>
            window.__REACT_APP__ = {version: "18.2.0"};
        </script>
    </body>
    </html>
    """


@pytest.fixture
def mock_html_django() -> bytes:
    """Fixture: Django application HTML snippet."""
    return b"""
    <html>
    <head>
        <meta name="csrf-token" content="xyz123" />
    </head>
    <body>
        <form method="post">
            {% csrf_token %}
            <input type="text" />
        </form>
    </body>
    </html>
    """


# ============================================================================
# DNS RESPONSE FIXTURES
# ============================================================================


@pytest.fixture
def mock_dns_a_records() -> dict[str, list[str]]:
    """Fixture: mock A record responses."""
    return {
        "example.com": ["93.184.216.34"],
        "google.com": ["142.251.32.46"],
    }


@pytest.fixture
def mock_dns_mx_records() -> dict[str, list[str]]:
    """Fixture: mock MX record responses."""
    return {
        "example.com": ["mail.example.com"],
        "google.com": ["aspmx.l.google.com", "alt1.aspmx.l.google.com"],
    }


@pytest.fixture
def mock_dns_ns_records() -> dict[str, list[str]]:
    """Fixture: mock NS record responses."""
    return {
        "example.com": ["a.iana-servers.net", "b.iana-servers.net"],
        "google.com": ["ns1.google.com", "ns2.google.com"],
    }


@pytest.fixture
def mock_dns_txt_records() -> dict[str, list[str]]:
    """Fixture: mock TXT record responses."""
    return {
        "example.com": [
            "v=spf1 -all",
            "google-site-verification=abcdef123456",
        ],
        "google.com": [
            "v=spf1 include:_spf.google.com ~all",
            "google-site-verification=xyz789",
        ],
    }


# ============================================================================
# MOCK SESSION & REQUEST FIXTURES
# ============================================================================


@pytest.fixture
def mock_session() -> MagicMock:
    """Fixture: mocked HTTP session."""
    session = MagicMock()
    session.get = MagicMock()
    session.head = MagicMock()
    session.options = MagicMock()
    session.timeout = 45
    session.retries = MagicMock()
    return session


@pytest.fixture
def mock_requests_response(mock_http_response_dict: dict[str, Any]) -> MagicMock:
    """Fixture: mocked requests.Response object."""
    response = MagicMock(spec=requests.Response)
    response.status_code = mock_http_response_dict["status_code"]
    response.headers = mock_http_response_dict["headers"]
    response.content = mock_http_response_dict["content"]
    response.text = mock_http_response_dict["content"].decode("utf-8")
    response.cookies = mock_http_response_dict["cookies"]
    response.url = "http://example.com"
    response.history = []
    return response


# ============================================================================
# SCAN RESULT FIXTURES
# ============================================================================


@pytest.fixture
def mock_dns_result() -> dict[str, Any]:
    """Fixture: mock DNS analysis result."""
    return {
        "a_records": ["93.184.216.34"],
        "aaaa_records": ["2606:2800:220:1:248:1893:25c8:1946"],
        "mx_records": ["mail.example.com"],
        "ns_records": ["a.iana-servers.net", "b.iana-servers.net"],
        "txt_records": ["v=spf1 -all"],
        "soa_record": "ns1.example.com. hostmaster.example.com. 2024 3600 1800 604800 86400",
    }


@pytest.fixture
def mock_ssl_result() -> dict[str, Any]:
    """Fixture: mock SSL/TLS analysis result."""
    return {
        "subject": {"commonName": "example.com"},
        "issuer": {"commonName": "Let's Encrypt Authority X3"},
        "not_before": "2024-01-01 00:00:00",
        "not_after": "2025-01-01 00:00:00",
        "self_signed": False,
        "cipher_suites": ["TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"],
        "tls_versions": ["TLSv1.2", "TLSv1.3"],
    }


@pytest.fixture
def mock_tech_result() -> dict[str, Any]:
    """Fixture: mock technology detection result."""
    return {
        "WordPress": {
            "confidence": 0.95,
            "version": "6.4",
            "category": "CMS",
            "evidence": ["meta generator tag", "wp-content directory"],
        },
        "PHP": {
            "confidence": 0.85,
            "version": "7.4.3",
            "category": "Language",
            "evidence": ["X-Powered-By header"],
        },
        "Apache": {
            "confidence": 0.90,
            "version": "2.4.41",
            "category": "Web Server",
            "evidence": ["Server header"],
        },
    }


@pytest.fixture
def mock_cdn_result() -> dict[str, Any]:
    """Fixture: mock CDN detection result."""
    return {
        "detected": True,
        "provider": "Cloudflare",
        "confidence": 0.95,
        "evidence": ["CF-Ray header", "Nameserver ns1.ns.cloudflare.com"],
        "asn": "AS13335",
    }


@pytest.fixture
def mock_waf_result() -> dict[str, Any]:
    """Fixture: mock WAF detection result."""
    return {
        "detected": True,
        "waf_name": "ModSecurity",
        "confidence": 0.85,
        "evidence": ["Suspicious request blocked response", "X-ModSecurity header"],
    }


@pytest.fixture
def mock_complete_scan_result(
    mock_dns_result: dict[str, Any],
    mock_ssl_result: dict[str, Any],
    mock_tech_result: dict[str, Any],
) -> dict[str, Any]:
    """Fixture: complete scan result with all modules."""
    return {
        "domain": "example.com",
        "dns": mock_dns_result,
        "ssl": mock_ssl_result,
        "technologies": mock_tech_result,
        "subdomains": ["www.example.com", "mail.example.com"],
        "security_headers": {
            "hsts": True,
            "csp": True,
            "x_frame_options": True,
        },
        "http_methods": ["GET", "POST", "OPTIONS"],
        "api_endpoints": ["/api/v1", "/graphql"],
    }


# ============================================================================
# FILE & OUTPUT FIXTURES
# ============================================================================


@pytest.fixture
def tmp_output_dir() -> Generator[Path, None, None]:
    """Fixture: temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_json_report(mock_complete_scan_result: dict[str, Any], tmp_output_dir: Path) -> Path:
    """Fixture: create mock JSON report file."""
    report_path = tmp_output_dir / "scan_report.json"
    report_path.write_text(json.dumps(mock_complete_scan_result, indent=2))
    return report_path


# ============================================================================
# PYTEST MARKERS & CONFIGURATION
# ============================================================================


def pytest_configure(config: Any) -> None:
    """Register custom pytest markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "http: marks tests requiring HTTP mocking")
    config.addinivalue_line("markers", "dns: marks tests requiring DNS mocking")
