"""HTTP 実行補助モジュール。

レート制限、リトライ判定、User-Agent 構築など、
HTTP リクエストに必要な共通ユーティリティを提供する。
"""

from __future__ import annotations

import random
import sys
import threading
import time
from email.utils import parsedate_to_datetime
from typing import TYPE_CHECKING

import anyio
import httpx

if TYPE_CHECKING:
    from types import TracebackType


class SyncRateLimiter:
    """同期用最小間隔レート制御。

    threading.Lock で排他制御を行い、指定された秒間リクエスト数を
    超えないように送信間隔を制御する。

    Args:
        rate_limit_per_sec: 1秒あたりの最大リクエスト数。
    """

    def __init__(self, rate_limit_per_sec: float) -> None:
        self._min_interval = 1.0 / rate_limit_per_sec if rate_limit_per_sec > 0 else 0.0
        self._lock = threading.Lock()
        self._next_allowed = 0.0

    def acquire(self) -> float:
        """送信許可まで待機する。

        Returns:
            実際に待機した秒数。
        """
        if self._min_interval <= 0:
            return 0.0
        with self._lock:
            now = time.monotonic()
            wait = max(0.0, self._next_allowed - now)
            if wait > 0:
                time.sleep(wait)
                now = time.monotonic()
            self._next_allowed = now + self._min_interval
            return wait


class AsyncRateLimiter:
    """非同期用最小間隔レート制御。

    anyio.Lock で排他制御を行い、指定された秒間リクエスト数を
    超えないように送信間隔を制御する。

    Args:
        rate_limit_per_sec: 1秒あたりの最大リクエスト数。
    """

    def __init__(self, rate_limit_per_sec: float) -> None:
        self._min_interval = 1.0 / rate_limit_per_sec if rate_limit_per_sec > 0 else 0.0
        self._lock = anyio.Lock()
        self._next_allowed = 0.0

    async def acquire(self) -> float:
        """送信許可まで非同期で待機する。

        Returns:
            実際に待機した秒数。
        """
        if self._min_interval <= 0:
            return 0.0
        async with self._lock:
            now = anyio.current_time()
            wait = max(0.0, self._next_allowed - now)
            if wait > 0:
                await anyio.sleep(wait)
                now = anyio.current_time()
            self._next_allowed = now + self._min_interval
            return wait


class AsyncConcurrencyLimiter:
    """非同期リクエストの同時実行数を制御するリミッター。

    async with 文で使用し、同時実行中のリクエスト数が上限を超えない
    ように制御する。

    Args:
        max_concurrent: 同時実行の最大数。
    """

    def __init__(self, max_concurrent: int = 10) -> None:
        self._limiter = anyio.CapacityLimiter(max_concurrent)

    async def __aenter__(self) -> AsyncConcurrencyLimiter:
        await self._limiter.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._limiter.__aexit__(exc_type, exc_val, exc_tb)


def should_retry_http_status(status_code: int) -> bool:
    """HTTP ステータスコードがリトライ対象か判定する。

    429（レート制限）および 5xx 系（500, 502, 503, 504）を
    リトライ対象とする。

    Args:
        status_code: HTTP ステータスコード。

    Returns:
        リトライ対象であれば True。
    """
    return status_code in {429, 500, 502, 503, 504}


def should_retry_transport_error(exc: Exception) -> bool:
    """トランスポートエラーがリトライ対象か判定する。

    TimeoutException, ConnectError, ReadError, RemoteProtocolError を
    リトライ対象とする。

    Args:
        exc: 発生した例外。

    Returns:
        リトライ対象であれば True。
    """
    retryable = (
        httpx.TimeoutException,
        httpx.ConnectError,
        httpx.ReadError,
        httpx.RemoteProtocolError,
    )
    return isinstance(exc, retryable)


def parse_retry_after(response: httpx.Response) -> float | None:
    """Retry-After ヘッダをパースして待機秒数を返す。

    秒数形式（整数）および HTTP-date 形式の両方に対応する。

    Args:
        response: HTTP レスポンスオブジェクト。

    Returns:
        待機すべき秒数。ヘッダが存在しない場合やパース失敗時は None。
    """
    value = response.headers.get("Retry-After")
    if not value:
        return None
    text = value.strip()
    if text.isdigit():
        return float(text)
    try:
        dt = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None
    wait: float = max(0.0, dt.timestamp() - time.time())
    return wait


def compute_wait_time(
    *,
    attempt: int,
    base: float,
    cap: float,
    retry_after: float | None,
) -> float:
    """リトライ待機秒を計算する。

    Retry-After が指定されている場合はそちらを優先し、
    それ以外は full jitter バックオフで計算する。

    Args:
        attempt: 現在のリトライ回数（0始まり）。
        base: バックオフの基本秒数。
        cap: バックオフの上限秒数。
        retry_after: Retry-After ヘッダから取得した待機秒数。

    Returns:
        リトライまでの待機秒数。
    """
    if retry_after is not None:
        return retry_after
    return full_jitter_backoff(attempt=attempt, base=base, cap=cap)


def full_jitter_backoff(*, attempt: int, base: float, cap: float) -> float:
    """full jitter アルゴリズムによるバックオフ待機秒を計算する。

    ``min(cap, base * 2^attempt)`` を上限としたランダムな待機秒を返す。

    Args:
        attempt: 現在のリトライ回数（0始まり）。
        base: バックオフの基本秒数。
        cap: バックオフの上限秒数。

    Returns:
        ランダムに算出された待機秒数。
    """
    upper = min(cap, base * (2**attempt))
    return random.uniform(0.0, upper)  # noqa: S311


def build_user_agent(*, version: str) -> str:
    """User-Agent ヘッダ文字列を構築する。

    ``gbizinfo/{version} python/{major}.{minor}.{micro}`` の形式で返す。

    Args:
        version: ライブラリのバージョン文字列。

    Returns:
        User-Agent ヘッダ文字列。
    """
    v = sys.version_info
    return f"gbizinfo/{version} python/{v.major}.{v.minor}.{v.micro}"


def build_request_headers(*, user_agent: str, api_token: str) -> dict[str, str]:
    """API リクエスト用の標準ヘッダ辞書を構築する。

    X-hojinInfo-api-token, Accept, Accept-Encoding, User-Agent を含む。

    Args:
        user_agent: User-Agent ヘッダ値。
        api_token: gBizINFO API トークン。

    Returns:
        リクエストヘッダの辞書。
    """
    return {
        "X-hojinInfo-api-token": api_token,
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "User-Agent": user_agent,
    }
