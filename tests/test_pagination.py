"""ページネーションテスト。"""

from __future__ import annotations

import httpx
import pytest

from gbizinfo.errors import PaginationLimitExceededError

BASE_URL = "https://api.info.gbiz.go.jp/hojin"


class TestPaginateSearch:
    """paginate_search テスト。"""

    def test_single_page(self, mock_api, client):
        """1ページ分の結果で終了。"""
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(200, json={
                "hojin-infos": [
                    {"corporate_number": f"{i:013d}", "name": f"法人{i}"}
                    for i in range(50)
                ],
                "id": "test",
                "message": "ok",
            })
        )
        items = list(client.paginate_search(name="test", limit=1000))
        assert len(items) == 50

    def test_multiple_pages(self, mock_api, client):
        """複数ページの透過的取得。"""
        call_count = 0

        def handler(request):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                items = [{"corporate_number": f"{i:013d}", "name": f"法人{i}"} for i in range(10)]
            else:
                items = [{"corporate_number": f"{i:013d}", "name": f"法人{i}"} for i in range(5)]
            return httpx.Response(200, json={
                "hojin-infos": items,
                "id": "test",
                "message": "ok",
            })

        mock_api.get("/v2/hojin").mock(side_effect=handler)
        items = list(client.paginate_search(name="test", limit=10))
        assert len(items) == 25  # 10 + 10 + 5
        assert call_count == 3

    def test_page_limit_exceeded(self, mock_api, client):
        """10ページ超過で PaginationLimitExceededError。"""
        # Always return full page
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(200, json={
                "hojin-infos": [
                    {"corporate_number": f"{i:013d}", "name": f"法人{i}"}
                    for i in range(1000)
                ],
                "id": "test",
                "message": "ok",
            })
        )
        with pytest.raises(PaginationLimitExceededError, match="上限"):
            list(client.paginate_search(name="test", limit=1000))

    def test_empty_result(self, mock_api, client):
        """空結果。"""
        mock_api.get("/v2/hojin").mock(
            return_value=httpx.Response(200, json={
                "hojin-infos": [],
                "id": "test",
                "message": "ok",
            })
        )
        items = list(client.paginate_search(name="nonexistent", limit=1000))
        assert len(items) == 0


class TestPaginateUpdateInfo:
    """paginate_update_info テスト。"""

    def test_uses_total_page(self, mock_api, client):
        """totalPage で終了判定。"""
        from datetime import date

        call_count = 0

        def handler(request):
            nonlocal call_count
            call_count += 1
            return httpx.Response(200, json={
                "hojin-infos": [
                    {"corporate_number": f"{i:013d}", "name": f"法人{i}"}
                    for i in range(3)
                ],
                "id": "test",
                "message": "ok",
                "totalCount": "6",
                "totalPage": "2",
                "pageNumber": str(call_count),
            })

        mock_api.get("/v2/hojin/updateInfo").mock(side_effect=handler)
        items = list(client.paginate_update_info(
            from_date=date(2024, 1, 1),
            to_date=date(2024, 1, 31),
        ))
        assert len(items) == 6
        assert call_count == 2
