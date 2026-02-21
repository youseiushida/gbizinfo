"""クライアント統合テスト。"""

from __future__ import annotations

import inspect
from datetime import date

import httpx
import pytest

from gbizinfo import AsyncGbizClient, GbizClient
from gbizinfo.client import _PARAM_MAPPING, SearchParams, _build_query_params, _convert_param_value
from gbizinfo.enums import CorporateType, Prefecture
from gbizinfo.errors import GbizValidationError
from gbizinfo.models.responses import HojinInfo, HojinInfoSearch

BASE_URL = "https://api.info.gbiz.go.jp/hojin"


class TestParamMapping:
    """_PARAM_MAPPING テスト。"""

    def test_all_keys_present(self):
        """全パラメータが定義されている。"""
        expected_keys = {
            "corporate_number", "name", "exist_flg", "corporate_type", "prefecture",
            "city", "capital_stock_from", "capital_stock_to", "employee_number_from",
            "employee_number_to", "founded_year", "net_sales_from", "net_sales_to",
            "total_assets_from", "total_assets_to", "average_continuous_service_years",
            "average_age", "month_average_predetermined_overtime_hours",
            "female_workers_proportion", "patent", "procurement",
            "procurement_amount_from", "procurement_amount_to", "subsidy",
            "subsidy_amount_from", "subsidy_amount_to", "certification", "ministry",
            "source", "page", "limit", "metadata_flg",
        }
        assert set(_PARAM_MAPPING.keys()) == expected_keys

    def test_net_sales_mapping(self):
        """短縮名がAPIパラメータ名にマップされる。"""
        assert _PARAM_MAPPING["net_sales_from"] == "net_sales_summary_of_business_results_from"
        assert _PARAM_MAPPING["net_sales_to"] == "net_sales_summary_of_business_results_to"

    def test_total_assets_mapping(self):
        assert _PARAM_MAPPING["total_assets_from"] == "total_assets_summary_of_business_results_from"

    def test_search_params_match_search_args(self):
        """search() の引数名が _PARAM_MAPPING / SearchParams と一致する。"""
        sig = inspect.signature(GbizClient.search)
        search_params = {p for p in sig.parameters if p != "self"}
        assert search_params == set(_PARAM_MAPPING.keys())
        assert search_params == set(SearchParams.__annotations__.keys())

    def test_async_search_params_match(self):
        """AsyncGbizClient.search() も同じ引数を持つ。"""
        sync_sig = inspect.signature(GbizClient.search)
        async_sig = inspect.signature(AsyncGbizClient.search)
        sync_params = {p for p in sync_sig.parameters if p != "self"}
        async_params = {p for p in async_sig.parameters if p != "self"}
        assert sync_params == async_params


class TestParamConversion:
    """パラメータ変換テスト。"""

    def test_bool_conversion(self):
        assert _convert_param_value("exist_flg", True) == "true"
        assert _convert_param_value("exist_flg", False) == "false"

    def test_enum_conversion(self):
        assert _convert_param_value("prefecture", Prefecture.東京都) == "13"

    def test_int_conversion(self):
        assert _convert_param_value("capital_stock_from", 1000000) == "1000000"

    def test_sequence_enum_conversion(self):
        result = _convert_param_value(
            "corporate_type",
            [CorporateType.株式会社, CorporateType.合同会社]
        )
        assert result == "301,305"

    def test_build_query_params_skips_none(self):
        params = _build_query_params({"name": "test", "prefecture": None, "page": 1})
        assert "name" in params
        assert "prefecture" not in params


class TestTokenResolution:
    """api_token 解決テスト。"""

    def test_explicit_token(self, mock_api):
        client = GbizClient(api_token="explicit-token")
        assert client._api_token == "explicit-token"
        client.close()

    def test_env_fallback(self, mock_api, monkeypatch):
        monkeypatch.setenv("GBIZINFO_API_TOKEN", "env-token")
        client = GbizClient()
        assert client._api_token == "env-token"
        client.close()

    def test_no_token_raises(self, mock_api, monkeypatch):
        monkeypatch.delenv("GBIZINFO_API_TOKEN", raising=False)
        with pytest.raises(GbizValidationError, match="api_token"):
            GbizClient()


class TestSearch:
    """search() テスト。"""

    def test_basic_search(self, mock_api, client):
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(200, json={
                "hojin-infos": [
                    {"corporate_number": "1234567890123", "name": "テスト"},
                ],
                "id": "test",
                "message": "ok",
            })
        )
        result = client.search(name="テスト")
        assert len(result.items) == 1
        assert isinstance(result.items[0], HojinInfoSearch)

    def test_enum_params_converted(self, mock_api, client):
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(200, json={
                "hojin-infos": [],
                "id": "test",
                "message": "ok",
            })
        )
        client.search(prefecture=Prefecture.東京都, corporate_type=CorporateType.株式会社)
        request = mock_api.calls.last.request
        assert "prefecture=13" in str(request.url)
        assert "corporate_type=301" in str(request.url)


class TestGet:
    """get() テスト。"""

    def test_get_by_corporate_number(self, mock_api, client):
        mock_api.get("/v2/hojin/7000012050002").mock(
            return_value=httpx.Response(200, json={
                "hojin-infos": [
                    {"corporate_number": "7000012050002", "name": "国税庁"},
                ],
                "id": "test",
                "message": "ok",
            })
        )
        result = client.get("7000012050002")
        assert isinstance(result, HojinInfo)
        assert result.name == "国税庁"


class TestUpdateInfo:
    """差分更新テスト。"""

    def test_update_info(self, mock_api, client):
        mock_api.get("/v2/hojin/updateInfo").mock(
            return_value=httpx.Response(200, json={
                "hojin-infos": [
                    {"corporate_number": "1234567890123", "name": "更新テスト"},
                ],
                "id": "test",
                "message": "ok",
                "totalCount": "100",
                "totalPage": "1",
                "pageNumber": "1",
            })
        )
        result = client.get_update_info(
            from_date=date(2024, 1, 1),
            to_date=date(2024, 1, 31),
        )
        assert result.total_count == 100
        assert result.total_page == 1
        assert len(result.items) == 1


class TestContextManager:
    """コンテキストマネージャテスト。"""

    def test_sync_context_manager(self, mock_api):
        with GbizClient(api_token="test") as c:
            assert c is not None

    @pytest.mark.anyio()
    async def test_async_context_manager(self, mock_api):
        async with AsyncGbizClient(api_token="test") as c:
            assert c is not None
