"""出典元の列挙型モジュール。

gBizINFO API の出典元コードに対応する StrEnum を定義する。
"""

from __future__ import annotations

from enum import StrEnum


class Source(StrEnum):
    """出典元の列挙型。

    gBizINFO API で使用される出典元コードを定義する。
    検索時に source パラメータとして指定する。
    """

    調達 = "1"
    表彰 = "2"
    届出認定 = "3"
    補助金 = "4"
    特許 = "5"
    財務 = "6"


# 英語 alias
PROCUREMENT = Source.調達
COMMENDATION = Source.表彰
CERTIFICATION = Source.届出認定
SUBSIDY = Source.補助金
PATENT = Source.特許
FINANCE = Source.財務
