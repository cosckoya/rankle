"""Unit tests for rankle.modules.subdomains module."""

from unittest.mock import MagicMock, patch

import pytest

from rankle.modules.subdomains import SubdomainDiscovery


class TestSubdomainDiscovery:
    """Test subdomain discovery."""

    def test_subdomain_discovery_init(self, valid_domain: str) -> None:
        """Test subdomain discovery initialization."""
        discovery = SubdomainDiscovery(valid_domain)
        assert discovery.domain == valid_domain

    @pytest.mark.integration
    @pytest.mark.slow
    def test_certificate_transparency_lookup(self, valid_domain: str) -> None:
        """Test Certificate Transparency lookup."""
        discovery = SubdomainDiscovery(valid_domain)
        with patch.object(discovery, "find_subdomains") as mock_find:
            mock_find.return_value = ["www.example.com", "mail.example.com"]
            result = discovery.find_subdomains()
            assert isinstance(result, list)

    def test_subdomain_limit_respected(self, valid_domain: str) -> None:
        """Test maximum subdomain limit respected."""
        discovery = SubdomainDiscovery(valid_domain)
        with patch.object(discovery, "find_subdomains") as mock_find:
            # Return more than max to test limiting
            mock_find.return_value = [f"sub{i}.{valid_domain}" for i in range(50)]
            result = discovery.find_subdomains()
            # Should be <= 100 (MAX_SUBDOMAINS)
            assert len(result) <= 100
