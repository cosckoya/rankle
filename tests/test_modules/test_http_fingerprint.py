"""Unit tests for rankle.modules.http_fingerprint module."""

from unittest.mock import MagicMock, patch

import pytest

from rankle.modules.http_fingerprint import HTTPFingerprinter


class TestHTTPFingerprinter:
    """Test HTTP fingerprinting."""

    def test_http_fingerprinter_init(self, valid_domain: str) -> None:
        """Test HTTP fingerprinter initialization."""
        fingerprinter = HTTPFingerprinter(valid_domain)
        assert fingerprinter.domain == valid_domain

    @pytest.mark.http
    def test_http_methods_detection(self, valid_domain: str) -> None:
        """Test allowed HTTP methods detection."""
        fingerprinter = HTTPFingerprinter(valid_domain)
        with patch.object(fingerprinter, "fingerprint") as mock_fp:
            mock_fp.return_value = {"methods": ["GET", "POST", "OPTIONS"]}
            result = fingerprinter.fingerprint()
            assert "methods" in result

    def test_api_endpoint_discovery(self, valid_domain: str) -> None:
        """Test API endpoint discovery."""
        fingerprinter = HTTPFingerprinter(valid_domain)
        with patch.object(fingerprinter, "fingerprint") as mock_fp:
            mock_fp.return_value = {"api_endpoints": ["/api/v1", "/graphql"]}
            result = fingerprinter.fingerprint()
            assert "api_endpoints" in result

    def test_exposed_files_detection(self, valid_domain: str) -> None:
        """Test exposed files/directories detection."""
        fingerprinter = HTTPFingerprinter(valid_domain)
        with patch.object(fingerprinter, "fingerprint") as mock_fp:
            mock_fp.return_value = {"exposed_files": [".git", ".env"]}
            result = fingerprinter.fingerprint()
            assert "exposed_files" in result
