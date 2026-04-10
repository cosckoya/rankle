"""Unit tests for rankle.utils.cve_mapper module."""

import pytest

from rankle.utils.cve_mapper import (
    assess_technology_risk,
    generate_cpe,
    get_high_risk_technologies,
    map_technology_to_cve_urls,
)


class TestCVEMapping:
    """Test CVE version mapping."""

    def test_generate_cpe(self) -> None:
        """Test CPE generation."""
        cpe = generate_cpe("wordpress", "wordpress", "6.4")
        assert isinstance(cpe, str)
        assert "wordpress" in cpe.lower()

    def test_map_technology_to_cve_urls(self) -> None:
        """Test technology to CVE URL mapping."""
        urls = map_technology_to_cve_urls("WordPress", "5.0")
        assert isinstance(urls, (list, dict, type(None)))

    def test_high_risk_technologies(self) -> None:
        """Test get high risk technologies."""
        high_risk = get_high_risk_technologies()
        assert isinstance(high_risk, dict)

    def test_assess_technology_risk(self) -> None:
        """Test technology risk assessment."""
        risk = assess_technology_risk("WordPress", "5.0")
        assert isinstance(risk, (list, dict, type(None)))
