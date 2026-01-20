"""
Confidence score calculation utilities for Rankle.

Provides reusable confidence scoring algorithms used across
detection modules (technology, CDN, WAF, etc.).
"""

from typing import Any


def calculate_confidence_score(
    evidence: list[dict[str, Any]],
    diminishing_factor: float = 0.5,
) -> float:
    """
    Calculate confidence score from weighted evidence.

    Uses weighted scoring with diminishing returns for multiple
    pieces of the same type of evidence. This prevents over-confidence
    from redundant signals while still rewarding diverse evidence.

    Algorithm:
    1. Group evidence by type
    2. For each type, take best weight + diminishing bonus for additional evidence
    3. Sum all type scores and cap at 1.0

    Args:
        evidence: List of evidence dictionaries with 'type' and 'weight' keys
        diminishing_factor: Factor for diminishing returns (default: 0.5)
                           Each additional piece of same type multiplies by this

    Returns:
        Confidence score between 0.0 and 1.0

    Example:
        >>> evidence = [
        ...     {"type": "header", "detail": "X-Powered-By: Django", "weight": 0.5},
        ...     {"type": "cookie", "detail": "sessionid", "weight": 0.4},
        ...     {"type": "header", "detail": "X-Frame-Options", "weight": 0.3},
        ... ]
        >>> score = calculate_confidence_score(evidence)
        >>> print(f"{score:.2f}")
        0.95

        >>> # Single strong evidence
        >>> evidence = [{"type": "header", "detail": "Server: nginx", "weight": 0.8}]
        >>> calculate_confidence_score(evidence)
        0.8

        >>> # Multiple weak evidence of same type (diminishing returns)
        >>> evidence = [
        ...     {"type": "pattern", "detail": "keyword1", "weight": 0.3},
        ...     {"type": "pattern", "detail": "keyword2", "weight": 0.3},
        ...     {"type": "pattern", "detail": "keyword3", "weight": 0.3},
        ... ]
        >>> score = calculate_confidence_score(evidence)
        >>> # 0.3 + 0.3*0.5 + 0.3*0.25 = 0.525
        >>> print(f"{score:.2f}")
        0.53
    """
    if not evidence:
        return 0.0

    # Group evidence by type
    by_type: dict[str, list[float]] = {}
    for ev in evidence:
        ev_type = ev["type"]
        if ev_type not in by_type:
            by_type[ev_type] = []
        by_type[ev_type].append(ev["weight"])

    # Calculate score with diminishing returns
    total_score = 0.0
    for weights in by_type.values():
        # Sort to prioritize strongest evidence
        weights.sort(reverse=True)

        # First piece of evidence gets full weight
        type_score = weights[0]

        # Additional pieces get diminishing returns
        for i, weight in enumerate(weights[1:], 1):
            type_score += weight * (diminishing_factor**i)

        total_score += type_score

    # Cap at 1.0 (100% confidence)
    return min(1.0, total_score)


def meets_confidence_threshold(
    evidence: list[dict[str, Any]],
    threshold: float,
    diminishing_factor: float = 0.5,
) -> bool:
    """
    Check if evidence meets minimum confidence threshold.

    Args:
        evidence: List of evidence dictionaries
        threshold: Minimum confidence score required (0.0 to 1.0)
        diminishing_factor: Factor for diminishing returns

    Returns:
        True if confidence score >= threshold

    Example:
        >>> evidence = [{"type": "header", "detail": "Server", "weight": 0.8}]
        >>> meets_confidence_threshold(evidence, threshold=0.5)
        True
        >>> meets_confidence_threshold(evidence, threshold=0.9)
        False
    """
    score = calculate_confidence_score(evidence, diminishing_factor)
    return score >= threshold


def group_evidence_by_type(
    evidence: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """
    Group evidence items by their type.

    Args:
        evidence: List of evidence dictionaries with 'type' key

    Returns:
        Dictionary mapping type -> list of evidence items

    Example:
        >>> evidence = [
        ...     {"type": "header", "detail": "Server: nginx", "weight": 0.5},
        ...     {"type": "cookie", "detail": "session", "weight": 0.4},
        ...     {"type": "header", "detail": "X-Powered-By", "weight": 0.3},
        ... ]
        >>> grouped = group_evidence_by_type(evidence)
        >>> len(grouped["header"])
        2
        >>> len(grouped["cookie"])
        1
    """
    grouped: dict[str, list[dict[str, Any]]] = {}
    for ev in evidence:
        ev_type = ev["type"]
        if ev_type not in grouped:
            grouped[ev_type] = []
        grouped[ev_type].append(ev)
    return grouped
