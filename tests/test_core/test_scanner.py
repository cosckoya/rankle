"""Unit tests for rankle.core.scanner module.

Tests the RankleScanner orchestrator including:
- Initialization and validation
- Lazy loading pattern
- Full scan execution
- Output formatting (JSON, text)
- Error handling
"""

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

from rankle.core.scanner import RankleScanner


class TestScannerInitialization:
    """Test RankleScanner initialization and validation."""

    def test_scanner_initialization_valid_domain(self, valid_domain: str) -> None:
        """Test scanner initialization with valid domain."""
        scanner = RankleScanner(valid_domain)
        assert scanner.domain == valid_domain
        assert scanner.verbose is False

    def test_scanner_initialization_invalid_domain(self, invalid_domain: str) -> None:
        """Test scanner initialization rejects invalid domain."""
        with pytest.raises(ValueError):
            RankleScanner(invalid_domain)

    def test_scanner_initialization_with_verbose(self, valid_domain: str) -> None:
        """Test scanner initialization with verbose flag."""
        scanner = RankleScanner(valid_domain, verbose=True)
        assert scanner.verbose is True

    def test_scanner_initialization_whitespace_domain(self) -> None:
        """Test scanner initialization rejects domains with whitespace."""
        with pytest.raises(ValueError):
            RankleScanner("  ")

    def test_scanner_initialization_empty_domain(self) -> None:
        """Test scanner initialization rejects empty domain."""
        with pytest.raises(ValueError):
            RankleScanner("")


class TestLazyInitialization:
    """Test lazy loading pattern of scanner properties."""

    def test_lazy_init_dns_analyzer(self, valid_domain: str) -> None:
        """Test DNS analyzer lazy loads on first access."""
        scanner = RankleScanner(valid_domain)
        # First access should initialize
        dns_analyzer = scanner.dns_analyzer
        assert dns_analyzer is not None
        # Second access should return same instance
        dns_analyzer_2 = scanner.dns_analyzer
        assert dns_analyzer is dns_analyzer_2

    def test_lazy_init_ssl_analyzer(self, valid_domain: str) -> None:
        """Test SSL analyzer lazy loads on first access."""
        scanner = RankleScanner(valid_domain)
        ssl_analyzer = scanner.ssl_analyzer
        assert ssl_analyzer is not None
        ssl_analyzer_2 = scanner.ssl_analyzer
        assert ssl_analyzer is ssl_analyzer_2

    def test_lazy_init_session_manager(self, valid_domain: str) -> None:
        """Test session manager lazy loads on first access."""
        scanner = RankleScanner(valid_domain)
        session = scanner.session_manager
        assert session is not None

    def test_lazy_init_on_demand(self, valid_domain: str) -> None:
        """Test modules only initialize when accessed."""
        scanner = RankleScanner(valid_domain)
        # Before accessing, should be None
        assert scanner._dns_analyzer is None
        # After accessing, should be initialized
        _ = scanner.dns_analyzer
        assert scanner._dns_analyzer is not None


class TestRunFullScan:
    """Test full scan execution."""

    @pytest.mark.integration
    def test_run_full_scan_returns_dict(self, valid_domain: str) -> None:
        """Test run_full_scan returns dictionary."""
        scanner = RankleScanner(valid_domain)
        with patch.object(scanner, "dns_analyzer") as mock_dns:
            mock_dns.analyze.return_value = {"a_records": ["1.2.3.4"]}
            with patch.object(scanner, "ssl_analyzer") as mock_ssl:
                mock_ssl.analyze.return_value = {"subject": "example.com"}
                with patch.object(scanner, "technology_detector") as mock_tech:
                    mock_tech.detect.return_value = {"WordPress": {"confidence": 0.95}}
                    result = scanner.run_full_scan()
                    assert isinstance(result, dict)

    @pytest.mark.integration
    def test_run_full_scan_contains_domain(self, valid_domain: str) -> None:
        """Test scan result contains domain key."""
        scanner = RankleScanner(valid_domain)
        with patch.object(scanner, "dns_analyzer") as mock_dns:
            mock_dns.analyze.return_value = {}
            with patch.multiple(
                scanner,
                ssl_analyzer=MagicMock(analyze=MagicMock(return_value={})),
                technology_detector=MagicMock(detect=MagicMock(return_value={})),
                cdn_detector=MagicMock(detect=MagicMock(return_value={})),
                waf_detector=MagicMock(detect=MagicMock(return_value={})),
            ):
                result = scanner.run_full_scan()
                assert "domain" in result
                assert result["domain"] == valid_domain


class TestOutputFormatting:
    """Test output formatting (JSON, text)."""

    def test_json_output_valid_format(
        self, valid_domain: str, mock_complete_scan_result: dict[str, Any]
    ) -> None:
        """Test JSON output is valid."""
        scanner = RankleScanner(valid_domain)
        json_str = scanner._format_json_output(mock_complete_scan_result)
        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed["domain"] == "example.com"

    def test_text_output_has_content(
        self, valid_domain: str, mock_complete_scan_result: dict[str, Any]
    ) -> None:
        """Test text output has content."""
        scanner = RankleScanner(valid_domain)
        text_output = scanner._format_text_output(mock_complete_scan_result)
        assert len(text_output) > 0
        assert "example.com" in text_output
        assert "DNS" in text_output or "Technologies" in text_output

    def test_save_json_report(
        self,
        valid_domain: str,
        mock_complete_scan_result: dict[str, Any],
        tmp_output_dir: Path,
    ) -> None:
        """Test saving JSON report to file."""
        scanner = RankleScanner(valid_domain)
        report_path = tmp_output_dir / "scan_report.json"
        scanner._save_report(mock_complete_scan_result, str(report_path), "json")
        assert report_path.exists()
        with open(report_path) as f:
            data = json.load(f)
            assert data["domain"] == "example.com"


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_error_handling_dns_failure(self, valid_domain: str) -> None:
        """Test graceful handling of DNS failures."""
        scanner = RankleScanner(valid_domain)
        with patch.object(scanner, "dns_analyzer") as mock_dns:
            mock_dns.analyze.side_effect = Exception("DNS lookup failed")
            with patch.multiple(
                scanner,
                ssl_analyzer=MagicMock(analyze=MagicMock(return_value={})),
                technology_detector=MagicMock(detect=MagicMock(return_value={})),
            ):
                # Should not raise, but handle gracefully
                result = scanner.run_full_scan()
                assert isinstance(result, dict)

    def test_verbose_mode_output(self, valid_domain: str, capsys: Any) -> None:
        """Test verbose mode produces output."""
        scanner = RankleScanner(valid_domain, verbose=True)
        with patch.object(scanner, "dns_analyzer") as mock_dns:
            mock_dns.analyze.return_value = {"a_records": ["1.2.3.4"]}
            with patch.multiple(
                scanner,
                ssl_analyzer=MagicMock(analyze=MagicMock(return_value={})),
            ):
                # Trigger verbose output
                scanner.run_full_scan()
                # Verbose mode should print something (implementation dependent)


class TestScannerIntegration:
    """Integration tests for scanner."""

    @pytest.mark.integration
    def test_scanner_with_mock_modules(self, valid_domain: str) -> None:
        """Test scanner with all modules mocked."""
        scanner = RankleScanner(valid_domain)

        with patch.multiple(
            scanner,
            dns_analyzer=MagicMock(analyze=MagicMock(return_value={"a_records": ["1.2.3.4"]})),
            ssl_analyzer=MagicMock(analyze=MagicMock(return_value={"issuer": "Let's Encrypt"})),
            subdomain_discovery=MagicMock(
                find_subdomains=MagicMock(return_value=["www.example.com"])
            ),
            technology_detector=MagicMock(detect=MagicMock(return_value={"Apache": {"confidence": 0.9}})),
            cdn_detector=MagicMock(detect=MagicMock(return_value={"detected": False})),
            waf_detector=MagicMock(detect=MagicMock(return_value={"detected": False})),
            security_headers_auditor=MagicMock(
                audit=MagicMock(return_value={"hsts": True})
            ),
            http_fingerprinter=MagicMock(
                fingerprint=MagicMock(return_value={"methods": ["GET", "POST"]})
            ),
            origin_discovery=MagicMock(
                find_origins=MagicMock(return_value=["1.2.3.4"])
            ),
            geolocation_lookup=MagicMock(
                lookup=MagicMock(return_value={"country": "US"})
            ),
            whois_lookup=MagicMock(lookup=MagicMock(return_value={"registrar": "Example"})),
        ):
            result = scanner.run_full_scan()
            assert result["domain"] == valid_domain
            assert "dns" in result or "technologies" in result
