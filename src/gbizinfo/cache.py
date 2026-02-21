"""ファイルベースキャッシュモジュール。

HTTP レスポンスを JSON ファイルとしてディスクにキャッシュする機能を提供する。
同期・非同期の両方の読み書きに対応し、atomic write により整合性を保証する。
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any

import anyio

from gbizinfo._logging import logger
from gbizinfo.config import CacheMode


@dataclass(slots=True)
class CacheHit:
    """キャッシュ読み取り結果を表すデータクラス。

    Attributes:
        payload: キャッシュされたレスポンスデータ。
        stale: TTL を超過している場合に True。
    """

    payload: dict[str, Any]
    stale: bool


class FileCache:
    """JSON ファイルベースキャッシュ（HTTP レスポンス単位）。

    キーを SHA-256 ハッシュでファイル名に変換し、JSON 形式で
    レスポンスデータを保存する。TTL による有効期限管理を行う。

    Args:
        cache_dir: キャッシュファイルの保存ディレクトリ。None の場合はキャッシュ無効。
        ttl_seconds: キャッシュの有効期間（秒）。
    """

    def __init__(self, *, cache_dir: Path | None, ttl_seconds: int) -> None:
        self._cache_dir = cache_dir
        self._ttl_seconds = ttl_seconds
        self._lock = Lock()
        if self._cache_dir is not None:
            self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _path_for_key(self, key: str) -> Path:
        """キー文字列からキャッシュファイルのパスを生成する。

        Args:
            key: キャッシュキー文字列。

        Returns:
            キャッシュファイルの Path オブジェクト。
        """
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        assert self._cache_dir is not None
        return self._cache_dir / f"{digest}.json"

    def get(self, *, key: str, mode: CacheMode) -> CacheHit | None:
        """キャッシュを同期的に読み取る。

        キャッシュが無効、存在しない、または破損している場合は None を返す。
        TTL 超過時は stale=True の CacheHit を返す。

        Args:
            key: キャッシュキー文字列。
            mode: キャッシュモード。

        Returns:
            キャッシュヒット結果。ミスの場合は None。
        """
        if self._cache_dir is None or mode in (CacheMode.OFF, CacheMode.FORCE_REFRESH):
            return None

        path = self._path_for_key(key)
        if not path.exists():
            logger.debug("Cache miss: %s", key[:80])
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self._quarantine(path)
            return None

        created_at = float(data.get("created_at", 0.0))
        stale = (time.time() - created_at) > self._ttl_seconds
        logger.debug("Cache hit (stale=%s): %s", stale, key[:80])
        return CacheHit(payload=data.get("payload", {}), stale=stale)

    async def aget(self, *, key: str, mode: CacheMode) -> CacheHit | None:
        """キャッシュを非同期的に読み取る。

        Args:
            key: キャッシュキー文字列。
            mode: キャッシュモード。

        Returns:
            キャッシュヒット結果。ミスの場合は None。
        """
        if self._cache_dir is None or mode in (CacheMode.OFF, CacheMode.FORCE_REFRESH):
            return None

        apath = anyio.Path(self._path_for_key(key))
        if not await apath.exists():
            logger.debug("Cache miss: %s", key[:80])
            return None
        try:
            text = await apath.read_text(encoding="utf-8")
            data = json.loads(text)
        except (OSError, json.JSONDecodeError):
            self._quarantine(self._path_for_key(key))
            return None

        created_at = float(data.get("created_at", 0.0))
        stale = (time.time() - created_at) > self._ttl_seconds
        logger.debug("Cache hit (stale=%s): %s", stale, key[:80])
        return CacheHit(payload=data.get("payload", {}), stale=stale)

    def put(self, *, key: str, payload: dict[str, Any]) -> None:
        """キャッシュを同期的に書き込む。

        tempfile による atomic write でファイルを作成・置換する。

        Args:
            key: キャッシュキー文字列。
            payload: キャッシュするレスポンスデータ。
        """
        if self._cache_dir is None:
            return
        path = self._path_for_key(key)
        body = {
            "created_at": time.time(),
            "payload": payload,
        }
        data = json.dumps(body, ensure_ascii=False, separators=(",", ":"))

        with self._lock:
            fd, tmp_path = tempfile.mkstemp(
                prefix=path.name,
                suffix=".tmp",
                dir=str(self._cache_dir),
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(data)
                Path(tmp_path).replace(path)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

    async def aput(self, *, key: str, payload: dict[str, Any]) -> None:
        """キャッシュを非同期的に書き込む。

        一意テンポラリファイルを作成し、rename による原子的置換で保存する。

        Args:
            key: キャッシュキー文字列。
            payload: キャッシュするレスポンスデータ。
        """
        if self._cache_dir is None:
            return
        path = self._path_for_key(key)
        body = {
            "created_at": time.time(),
            "payload": payload,
        }
        data = json.dumps(body, ensure_ascii=False, separators=(",", ":"))

        fd, tmp_path_str = tempfile.mkstemp(
            prefix=path.name,
            suffix=".tmp",
            dir=str(self._cache_dir),
        )
        tmp_path = Path(tmp_path_str)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(data)
            await anyio.Path(tmp_path).rename(path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)

    def _quarantine(self, path: Path) -> None:
        """破損したキャッシュファイルを隔離する。

        ``.broken/`` ディレクトリに移動し、100件を超過した場合は
        古い順に削除する。

        Args:
            path: 破損したキャッシュファイルのパス。
        """
        assert self._cache_dir is not None
        broken_dir = self._cache_dir / ".broken"
        try:
            broken_dir.mkdir(exist_ok=True)
            dest = broken_dir / path.name
            path.replace(dest)
            logger.warning("Quarantined corrupt cache file: %s", path)

            # 100件上限
            broken_files = sorted(broken_dir.iterdir(), key=lambda p: p.stat().st_mtime)
            while len(broken_files) > 100:
                oldest = broken_files.pop(0)
                oldest.unlink(missing_ok=True)
        except OSError:
            pass

    @staticmethod
    def make_key(*, method: str, path: str, params: dict[str, str]) -> str:
        """キャッシュキー文字列を生成する。

        HTTP メソッド、パス、クエリパラメータからキーを構築する。
        API トークンはキーに含めない。

        Args:
            method: HTTP メソッド（GET 等）。
            path: リクエストパス。
            params: クエリパラメータの辞書。

        Returns:
            SHA-256 ハッシュによるキー文字列。
        """
        sorted_params = sorted(params.items())
        raw = f"{method}:{path}:{sorted_params}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
