"""Unit tests for rankle.utils.confidence module."""

import pytest

from rankle.utils.confidence import calculate_confidence_score


class TestConfidenceCalculation:
    """Test confidence score calculation."""

    def test_confidence_single_evidence(self) -> None:
        """Test confidence with single evidence."""
        evidence = [{"type": "header", "value": "WordPress"}]
        score = calculate_confidence_score(evidence)
        assert 0 <= score <= 1

    def test_confidence_multiple_evidence(self) -> None:
        """Test confidence with multiple evidence."""
        evidence = [
            {"type": "header", "value": "X-Powered-By: WordPress"},
            {"type": "meta", "value": "generator: WordPress"},
            {"type": "directory", "value": "/wp-content/"},
        ]
        score = calculate_confidence_score(evidence)
        assert 0 <= score <= 1
        # Multiple evidence should increase confidence
        assert score > 0.5

    def test_confidence_diminishing_factor(self) -> None:
        """Test diminishing factor application."""
        evidence = [{"type": "header", "value": "x"}]
        score1 = calculate_confidence_score(evidence, diminishing_factor=0.5)
        score2 = calculate_confidence_score(evidence, diminishing_factor=0.8)
        # Lower diminishing factor should result in lower score
        assert score1 < score2

    def test_confidence_minimum_threshold(self) -> None:
        """Test minimum confidence threshold."""
        evidence = [{"type": "weak", "value": "vague"}]
        score = calculate_confidence_score(evidence)
        # Even weak evidence should be 0-100%
        assert 0 <= score <= 1

    def test_confidence_maximum_is_one(self) -> None:
        """Test maximum confidence is 1.0."""
        evidence = [
            {"type": "header", "value": "x"},
            {"type": "meta", "value": "x"},
            {"type": "directory", "value": "x"},
            {"type": "cookie", "value": "x"},
        ]
        score = calculate_confidence_score(evidence)
        assert score <= 1.0

    def test_confidence_empty_evidence(self) -> None:
        """Test confidence with no evidence."""
        score = calculate_confidence_score([])
        assert score == 0.0
