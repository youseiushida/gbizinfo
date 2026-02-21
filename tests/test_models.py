"""モデルテスト。"""

from __future__ import annotations

import json

from gbizinfo.models.responses import HojinInfo, HojinInfoSearch, SearchResult, UpdateResult


class TestToFlatDict:
    """to_flat_dict() テスト。"""

    def test_count_strategy(self):
        info = HojinInfo.model_validate({
            "name": "テスト株式会社",
            "corporate_number": "1234567890123",
            "certification": [
                {"title": "認定A"},
                {"title": "認定B"},
            ],
        })
        flat = info.to_flat_dict(lists="count")
        assert flat["name"] == "テスト株式会社"
        assert flat["certification_count"] == 2

    def test_first_strategy(self):
        info = HojinInfo.model_validate({
            "name": "テスト",
            "corporate_number": "1234567890123",
            "patent": [
                {"patent_type": "特許", "title": "特許A"},
                {"patent_type": "意匠", "title": "意匠B"},
            ],
        })
        flat = info.to_flat_dict(lists="first")
        assert flat["patent_patent_type"] == "特許"

    def test_json_strategy(self):
        info = HojinInfo.model_validate({
            "name": "テスト",
            "corporate_number": "1234567890123",
            "procurement": [
                {"title": "調達A"},
            ],
        })
        flat = info.to_flat_dict(lists="json")
        parsed = json.loads(flat["procurement"])
        assert len(parsed) == 1

    def test_explode_strategy(self):
        info = HojinInfo.model_validate({
            "name": "テスト",
            "corporate_number": "1234567890123",
            "subsidy": [
                {"title": "補助金A"},
                {"title": "補助金B"},
            ],
        })
        flat = info.to_flat_dict(lists="explode", max_items=10)
        assert flat["subsidy_0_title"] == "補助金A"
        assert flat["subsidy_1_title"] == "補助金B"


class TestAlias:
    """ハイフン alias テスト。"""

    def test_hojin_infos_alias(self):
        from gbizinfo.models._generated import HojinInfoResponseSearchV2
        resp = HojinInfoResponseSearchV2.model_validate({
            "hojin-infos": [{"name": "テスト", "corporate_number": "1234567890123"}],
            "id": "test",
        })
        assert resp.hojin_infos is not None
        assert len(resp.hojin_infos) == 1

    def test_populate_by_name(self):
        from gbizinfo.models._generated import HojinInfoResponseSearchV2
        resp = HojinInfoResponseSearchV2.model_validate({
            "hojin_infos": [{"name": "テスト", "corporate_number": "1234567890123"}],
            "id": "test",
        })
        assert resp.hojin_infos is not None


class TestExtraIgnore:
    """extra="ignore" テスト。"""

    def test_unknown_field_ignored(self):
        info = HojinInfo.model_validate({
            "name": "テスト",
            "corporate_number": "1234567890123",
            "unknown_future_field": "should be ignored",
            "another_field": 42,
        })
        assert info.name == "テスト"


class TestSearchResult:
    def test_to_flat_dicts(self):
        result = SearchResult([
            HojinInfoSearch.model_validate({"name": "A", "corporate_number": "1234567890123"}),
            HojinInfoSearch.model_validate({"name": "B", "corporate_number": "9876543210123"}),
        ])
        dicts = result.to_flat_dicts()
        assert len(dicts) == 2


class TestUpdateResult:
    def test_metadata(self):
        result = UpdateResult(
            items=[HojinInfo.model_validate({"name": "A", "corporate_number": "1234567890123"})],
            total_count=100,
            total_page=2,
            page_number=1,
        )
        assert result.total_count == 100
        assert result.total_page == 2
