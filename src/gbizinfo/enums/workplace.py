"""職場情報の区分コード列挙型モジュール。

従業員の平均年齢、平均継続勤務年数、月平均所定外労働時間、
女性労働者割合の区分コードを定義する。
"""

from __future__ import annotations

from enum import StrEnum


class AverageAge(StrEnum):
    """従業員の平均年齢の区分コード。

    検索時に average_age パラメータとして指定する。
    ``label`` / ``label_en`` プロパティで日英のラベルを取得できる。
    """

    歳30以下 = "A"
    歳31から45 = "B"
    歳46から60 = "C"
    歳61以上 = "D"

    @property
    def label(self) -> str:
        """日本語ラベルを返す。"""
        return _AVERAGE_AGE_LABELS[self][0]

    @property
    def label_en(self) -> str:
        """英語ラベルを返す。"""
        return _AVERAGE_AGE_LABELS[self][1]


_AVERAGE_AGE_LABELS: dict[AverageAge, tuple[str, str]] = {
    AverageAge.歳30以下: ("～30歳", "30 or under"),
    AverageAge.歳31から45: ("31歳～45歳", "31-45"),
    AverageAge.歳46から60: ("46歳～60歳", "46-60"),
    AverageAge.歳61以上: ("61歳～", "61 or over"),
}


class AverageContinuousServiceYears(StrEnum):
    """平均継続勤務年数の区分コード。

    検索時に average_continuous_service_years パラメータとして指定する。
    ``label`` / ``label_en`` プロパティで日英のラベルを取得できる。
    """

    年5以下 = "A"
    年6から10 = "B"
    年11から20 = "C"
    年21以上 = "D"

    @property
    def label(self) -> str:
        """日本語ラベルを返す。"""
        return _SERVICE_YEARS_LABELS[self][0]

    @property
    def label_en(self) -> str:
        """英語ラベルを返す。"""
        return _SERVICE_YEARS_LABELS[self][1]


_SERVICE_YEARS_LABELS: dict[AverageContinuousServiceYears, tuple[str, str]] = {
    AverageContinuousServiceYears.年5以下: ("～5年", "5 years or less"),
    AverageContinuousServiceYears.年6から10: ("6年～10年", "6-10 years"),
    AverageContinuousServiceYears.年11から20: ("11年～20年", "11-20 years"),
    AverageContinuousServiceYears.年21以上: ("21年～", "21 years or more"),
}


class MonthAverageOvertimeHours(StrEnum):
    """月平均所定外労働時間の区分コード。

    検索時に month_average_predetermined_overtime_hours パラメータとして指定する。
    ``label`` / ``label_en`` プロパティで日英のラベルを取得できる。
    """

    時間20未満 = "A"
    時間40未満 = "B"
    時間40以上 = "C"

    @property
    def label(self) -> str:
        """日本語ラベルを返す。"""
        return _OVERTIME_LABELS[self][0]

    @property
    def label_en(self) -> str:
        """英語ラベルを返す。"""
        return _OVERTIME_LABELS[self][1]


_OVERTIME_LABELS: dict[MonthAverageOvertimeHours, tuple[str, str]] = {
    MonthAverageOvertimeHours.時間20未満: ("20時間未満", "Less than 20 hours"),
    MonthAverageOvertimeHours.時間40未満: ("40時間未満", "Less than 40 hours"),
    MonthAverageOvertimeHours.時間40以上: ("40時間以上", "40 hours or more"),
}


class FemaleWorkersProportion(StrEnum):
    """労働者に占める女性労働者の割合の区分コード。

    検索時に female_workers_proportion パラメータとして指定する。
    ``label`` / ``label_en`` プロパティで日英のラベルを取得できる。
    """

    割合20以下 = "A"
    割合21から40 = "B"
    割合41から60 = "C"
    割合61以上 = "D"

    @property
    def label(self) -> str:
        """日本語ラベルを返す。"""
        return _FEMALE_LABELS[self][0]

    @property
    def label_en(self) -> str:
        """英語ラベルを返す。"""
        return _FEMALE_LABELS[self][1]


_FEMALE_LABELS: dict[FemaleWorkersProportion, tuple[str, str]] = {
    FemaleWorkersProportion.割合20以下: ("～20%", "20% or less"),
    FemaleWorkersProportion.割合21から40: ("21%～40%", "21%-40%"),
    FemaleWorkersProportion.割合41から60: ("41%～60%", "41%-60%"),
    FemaleWorkersProportion.割合61以上: ("61%～", "61% or more"),
}
