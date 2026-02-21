"""例外テスト。"""

from __future__ import annotations

import httpx
import pytest

from gbizinfo.errors import (
    GbizBadRequestError,
    GbizHttpStatusError,
    GbizNotFoundError,
    GbizRateLimitError,
    GbizServerError,
    GbizUnauthorizedError,
)

BASE_URL = "https://api.info.gbiz.go.jp/hojin"


class TestErrorDispatching:
    def test_400_with_errors_json(self, mock_api, client):
        """400 + JSON errors → GbizBadRequestError。"""
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(
                400,
                json={
                    "errors": [{"item": "name", "message": "必須です"}],
                    "id": "err-001",
                },
            )
        )
        with pytest.raises(GbizBadRequestError) as exc_info:
            client.search(name="test")
        assert exc_info.value.context.status_code == 400
        assert len(exc_info.value.errors) == 1
        assert exc_info.value.context.response_id == "err-001"

    def test_401_unauthorized(self, mock_api, client):
        """401 → GbizUnauthorizedError。"""
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(401, text="Unauthorized")
        )
        with pytest.raises(GbizUnauthorizedError) as exc_info:
            client.search(name="test")
        assert exc_info.value.context.status_code == 401

    def test_404_not_found(self, mock_api, client):
        """404 → GbizNotFoundError。"""
        mock_api.get("/v2/hojin/7000012050002").mock(
            return_value=httpx.Response(404, text="Not Found")
        )
        with pytest.raises(GbizNotFoundError):
            client.get("7000012050002")

    def test_429_rate_limit(self, mock_api, client):
        """429 → リトライ後 GbizRateLimitError（max_attempts=1 の場合即エラー）。"""
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(429, headers={"Retry-After": "1"}, text="Too Many Requests")
        )
        # Override with 1 retry to avoid long waits
        client._retry.max_attempts = 1
        with pytest.raises(GbizRateLimitError) as exc_info:
            client.search(name="test")
        assert exc_info.value.context.retry_after == 1.0

    def test_500_server_error(self, mock_api, client):
        """500 → リトライ後 GbizServerError。"""
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )
        client._retry.max_attempts = 1
        with pytest.raises(GbizServerError):
            client.search(name="test")

    def test_non_json_error_body(self, mock_api, client):
        """HTML レスポンスでも body_snippet が保持される。"""
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(403, text="<html>Forbidden</html>")
        )
        with pytest.raises(GbizHttpStatusError) as exc_info:
            client.search(name="test")
        assert "<html>" in (exc_info.value.context.body_snippet or "")
