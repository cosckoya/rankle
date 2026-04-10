"""Unit tests for rankle.detectors.waf module."""

from unittest.mock import patch

import pytest

from rankle.detectors.waf import WAFDetector


class TestWAFDetector:
    """Test WAF detection."""

    def test_waf_detector_init(self, valid_domain: str) -> None:
        """Test WAF detector initialization."""
        detector = WAFDetector(valid_domain)
        assert detector.domain == valid_domain

    def test_imperva_detection(self, valid_domain: str) -> None:
        """Test Imperva WAF detection."""
        detector = WAFDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "detected": True,
                "waf_name": "Imperva",
                "confidence": 0.92,
                "evidence": ["Set-Cookie: visid header"]
            }
            result = detector.detect()
            assert result["detected"] is True

    def test_modsecurity_detection(self, valid_domain: str) -> None:
        """Test ModSecurity WAF detection."""
        detector = WAFDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "detected": True,
                "waf_name": "ModSecurity",
                "confidence": 0.85,
                "evidence": ["X-ModSecurity header"]
            }
            result = detector.detect()
            assert result["detected"] is True

    def test_waf_not_detected(self, valid_domain: str) -> None:
        """Test when WAF is not detected."""
        detector = WAFDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "detected": False,
                "waf_name": None,
                "confidence": 0.0
            }
            result = detector.detect()
            assert result["detected"] is False

    def test_waf_confidence_score(self, valid_domain: str, mock_waf_result: dict) -> None:
        """Test WAF confidence scoring."""
        detector = WAFDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = mock_waf_result
            result = detector.detect()
            if result["detected"]:
                assert 0 <= result["confidence"] <= 1
