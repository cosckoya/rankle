"""Unit tests for rankle.utils.favicon_hash module."""

import pytest

from rankle.utils.favicon_hash import (
    analyze_favicon,
    calculate_favicon_hash,
    get_technology_from_favicon_hash,
)


class TestFaviconHashing:
    """Test favicon hashing and fingerprinting."""

    def test_calculate_favicon_hash(self) -> None:
        """Test favicon hash calculation with mmh3."""
        favicon_data = b"\x89PNG\r\n\x1a\n"  # PNG header
        hash_value = calculate_favicon_hash(favicon_data)
        assert isinstance(hash_value, (int, str))

    def test_favicon_hash_consistency(self) -> None:
        """Test favicon hash is consistent."""
        favicon = b"favicon_data"
        hash1 = calculate_favicon_hash(favicon)
        hash2 = calculate_favicon_hash(favicon)
        # Same favicon should have same hash
        assert hash1 == hash2

    def test_favicon_hash_different_favicons(self) -> None:
        """Test different favicons have different hashes."""
        favicon1 = b"favicon1"
        favicon2 = b"favicon2"
        hash1 = calculate_favicon_hash(favicon1)
        hash2 = calculate_favicon_hash(favicon2)
        # Different favicons should have different hashes
        assert hash1 != hash2

    def test_get_technology_from_hash(self) -> None:
        """Test technology lookup from favicon hash."""
        # Use a known favicon hash if available
        result = get_technology_from_favicon_hash("-1234567890")
        assert isinstance(result, (dict, type(None)))

    def test_analyze_favicon(self) -> None:
        """Test full favicon analysis."""
        favicon_data = b"\x89PNG\r\n\x1a\n"
        result = analyze_favicon(favicon_data)
        assert isinstance(result, dict)
