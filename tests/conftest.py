"""共通フィクスチャ。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import respx

from gbizinfo import AsyncGbizClient, GbizClient

FIXTURES_DIR = Path(__file__).parent / "fixtures"

BASE_URL = "https://api.info.gbiz.go.jp/hojin"


@pytest.fixture
def anyio_backend():
    return "asyncio"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


@pytest.fixture()
def mock_api():
    """respx で gBizINFO API をモック。"""
    with respx.mock(base_url=BASE_URL) as respx_mock:
        yield respx_mock


@pytest.fixture()
def client(mock_api):
    """テスト用同期クライアント。"""
    with GbizClient(api_token="test-token") as c:
        yield c


@pytest.fixture()
async def async_client(mock_api):
    """テスト用非同期クライアント。"""
    async with AsyncGbizClient(api_token="test-token") as c:
        yield c
