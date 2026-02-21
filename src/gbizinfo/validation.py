"""入力値バリデーションモジュール。

法人番号のチェックデジット検証や日付フォーマット変換など、
API リクエスト送信前のバリデーション処理を提供する。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from gbizinfo.errors import GbizCorporateNumberError

if TYPE_CHECKING:
    from datetime import date


def validate_corporate_number(value: str) -> str:
    """法人番号（13桁）をバリデーションする。

    桁数チェックおよびチェックデジット検証を行う。

    チェックデジット計算:
        法人番号の先頭1桁 = 9 - (Σ(Pi × Qi) mod 9)

        - P: 2桁目以降の各桁
        - Q: 偶数位置は1, 奇数位置は2

    Args:
        value: 検証対象の法人番号文字列。

    Returns:
        検証済みの法人番号文字列（入力値をそのまま返す）。

    Raises:
        GbizCorporateNumberError: 桁数不正またはチェックデジット不一致の場合。
    """
    if not value.isdigit() or len(value) != 13:
        raise GbizCorporateNumberError(
            f"法人番号は13桁の数字である必要があります: {value!r}"
        )

    digits = [int(c) for c in value]
    body = digits[1:]  # 2桁目以降
    total = 0
    for i, p in enumerate(body):
        # 右端から数えて n=1,2,...,12 とすると Q=1(n奇数), Q=2(n偶数)
        # 左端(i=0)は n=12(偶数→Q=2), i=1 は n=11(奇数→Q=1), ...
        q = 2 if i % 2 == 0 else 1
        total += p * q

    expected_check = 9 - (total % 9)
    if digits[0] != expected_check:
        raise GbizCorporateNumberError(
            f"法人番号のチェックデジットが不正です: {value!r} "
            f"(期待値={expected_check}, 実際={digits[0]})"
        )

    return value


def format_date(d: date) -> str:
    """datetime.date を yyyyMMdd 形式の文字列に変換する。

    Args:
        d: 変換対象の日付オブジェクト。

    Returns:
        ``"20260221"`` 形式の日付文字列。
    """
    return d.strftime("%Y%m%d")
