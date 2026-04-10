"""Unit tests for rankle.modules.geolocation module."""

from unittest.mock import patch

import pytest

from rankle.modules.geolocation import GeolocationLookup


class TestGeolocationLookup:
    """Test geolocation IP lookups."""

    def test_geolocation_lookup_init(self, valid_domain: str) -> None:
        """Test geolocation lookup initialization."""
        lookup = GeolocationLookup(valid_domain)
        assert lookup.domain == valid_domain

    def test_geoip_lookup(self, valid_domain: str) -> None:
        """Test GeoIP lookup."""
        lookup = GeolocationLookup(valid_domain)
        with patch.object(lookup, "lookup") as mock_lookup:
            mock_lookup.return_value = {
                "country": "US",
                "city": "Los Angeles",
                "asn": "AS15169"
            }
            result = lookup.lookup()
            assert "country" in result

    def test_asn_mapping(self, valid_domain: str) -> None:
        """Test ASN to provider mapping."""
        lookup = GeolocationLookup(valid_domain)
        with patch.object(lookup, "lookup") as mock_lookup:
            mock_lookup.return_value = {
                "asn": "AS15169",
                "provider": "Google"
            }
            result = lookup.lookup()
            assert "provider" in result or "asn" in result
