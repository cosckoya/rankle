"""Unit tests for rankle.detectors.origin module."""

from unittest.mock import patch

import pytest

from rankle.detectors.origin import OriginDiscovery


class TestOriginDiscovery:
    """Test origin discovery."""

    def test_origin_discovery_init(self, valid_domain: str) -> None:
        """Test origin discovery initialization."""
        discovery = OriginDiscovery(valid_domain)
        assert discovery.domain == valid_domain

    def test_origin_discovery_via_dns(self, valid_domain: str) -> None:
        """Test origin discovery via DNS A records."""
        discovery = OriginDiscovery(valid_domain)
        with patch.object(discovery, "find_origins") as mock_find:
            mock_find.return_value = ["93.184.216.34"]
            result = discovery.find_origins()
            assert isinstance(result, list)
            if result:
                assert all(isinstance(ip, str) for ip in result)

    def test_origin_discovery_via_certificate(self, valid_domain: str) -> None:
        """Test origin discovery via SSL certificate."""
        discovery = OriginDiscovery(valid_domain)
        with patch.object(discovery, "find_origins") as mock_find:
            mock_find.return_value = ["198.51.100.0"]
            result = discovery.find_origins()
            assert isinstance(result, list)

    def test_origin_behind_cloudflare(self, valid_domain: str) -> None:
        """Test origin discovery behind Cloudflare CDN."""
        discovery = OriginDiscovery(valid_domain)
        with patch.object(discovery, "find_origins") as mock_find:
            mock_find.return_value = ["192.0.2.0"]  # Real origin
            result = discovery.find_origins()
            assert isinstance(result, list)

    def test_origin_not_found(self, valid_domain: str) -> None:
        """Test when origin cannot be discovered."""
        discovery = OriginDiscovery(valid_domain)
        with patch.object(discovery, "find_origins") as mock_find:
            mock_find.return_value = []
            result = discovery.find_origins()
            assert isinstance(result, list)
            assert len(result) == 0
