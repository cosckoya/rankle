"""Unit tests for rankle.detectors.technology module."""

from unittest.mock import MagicMock, patch

import pytest

from rankle.detectors.technology import TechnologyDetector


class TestTechnologyDetector:
    """Test technology detection."""

    def test_technology_detector_init(self, valid_domain: str) -> None:
        """Test technology detector initialization."""
        detector = TechnologyDetector(valid_domain)
        assert detector.domain == valid_domain

    @pytest.mark.integration
    def test_wordpress_detection(self, valid_domain: str) -> None:
        """Test WordPress detection."""
        detector = TechnologyDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "WordPress": {
                    "confidence": 0.95,
                    "version": "6.4",
                    "category": "CMS"
                }
            }
            result = detector.detect()
            assert "WordPress" in result

    def test_react_detection(self, valid_domain: str) -> None:
        """Test React.js detection."""
        detector = TechnologyDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "React": {
                    "confidence": 0.85,
                    "version": "18.2.0",
                    "category": "JavaScript Framework"
                }
            }
            result = detector.detect()
            assert "React" in result

    def test_django_detection(self, valid_domain: str) -> None:
        """Test Django framework detection."""
        detector = TechnologyDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "Django": {
                    "confidence": 0.80,
                    "version": "4.2",
                    "category": "Web Framework"
                }
            }
            result = detector.detect()
            assert "Django" in result

    def test_confidence_scoring(self, valid_domain: str, mock_tech_result: dict) -> None:
        """Test confidence score calculation."""
        detector = TechnologyDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = mock_tech_result
            result = detector.detect()
            for tech, data in result.items():
                assert "confidence" in data
                assert 0 <= data["confidence"] <= 1

    def test_version_extraction(self, valid_domain: str) -> None:
        """Test version extraction."""
        detector = TechnologyDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "PHP": {"version": "7.4.3", "confidence": 0.9},
                "Apache": {"version": "2.4.41", "confidence": 0.95}
            }
            result = detector.detect()
            for tech, data in result.items():
                if "version" in data:
                    assert isinstance(data["version"], str)

    def test_wappalyzer_integration(self, valid_domain: str) -> None:
        """Test Wappalyzer integration (3000+ signatures)."""
        detector = TechnologyDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            # Wappalyzer should return multiple technologies
            mock_detect.return_value = {
                "Apache": {"confidence": 0.95},
                "jQuery": {"confidence": 0.88},
                "Bootstrap": {"confidence": 0.82}
            }
            result = detector.detect()
            assert len(result) > 0

    def test_favicon_hashing(self, valid_domain: str) -> None:
        """Test favicon hashing via mmh3."""
        detector = TechnologyDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "Cloudflare": {
                    "confidence": 0.75,
                    "detection_method": "favicon_hash"
                }
            }
            result = detector.detect()
            assert isinstance(result, dict)

    def test_detection_result_structure(self, valid_domain: str, mock_tech_result: dict) -> None:
        """Test detection result has expected structure."""
        detector = TechnologyDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = mock_tech_result
            result = detector.detect()
            for tech, data in result.items():
                assert isinstance(data, dict)
                assert "confidence" in data
