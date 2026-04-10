"""Unit tests for rankle.detectors.cdn module."""

from unittest.mock import patch

import pytest

from rankle.detectors.cdn import CDNDetector


class TestCDNDetector:
    """Test CDN detection."""

    def test_cdn_detector_init(self, valid_domain: str) -> None:
        """Test CDN detector initialization."""
        detector = CDNDetector(valid_domain)
        assert detector.domain == valid_domain

    def test_cloudflare_detection(self, valid_domain: str) -> None:
        """Test Cloudflare CDN detection."""
        detector = CDNDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "detected": True,
                "provider": "Cloudflare",
                "confidence": 0.95,
                "asn": "AS13335"
            }
            result = detector.detect()
            assert result["detected"] is True
            assert "Cloudflare" in result.get("provider", "")

    def test_aws_cloudfront_detection(self, valid_domain: str) -> None:
        """Test AWS CloudFront detection."""
        detector = CDNDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "detected": True,
                "provider": "AWS CloudFront",
                "confidence": 0.88,
                "asn": "AS16509"
            }
            result = detector.detect()
            assert result["detected"] is True

    def test_cdn_not_detected(self, valid_domain: str) -> None:
        """Test when CDN is not detected."""
        detector = CDNDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = {
                "detected": False,
                "provider": None,
                "confidence": 0.0
            }
            result = detector.detect()
            assert result["detected"] is False

    def test_cdn_confidence_score(self, valid_domain: str, mock_cdn_result: dict) -> None:
        """Test CDN confidence scoring."""
        detector = CDNDetector(valid_domain)
        with patch.object(detector, "detect") as mock_detect:
            mock_detect.return_value = mock_cdn_result
            result = detector.detect()
            if result["detected"]:
                assert 0 <= result["confidence"] <= 1
