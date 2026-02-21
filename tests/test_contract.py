"""契約テスト - fixtures の JSON スナップショットに対するパース互換性。"""

from __future__ import annotations

import json
from pathlib import Path

from gbizinfo.models._generated import (
    HojinInfoResponseSearchV2,
    HojinInfoResponseV2,
    HojinInfoUpdateInfoResponseV2,
)
from gbizinfo.models.responses import HojinInfo, HojinInfoSearch

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestSearchResponseContract:
    """search_response.json のパース。"""

    def test_parse(self):
        data = json.loads((FIXTURES_DIR / "search_response.json").read_text(encoding="utf-8"))
        resp = HojinInfoResponseSearchV2.model_validate(data)
        assert resp.hojin_infos is not None
        assert len(resp.hojin_infos) == 2
        assert resp.hojin_infos[0].name == "テスト株式会社"
        assert resp.id == "test-id-001"

    def test_items_as_search_model(self):
        data = json.loads((FIXTURES_DIR / "search_response.json").read_text(encoding="utf-8"))
        resp = HojinInfoResponseSearchV2.model_validate(data)
        for h in resp.hojin_infos or []:
            item = HojinInfoSearch.model_validate(h.model_dump(by_alias=True))
            assert item.corporate_number is not None


class TestDetailResponseContract:
    """hojin_detail_response.json のパース。"""

    def test_parse(self):
        data = json.loads((FIXTURES_DIR / "hojin_detail_response.json").read_text(encoding="utf-8"))
        resp = HojinInfoResponseV2.model_validate(data)
        assert resp.hojin_infos is not None
        assert len(resp.hojin_infos) == 1
        info = HojinInfo.model_validate(resp.hojin_infos[0].model_dump(by_alias=True))
        assert info.name == "トヨタ自動車株式会社"
        assert info.capital_stock == 635401790000

    def test_to_flat_dict(self):
        data = json.loads((FIXTURES_DIR / "hojin_detail_response.json").read_text(encoding="utf-8"))
        resp = HojinInfoResponseV2.model_validate(data)
        info = HojinInfo.model_validate(resp.hojin_infos[0].model_dump(by_alias=True))
        flat = info.to_flat_dict()
        assert flat["name"] == "トヨタ自動車株式会社"


class TestUpdateInfoResponseContract:
    """update_info_response.json のパース。"""

    def test_parse(self):
        data = json.loads((FIXTURES_DIR / "update_info_response.json").read_text(encoding="utf-8"))
        resp = HojinInfoUpdateInfoResponseV2.model_validate(data)
        assert resp.hojin_infos is not None
        assert len(resp.hojin_infos) == 1
        assert resp.totalCount == "150"
        assert resp.totalPage == "2"
        assert resp.pageNumber == "1"


class TestForwardCompatibility:
    """API フィールド追加でパースが壊れないこと。"""

    def test_extra_fields_ignored(self):
        data = {
            "hojin-infos": [
                {
                    "corporate_number": "1234567890123",
                    "name": "テスト",
                    "new_future_field": "should not break",
                    "another_new_field": [1, 2, 3],
                }
            ],
            "id": "test",
            "message": "ok",
            "brand_new_metadata": {"key": "value"},
        }
        resp = HojinInfoResponseSearchV2.model_validate(data)
        assert resp.hojin_infos is not None
        assert resp.hojin_infos[0].name == "テスト"
