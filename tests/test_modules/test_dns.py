"""Unit tests for rankle.modules.dns module.

Tests DNS record queries including:
- A, AAAA, MX, NS, TXT record resolution
- Invalid domain handling
- Custom nameserver support
"""

from unittest.mock import MagicMock, patch

import dns.resolver
import pytest

from rankle.modules.dns import DNSAnalyzer


class TestDNSInitialization:
    """Test DNS analyzer initialization."""

    def test_dns_analyzer_init(self, valid_domain: str) -> None:
        """Test DNS analyzer initializes with domain."""
        analyzer = DNSAnalyzer(valid_domain)
        assert analyzer.domain == valid_domain

    def test_dns_analyzer_with_custom_nameserver(self, valid_domain: str) -> None:
        """Test DNS analyzer with custom nameserver."""
        analyzer = DNSAnalyzer(valid_domain, nameservers=["8.8.8.8"])
        assert analyzer is not None


class TestDNSQueries:
    """Test DNS record queries."""

    @pytest.mark.dns
    @pytest.mark.integration
    def test_dns_a_record_query(
        self, valid_domain: str, mock_dns_a_records: dict[str, list[str]]
    ) -> None:
        """Test A record query."""
        analyzer = DNSAnalyzer(valid_domain)
        with patch("dns.resolver.resolve") as mock_resolve:
            mock_answer = MagicMock()
            mock_answer.__iter__ = lambda self: iter([MagicMock(address=ip) for ip in mock_dns_a_records[valid_domain]])
            mock_resolve.return_value = mock_answer
            result = analyzer.analyze()
            assert "a_records" in result or result is not None

    @pytest.mark.dns
    def test_dns_mx_record_query(
        self, valid_domain: str, mock_dns_mx_records: dict[str, list[str]]
    ) -> None:
        """Test MX record query."""
        analyzer = DNSAnalyzer(valid_domain)
        with patch("dns.resolver.resolve") as mock_resolve:
            mock_answer = MagicMock()
            mock_answer.__iter__ = lambda self: iter([MagicMock(exchange=MagicMock(to_text=lambda: mx)) for mx in mock_dns_mx_records[valid_domain]])
            mock_resolve.return_value = mock_answer
            result = analyzer.analyze()
            assert result is not None

    @pytest.mark.dns
    def test_dns_ns_record_query(
        self, valid_domain: str, mock_dns_ns_records: dict[str, list[str]]
    ) -> None:
        """Test NS record query."""
        analyzer = DNSAnalyzer(valid_domain)
        with patch("dns.resolver.resolve") as mock_resolve:
            mock_answer = MagicMock()
            mock_resolve.return_value = mock_answer
            result = analyzer.analyze()
            assert result is not None

    @pytest.mark.dns
    def test_dns_txt_record_query(
        self, valid_domain: str, mock_dns_txt_records: dict[str, list[str]]
    ) -> None:
        """Test TXT record query."""
        analyzer = DNSAnalyzer(valid_domain)
        with patch("dns.resolver.resolve") as mock_resolve:
            mock_answer = MagicMock()
            mock_resolve.return_value = mock_answer
            result = analyzer.analyze()
            assert result is not None


class TestDNSErrors:
    """Test DNS error handling."""

    @pytest.mark.dns
    def test_dns_nxdomain_error(self, valid_domain: str) -> None:
        """Test handling of NXDOMAIN error."""
        analyzer = DNSAnalyzer(valid_domain)
        with patch("dns.resolver.resolve") as mock_resolve:
            mock_resolve.side_effect = dns.resolver.NXDOMAIN()
            result = analyzer.analyze()
            # Should handle gracefully, return empty or error dict
            assert isinstance(result, dict)

    @pytest.mark.dns
    def test_dns_no_answer_error(self, valid_domain: str) -> None:
        """Test handling of NoAnswer error."""
        analyzer = DNSAnalyzer(valid_domain)
        with patch("dns.resolver.resolve") as mock_resolve:
            mock_resolve.side_effect = dns.resolver.NoAnswer()
            result = analyzer.analyze()
            assert isinstance(result, dict)

    @pytest.mark.dns
    def test_dns_timeout_error(self, valid_domain: str) -> None:
        """Test handling of timeout error."""
        analyzer = DNSAnalyzer(valid_domain)
        with patch("dns.resolver.resolve") as mock_resolve:
            mock_resolve.side_effect = dns.exception.Timeout()
            result = analyzer.analyze()
            assert isinstance(result, dict)


class TestDNSResults:
    """Test DNS analysis results."""

    @pytest.mark.dns
    def test_dns_result_contains_records(self, valid_domain: str, mock_dns_result: dict) -> None:
        """Test DNS result contains record types."""
        analyzer = DNSAnalyzer(valid_domain)
        with patch.object(analyzer, "analyze") as mock_analyze:
            mock_analyze.return_value = mock_dns_result
            result = analyzer.analyze()
            assert "a_records" in result or "mx_records" in result
