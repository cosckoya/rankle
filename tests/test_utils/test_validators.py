"""Unit tests for rankle.utils.validators module."""

import pytest

from rankle.utils.validators import (
    sanitize_filename,
    validate_domain,
    validate_ip,
    validate_url,
)


class TestDomainValidation:
    """Test domain validation."""

    def test_valid_domain(self, valid_domain: str) -> None:
        """Test valid domain passes validation."""
        assert validate_domain(valid_domain) is True

    def test_invalid_domain_with_space(self) -> None:
        """Test domain with space fails."""
        assert validate_domain("invalid domain") is False

    def test_invalid_domain_single_label(self) -> None:
        """Test single label domain fails."""
        assert validate_domain("localhost") is False

    def test_invalid_domain_leading_hyphen(self) -> None:
        """Test domain with leading hyphen fails."""
        assert validate_domain("-example.com") is False

    def test_invalid_domain_trailing_hyphen(self) -> None:
        """Test domain with trailing hyphen fails."""
        assert validate_domain("example-.com") is False

    def test_valid_subdomain(self) -> None:
        """Test valid subdomain passes."""
        assert validate_domain("www.example.com") is True

    def test_valid_deep_subdomain(self) -> None:
        """Test deep subdomain passes."""
        assert validate_domain("api.v1.example.com") is True


class TestIPValidation:
    """Test IP address validation."""

    def test_valid_ipv4(self) -> None:
        """Test valid IPv4 address."""
        assert validate_ip("192.168.1.1") is True
        assert validate_ip("8.8.8.8") is True

    def test_invalid_ipv4(self) -> None:
        """Test invalid IPv4 address."""
        assert validate_ip("256.1.1.1") is False
        assert validate_ip("192.168.1") is False

    def test_valid_ipv6(self) -> None:
        """Test valid IPv6 address."""
        assert validate_ip("2001:db8::1") is True
        assert validate_ip("::1") is True

    def test_invalid_ipv6(self) -> None:
        """Test invalid IPv6 address."""
        assert validate_ip("gggg::1") is False


class TestURLValidation:
    """Test URL validation."""

    def test_valid_http_url(self) -> None:
        """Test valid HTTP URL."""
        assert validate_url("http://example.com") is True

    def test_valid_https_url(self) -> None:
        """Test valid HTTPS URL."""
        assert validate_url("https://example.com") is True

    def test_invalid_url_no_scheme(self) -> None:
        """Test URL without scheme fails."""
        assert validate_url("example.com") is False

    def test_invalid_url_no_netloc(self) -> None:
        """Test URL without netloc fails."""
        assert validate_url("http://") is False


class TestFilenameSanitization:
    """Test filename sanitization."""

    def test_sanitize_valid_filename(self) -> None:
        """Test valid filename unchanged."""
        result = sanitize_filename("scan_report.json")
        assert "scan_report.json" in result or result == "scan_report.json"

    def test_sanitize_removes_windows_invalid_chars(self) -> None:
        """Test removes Windows-invalid characters."""
        result = sanitize_filename("file<name>.txt")
        assert "<" not in result
        assert ">" not in result

    def test_sanitize_removes_path_traversal(self) -> None:
        """Test removes path traversal sequences."""
        result = sanitize_filename("../../etc/passwd")
        assert ".." not in result

    def test_sanitize_length_limit(self) -> None:
        """Test filename length is limited."""
        long_name = "a" * 500
        result = sanitize_filename(long_name)
        assert len(result) <= 200

    def test_sanitize_preserves_extension(self) -> None:
        """Test file extension preserved."""
        result = sanitize_filename("report.json")
        assert ".json" in result or "json" in result
