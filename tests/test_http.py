"""HTTP ヘルパーテスト。"""

from __future__ import annotations

import time

import httpx
import pytest

from gbizinfo.http import (
    AsyncRateLimiter,
    SyncRateLimiter,
    build_request_headers,
    build_user_agent,
    compute_wait_time,
    full_jitter_backoff,
    parse_retry_after,
    should_retry_http_status,
    should_retry_transport_error,
)


class TestSyncRateLimiter:
    def test_acquire_enforces_interval(self):
        limiter = SyncRateLimiter(rate_limit_per_sec=10.0)  # 100ms interval
        limiter.acquire()
        start = time.monotonic()
        limiter.acquire()
        elapsed = time.monotonic() - start
        assert elapsed >= 0.05  # at least some wait

    def test_zero_rate_no_wait(self):
        limiter = SyncRateLimiter(rate_limit_per_sec=0.0)
        assert limiter.acquire() == 0.0


@pytest.mark.anyio()
class TestAsyncRateLimiter:
    async def test_acquire(self):
        limiter = AsyncRateLimiter(rate_limit_per_sec=10.0)
        await limiter.acquire()
        await limiter.acquire()  # should wait

    async def test_zero_rate_no_wait(self):
        limiter = AsyncRateLimiter(rate_limit_per_sec=0.0)
        assert await limiter.acquire() == 0.0


class TestShouldRetry:
    def test_retry_on_429(self):
        assert should_retry_http_status(429) is True

    def test_retry_on_500(self):
        assert should_retry_http_status(500) is True

    def test_retry_on_502(self):
        assert should_retry_http_status(502) is True

    def test_retry_on_503(self):
        assert should_retry_http_status(503) is True

    def test_retry_on_504(self):
        assert should_retry_http_status(504) is True

    def test_no_retry_on_400(self):
        assert should_retry_http_status(400) is False

    def test_no_retry_on_404(self):
        assert should_retry_http_status(404) is False

    def test_transport_timeout(self):
        assert should_retry_transport_error(httpx.ReadTimeout("timeout")) is True

    def test_transport_connect(self):
        assert should_retry_transport_error(httpx.ConnectError("conn")) is True

    def test_transport_value_error(self):
        assert should_retry_transport_error(ValueError("nope")) is False


class TestParseRetryAfter:
    def test_numeric(self):
        response = httpx.Response(429, headers={"Retry-After": "5"})
        assert parse_retry_after(response) == 5.0

    def test_missing(self):
        response = httpx.Response(429)
        assert parse_retry_after(response) is None


class TestComputeWaitTime:
    def test_retry_after_takes_priority(self):
        wait = compute_wait_time(attempt=0, base=0.5, cap=8.0, retry_after=10.0)
        assert wait == 10.0

    def test_backoff_when_no_retry_after(self):
        wait = compute_wait_time(attempt=0, base=0.5, cap=8.0, retry_after=None)
        assert 0 <= wait <= 0.5


class TestFullJitterBackoff:
    def test_bounded(self):
        for _ in range(100):
            val = full_jitter_backoff(attempt=3, base=0.5, cap=8.0)
            assert 0 <= val <= 4.0  # min(8.0, 0.5 * 2^3) = 4.0


class TestBuildUserAgent:
    def test_format(self):
        ua = build_user_agent(version="0.1.0")
        assert ua.startswith("gbizinfo/0.1.0 python/")


class TestBuildRequestHeaders:
    def test_contains_token(self):
        headers = build_request_headers(user_agent="test/1.0", api_token="my-token")
        assert headers["X-hojinInfo-api-token"] == "my-token"
        assert headers["Accept"] == "application/json"
        assert headers["User-Agent"] == "test/1.0"
