"""クライアント設定値の定義モジュール。

キャッシュ設定、リトライ設定、クライアント共通設定など、
API クライアントの動作に関わる定数とデータクラスを定義する。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

DEFAULT_BASE_URL = "https://api.info.gbiz.go.jp/hojin"
MAX_PAGE = 10
MAX_LIMIT = 5000
MAX_TOTAL_RECORDS = MAX_PAGE * MAX_LIMIT  # 50,000


class CacheMode(StrEnum):
    """キャッシュモードの列挙型。

    Attributes:
        OFF: キャッシュ無効。
        READ: 読み取りのみ（既存キャッシュを利用するが書き込まない）。
        READ_WRITE: 読み書き両対応（通常のキャッシュ動作）。
        FORCE_REFRESH: キャッシュを無視してリクエストし、結果を書き込む。
    """

    OFF = "off"
    READ = "read"
    READ_WRITE = "read_write"
    FORCE_REFRESH = "force_refresh"


@dataclass(slots=True)
class RetryConfig:
    """リトライ（再試行）設定。

    Attributes:
        max_attempts: 最大リトライ回数。
        base_delay: バックオフの基本待機秒数。
        cap_delay: バックオフの上限待機秒数。
    """

    max_attempts: int = 5
    base_delay: float = 0.5
    cap_delay: float = 8.0


@dataclass(slots=True)
class CacheConfig:
    """キャッシュ設定。

    Attributes:
        mode: キャッシュモード。
        dir: キャッシュファイルの保存ディレクトリ。None でキャッシュ無効。
        ttl_seconds: キャッシュの有効期間（秒）。デフォルトは24時間。
    """

    mode: CacheMode = CacheMode.OFF
    dir: Path | None = None
    ttl_seconds: int = 24 * 60 * 60


@dataclass(slots=True)
class ClientConfig:
    """クライアント共通設定。

    Attributes:
        base_url: API のベース URL。
        timeout: HTTP タイムアウト秒数。
        user_agent: User-Agent ヘッダ値。
        rate_limit_per_sec: 1秒あたりの最大リクエスト数。
        cache: キャッシュ設定。
    """

    base_url: str = DEFAULT_BASE_URL
    timeout: float = 30.0
    user_agent: str = ""
    rate_limit_per_sec: float = 1.0
    cache: CacheConfig = field(default_factory=CacheConfig)
