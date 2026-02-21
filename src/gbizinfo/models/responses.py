"""レスポンスラッパーモデルおよびフラット化拡張モジュール。

API レスポンスのラッパークラスと、ネストされた Pydantic モデルを
フラットな辞書に変換する ``to_flat_dict()`` 機能を提供する。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel as PydanticBaseModel

from gbizinfo.models._generated import HojinInfoSearchV2, HojinInfoV2

ListStrategy = Literal["count", "first", "json", "explode"]


def _flatten(
    obj: Any,
    *,
    prefix: str,
    sep: str,
    lists: ListStrategy,
    max_items: int,
    result: dict[str, Any],
) -> None:
    """ネストされたオブジェクトを再帰的にフラット化する。

    Pydantic モデルのフィールドを辿り、プレフィックス付きの
    キーで result 辞書に書き込む。

    Args:
        obj: フラット化対象のオブジェクト。
        prefix: 現在のキーのプレフィックス。
        sep: プレフィックスの区切り文字。
        lists: リスト型フィールドの処理戦略。
        max_items: ``"explode"`` 戦略時の最大展開数。
        result: 結果を格納する辞書（破壊的に更新される）。
    """
    if obj is None:
        return

    if isinstance(obj, PydanticBaseModel):
        for field_name in type(obj).model_fields:
            value = getattr(obj, field_name, None)
            key = f"{prefix}{sep}{field_name}" if prefix else field_name
            _flatten(value, prefix=key, sep=sep, lists=lists, max_items=max_items, result=result)
        return

    if isinstance(obj, list):
        if lists == "count":
            result[f"{prefix}_count"] = len(obj)
        elif lists == "first":
            if obj:
                _flatten(obj[0], prefix=prefix, sep=sep, lists=lists, max_items=max_items, result=result)
        elif lists == "json":
            items = []
            for item in obj:
                if isinstance(item, PydanticBaseModel):
                    items.append(item.model_dump(by_alias=False))
                else:
                    items.append(item)
            result[prefix] = json.dumps(items, ensure_ascii=False, default=str)
        elif lists == "explode":
            for i, item in enumerate(obj[:max_items]):
                idx_prefix = f"{prefix}_{i}"
                _flatten(item, prefix=idx_prefix, sep=sep, lists=lists, max_items=max_items, result=result)
        return

    result[prefix] = obj


class _FlatDictMixin:
    """``to_flat_dict()`` メソッドを提供する Mixin クラス。

    Pydantic モデルに組み込むことで、ネストされたフィールドを
    フラットな辞書に変換する機能を追加する。
    """

    def to_flat_dict(
        self,
        *,
        prefix_separator: str = "_",
        lists: ListStrategy = "count",
        max_items: int = 10,
    ) -> dict[str, Any]:
        """ネストされたモデルをフラット化した辞書を返す。

        Args:
            prefix_separator: ネストしたフィールド名の区切り文字。
            lists: リスト型フィールドの処理戦略。
                ``"count"`` で件数のみ、``"first"`` で先頭要素のみ、
                ``"json"`` で JSON 文字列化、``"explode"`` でインデックス付き展開。
            max_items: ``"explode"`` 時の最大展開数。

        Returns:
            フラット化されたフィールド名と値の辞書。
        """
        result: dict[str, Any] = {}
        for field_name in type(self).model_fields:  # type: ignore[attr-defined]
            value = getattr(self, field_name, None)
            _flatten(
                value,
                prefix=field_name,
                sep=prefix_separator,
                lists=lists,
                max_items=max_items,
                result=result,
            )
        return result


class HojinInfo(_FlatDictMixin, HojinInfoV2):
    """法人情報（拡張）。

    ``HojinInfoV2`` に ``to_flat_dict()`` メソッドを追加した拡張モデル。
    """


class HojinInfoSearch(_FlatDictMixin, HojinInfoSearchV2):
    """法人検索情報（拡張）。

    ``HojinInfoSearchV2`` に ``to_flat_dict()`` メソッドを追加した拡張モデル。
    """


@dataclass
class SearchResult:
    """検索結果（/v2/hojin 系）を格納するデータクラス。

    Attributes:
        items: 検索にヒットした法人情報のリスト。
    """

    items: list[HojinInfoSearch] = field(default_factory=list)

    def to_flat_dicts(
        self,
        *,
        lists: ListStrategy = "count",
        max_items: int = 10,
    ) -> list[dict[str, Any]]:
        """全件をフラット化した辞書のリストを返す。

        Args:
            lists: リスト型フィールドの処理戦略。
            max_items: ``"explode"`` 時の最大展開数。

        Returns:
            各法人情報をフラット化した辞書のリスト。
        """
        return [item.to_flat_dict(lists=lists, max_items=max_items) for item in self.items]


@dataclass
class UpdateResult:
    """差分更新結果（/v2/hojin/updateInfo 系）を格納するデータクラス。

    Attributes:
        items: 更新された法人情報のリスト。
        total_count: 総件数。
        total_page: 総ページ数。
        page_number: 現在のページ番号。
    """

    items: list[HojinInfo] = field(default_factory=list)
    total_count: int = 0
    total_page: int = 0
    page_number: int = 0

    def to_flat_dicts(
        self,
        *,
        lists: ListStrategy = "count",
        max_items: int = 10,
    ) -> list[dict[str, Any]]:
        """全件をフラット化した辞書のリストを返す。

        Args:
            lists: リスト型フィールドの処理戦略。
            max_items: ``"explode"`` 時の最大展開数。

        Returns:
            各法人情報をフラット化した辞書のリスト。
        """
        return [item.to_flat_dict(lists=lists, max_items=max_items) for item in self.items]
