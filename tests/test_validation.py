"""法人番号バリデーションテスト。"""

from __future__ import annotations

from datetime import date

import pytest

from gbizinfo.errors import GbizCorporateNumberError
from gbizinfo.validation import format_date, validate_corporate_number


class TestValidateCorporateNumber:
    """法人番号バリデーション。"""

    def test_valid_number(self):
        """正しい法人番号はそのまま返る。"""
        # 1180001015846: body 180001015846 → check=1
        assert validate_corporate_number("1180001015846") == "1180001015846"

    def test_valid_number_national_tax(self):
        """国税庁の法人番号。"""
        assert validate_corporate_number("7000012050002") == "7000012050002"

    def test_too_short(self):
        """12桁以下は拒否。"""
        with pytest.raises(GbizCorporateNumberError, match="13桁"):
            validate_corporate_number("123456789012")

    def test_too_long(self):
        """14桁以上は拒否。"""
        with pytest.raises(GbizCorporateNumberError, match="13桁"):
            validate_corporate_number("12345678901234")

    def test_non_digit(self):
        """数字以外は拒否。"""
        with pytest.raises(GbizCorporateNumberError, match="13桁"):
            validate_corporate_number("123456789012a")

    def test_bad_check_digit(self):
        """チェックデジットが不正な場合。"""
        # 2180001015846: 正しいチェックデジットは 1 なので 2 は不正
        with pytest.raises(GbizCorporateNumberError, match="チェックデジット"):
            validate_corporate_number("2180001015846")

    def test_empty(self):
        """空文字列は拒否。"""
        with pytest.raises(GbizCorporateNumberError):
            validate_corporate_number("")


class TestFormatDate:
    """日付フォーマット。"""

    def test_format(self):
        assert format_date(date(2024, 1, 15)) == "20240115"

    def test_format_padded(self):
        assert format_date(date(2024, 3, 5)) == "20240305"
