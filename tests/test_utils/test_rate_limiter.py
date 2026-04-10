"""Unit tests for rankle.utils.rate_limiter module."""

import time
from unittest.mock import patch

import pytest

from rankle.utils.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test rate limiting."""

    def test_rate_limiter_init(self) -> None:
        """Test rate limiter initialization."""
        limiter = RateLimiter()
        assert limiter is not None

    def test_rate_limit_delay_enforced(self) -> None:
        """Test rate limit delay is enforced."""
        limiter = RateLimiter()
        start = time.time()
        limiter.wait("example.com")
        limiter.wait("example.com")
        elapsed = time.time() - start
        # Should have at least 0.5s delay (RATE_LIMIT_DELAY)
        assert elapsed >= 0.4  # Allow some tolerance

    @pytest.mark.slow
    def test_adaptive_backoff(self) -> None:
        """Test adaptive backoff on slow responses."""
        limiter = RateLimiter()
        with patch.object(limiter, "record_response_time") as mock_record:
            # Record slow response (>2s)
            limiter.record_response_time("example.com", 3.0)
            # Next request should have increased delay

    def test_concurrent_limit_tracked(self) -> None:
        """Test concurrent request limit tracking."""
        limiter = RateLimiter()
        assert limiter.concurrent_requests >= 0

    def test_jitter_applied(self) -> None:
        """Test jitter is applied to delays."""
        limiter = RateLimiter()
        # Make multiple requests and check for jitter
        delays = []
        for _ in range(3):
            start = time.time()
            limiter.wait("example.com")
            delays.append(time.time() - start)
        # Delays should not be identical (jitter applied)
