"""法人種別の列挙型モジュール。

gBizINFO API の法人種別コードに対応する StrEnum を定義する。
"""

from __future__ import annotations

from enum import StrEnum


class CorporateType(StrEnum):
    """法人種別の列挙型。

    gBizINFO API で使用される法人種別コードを定義する。
    検索時に corporate_type パラメータとして指定する。
    """

    国の機関 = "101"
    地方公共団体 = "201"
    株式会社 = "301"
    有限会社 = "302"
    合名会社 = "303"
    合資会社 = "304"
    合同会社 = "305"
    その他の設立登記法人 = "399"
    外国会社等 = "401"
    その他 = "499"


# 英語 alias
NATIONAL_AGENCY = CorporateType.国の機関
LOCAL_GOVERNMENT = CorporateType.地方公共団体
KABUSHIKI_KAISHA = CorporateType.株式会社
YUGEN_KAISHA = CorporateType.有限会社
GOMEI_KAISHA = CorporateType.合名会社
GOSHI_KAISHA = CorporateType.合資会社
GODO_KAISHA = CorporateType.合同会社
OTHER_REGISTERED = CorporateType.その他の設立登記法人
FOREIGN_COMPANY = CorporateType.外国会社等
OTHER = CorporateType.その他
