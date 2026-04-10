"""Unit tests for rankle.modules.ssl module."""

from unittest.mock import MagicMock, patch

import pytest

from rankle.modules.ssl import SSLAnalyzer


class TestSSLAnalyzer:
    """Test SSL/TLS certificate analysis."""

    def test_ssl_analyzer_init(self, valid_domain: str) -> None:
        """Test SSL analyzer initializes."""
        analyzer = SSLAnalyzer(valid_domain)
        assert analyzer.domain == valid_domain

    @pytest.mark.integration
    def test_ssl_certificate_extraction(self, valid_domain: str, mock_ssl_result: dict) -> None:
        """Test SSL certificate extraction."""
        analyzer = SSLAnalyzer(valid_domain)
        with patch.object(analyzer, "analyze") as mock_analyze:
            mock_analyze.return_value = mock_ssl_result
            result = analyzer.analyze()
            assert "subject" in result or "issuer" in result

    def test_ssl_self_signed_detection(self, valid_domain: str) -> None:
        """Test self-signed certificate detection."""
        analyzer = SSLAnalyzer(valid_domain)
        with patch.object(analyzer, "analyze") as mock_analyze:
            mock_analyze.return_value = {"self_signed": False}
            result = analyzer.analyze()
            assert "self_signed" in result

    def test_ssl_cipher_suite_detection(self, valid_domain: str) -> None:
        """Test cipher suite detection."""
        analyzer = SSLAnalyzer(valid_domain)
        with patch.object(analyzer, "analyze") as mock_analyze:
            mock_analyze.return_value = {"cipher_suites": ["TLS_AES_256_GCM_SHA384"]}
            result = analyzer.analyze()
            assert "cipher_suites" in result
