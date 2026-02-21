"""キャッシュテスト。"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

import pytest

from gbizinfo.cache import FileCache
from gbizinfo.config import CacheMode

if TYPE_CHECKING:
    from pathlib import Path


class TestFileCache:
    def test_hit_miss(self, tmp_path: Path):
        cache = FileCache(cache_dir=tmp_path, ttl_seconds=3600)
        key = "test-key"

        # miss
        assert cache.get(key=key, mode=CacheMode.READ_WRITE) is None

        # put
        cache.put(key=key, payload={"data": "hello"})

        # hit
        hit = cache.get(key=key, mode=CacheMode.READ_WRITE)
        assert hit is not None
        assert hit.payload["data"] == "hello"
        assert hit.stale is False

    def test_ttl_expiry(self, tmp_path: Path):
        cache = FileCache(cache_dir=tmp_path, ttl_seconds=0)
        key = "expire-key"
        cache.put(key=key, payload={"data": "old"})
        time.sleep(0.01)
        hit = cache.get(key=key, mode=CacheMode.READ_WRITE)
        assert hit is not None
        assert hit.stale is True

    def test_off_mode(self, tmp_path: Path):
        cache = FileCache(cache_dir=tmp_path, ttl_seconds=3600)
        key = "off-key"
        cache.put(key=key, payload={"data": "value"})
        assert cache.get(key=key, mode=CacheMode.OFF) is None

    def test_corrupt_file_quarantine(self, tmp_path: Path):
        cache = FileCache(cache_dir=tmp_path, ttl_seconds=3600)
        key = "corrupt-key"

        # Write a corrupt file
        import hashlib
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        corrupt_path = tmp_path / f"{digest}.json"
        corrupt_path.write_text("NOT JSON{{{", encoding="utf-8")

        # Get should return None and quarantine
        assert cache.get(key=key, mode=CacheMode.READ_WRITE) is None
        assert (tmp_path / ".broken" / corrupt_path.name).exists()

    def test_no_cache_dir(self):
        cache = FileCache(cache_dir=None, ttl_seconds=3600)
        assert cache.get(key="any", mode=CacheMode.READ_WRITE) is None
        cache.put(key="any", payload={"data": "ignored"})  # no-op


class TestMakeKey:
    def test_token_not_in_key(self):
        """キーに token が含まれないこと。"""
        key1 = FileCache.make_key(method="GET", path="/v2/hojin", params={"name": "test"})
        key2 = FileCache.make_key(method="GET", path="/v2/hojin", params={"name": "test"})
        assert key1 == key2

    def test_different_params_different_keys(self):
        key1 = FileCache.make_key(method="GET", path="/v2/hojin", params={"name": "a"})
        key2 = FileCache.make_key(method="GET", path="/v2/hojin", params={"name": "b"})
        assert key1 != key2

    def test_metadata_changes_key(self):
        key1 = FileCache.make_key(method="GET", path="/v2/hojin", params={})
        key2 = FileCache.make_key(method="GET", path="/v2/hojin", params={"metadata_flg": "true"})
        assert key1 != key2


@pytest.mark.anyio()
class TestAsyncCache:
    async def test_async_hit_miss(self, tmp_path: Path):
        cache = FileCache(cache_dir=tmp_path, ttl_seconds=3600)
        key = "async-test"

        assert await cache.aget(key=key, mode=CacheMode.READ_WRITE) is None

        await cache.aput(key=key, payload={"async": True})

        hit = await cache.aget(key=key, mode=CacheMode.READ_WRITE)
        assert hit is not None
        assert hit.payload["async"] is True
