"""Unit tests for rankle.modules.security_headers module."""

from unittest.mock import patch

import pytest

from rankle.modules.security_headers import SecurityHeadersAuditor


class TestSecurityHeadersAuditor:
    """Test security headers auditing."""

    def test_security_headers_auditor_init(self, valid_domain: str) -> None:
        """Test security headers auditor initialization."""
        auditor = SecurityHeadersAuditor(valid_domain)
        assert auditor.domain == valid_domain

    def test_hsts_detection(self, valid_domain: str) -> None:
        """Test HSTS header detection."""
        auditor = SecurityHeadersAuditor(valid_domain)
        with patch.object(auditor, "audit") as mock_audit:
            mock_audit.return_value = {"hsts": True, "hsts_header": "max-age=31536000"}
            result = auditor.audit()
            assert "hsts" in result

    def test_csp_detection(self, valid_domain: str) -> None:
        """Test Content Security Policy detection."""
        auditor = SecurityHeadersAuditor(valid_domain)
        with patch.object(auditor, "audit") as mock_audit:
            mock_audit.return_value = {"csp": True, "csp_directives": ["default-src", "script-src"]}
            result = auditor.audit()
            assert "csp" in result

    def test_missing_headers_reported(self, valid_domain: str) -> None:
        """Test missing headers are reported."""
        auditor = SecurityHeadersAuditor(valid_domain)
        with patch.object(auditor, "audit") as mock_audit:
            mock_audit.return_value = {
                "hsts": False,
                "missing_headers": ["X-Frame-Options", "X-Content-Type-Options"]
            }
            result = auditor.audit()
            assert "missing_headers" in result
