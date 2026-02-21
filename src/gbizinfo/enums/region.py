"""地域対応表（gBizINFO 内部コード）モジュール。

日本の地域区分と各地域に含まれる都道府県の対応を定義する。
"""

from __future__ import annotations

from enum import StrEnum

from gbizinfo.enums.prefecture import Prefecture


class Region(StrEnum):
    """地域の列挙型（gBizINFO 内部コード）。

    日本の10地域区分を定義する。各地域が含む都道府県は
    ``prefectures`` プロパティで取得できる。
    """

    北海道 = "1"
    東北 = "2"
    関東 = "3"
    北陸 = "4"
    中部 = "5"
    近畿 = "6"
    中国 = "7"
    四国 = "8"
    九州 = "9"
    沖縄 = "10"

    @property
    def prefectures(self) -> tuple[Prefecture, ...]:
        """この地域に含まれる都道府県のタプルを返す。

        Returns:
            都道府県の列挙値のタプル。
        """
        return _REGION_PREFECTURES[self]


_REGION_PREFECTURES: dict[Region, tuple[Prefecture, ...]] = {
    Region.北海道: (Prefecture.北海道,),
    Region.東北: (
        Prefecture.青森県,
        Prefecture.岩手県,
        Prefecture.宮城県,
        Prefecture.秋田県,
        Prefecture.山形県,
        Prefecture.福島県,
    ),
    Region.関東: (
        Prefecture.茨城県,
        Prefecture.栃木県,
        Prefecture.群馬県,
        Prefecture.埼玉県,
        Prefecture.千葉県,
        Prefecture.東京都,
        Prefecture.神奈川県,
    ),
    Region.北陸: (
        Prefecture.新潟県,
        Prefecture.富山県,
        Prefecture.石川県,
        Prefecture.福井県,
    ),
    Region.中部: (
        Prefecture.山梨県,
        Prefecture.長野県,
        Prefecture.岐阜県,
        Prefecture.静岡県,
        Prefecture.愛知県,
        Prefecture.三重県,
    ),
    Region.近畿: (
        Prefecture.滋賀県,
        Prefecture.京都府,
        Prefecture.大阪府,
        Prefecture.兵庫県,
        Prefecture.奈良県,
        Prefecture.和歌山県,
    ),
    Region.中国: (
        Prefecture.鳥取県,
        Prefecture.島根県,
        Prefecture.岡山県,
        Prefecture.広島県,
        Prefecture.山口県,
    ),
    Region.四国: (
        Prefecture.徳島県,
        Prefecture.香川県,
        Prefecture.愛媛県,
        Prefecture.高知県,
    ),
    Region.九州: (
        Prefecture.福岡県,
        Prefecture.佐賀県,
        Prefecture.長崎県,
        Prefecture.熊本県,
        Prefecture.大分県,
        Prefecture.宮崎県,
        Prefecture.鹿児島県,
    ),
    Region.沖縄: (Prefecture.沖縄県,),
}


# 英語 alias
HOKKAIDO = Region.北海道
TOHOKU = Region.東北
KANTO = Region.関東
HOKURIKU = Region.北陸
CHUBU = Region.中部
KINKI = Region.近畿
CHUGOKU = Region.中国
SHIKOKU = Region.四国
KYUSHU = Region.九州
OKINAWA = Region.沖縄
