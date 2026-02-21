"""都道府県（JIS X 0401）の列挙型モジュール。

47都道府県をJIS X 0401コードで定義する。
"""

from __future__ import annotations

from enum import StrEnum


class Prefecture(StrEnum):
    """都道府県の列挙型（JIS X 0401 準拠）。

    各都道府県に JIS X 0401 の2桁コードを割り当てる。
    検索時に prefecture パラメータとして指定する。
    """

    北海道 = "01"
    青森県 = "02"
    岩手県 = "03"
    宮城県 = "04"
    秋田県 = "05"
    山形県 = "06"
    福島県 = "07"
    茨城県 = "08"
    栃木県 = "09"
    群馬県 = "10"
    埼玉県 = "11"
    千葉県 = "12"
    東京都 = "13"
    神奈川県 = "14"
    新潟県 = "15"
    富山県 = "16"
    石川県 = "17"
    福井県 = "18"
    山梨県 = "19"
    長野県 = "20"
    岐阜県 = "21"
    静岡県 = "22"
    愛知県 = "23"
    三重県 = "24"
    滋賀県 = "25"
    京都府 = "26"
    大阪府 = "27"
    兵庫県 = "28"
    奈良県 = "29"
    和歌山県 = "30"
    鳥取県 = "31"
    島根県 = "32"
    岡山県 = "33"
    広島県 = "34"
    山口県 = "35"
    徳島県 = "36"
    香川県 = "37"
    愛媛県 = "38"
    高知県 = "39"
    福岡県 = "40"
    佐賀県 = "41"
    長崎県 = "42"
    熊本県 = "43"
    大分県 = "44"
    宮崎県 = "45"
    鹿児島県 = "46"
    沖縄県 = "47"


# 英語 alias
HOKKAIDO = Prefecture.北海道
AOMORI = Prefecture.青森県
IWATE = Prefecture.岩手県
MIYAGI = Prefecture.宮城県
AKITA = Prefecture.秋田県
YAMAGATA = Prefecture.山形県
FUKUSHIMA = Prefecture.福島県
IBARAKI = Prefecture.茨城県
TOCHIGI = Prefecture.栃木県
GUNMA = Prefecture.群馬県
SAITAMA = Prefecture.埼玉県
CHIBA = Prefecture.千葉県
TOKYO = Prefecture.東京都
KANAGAWA = Prefecture.神奈川県
NIIGATA = Prefecture.新潟県
TOYAMA = Prefecture.富山県
ISHIKAWA = Prefecture.石川県
FUKUI = Prefecture.福井県
YAMANASHI = Prefecture.山梨県
NAGANO = Prefecture.長野県
GIFU = Prefecture.岐阜県
SHIZUOKA = Prefecture.静岡県
AICHI = Prefecture.愛知県
MIE = Prefecture.三重県
SHIGA = Prefecture.滋賀県
KYOTO = Prefecture.京都府
OSAKA = Prefecture.大阪府
HYOGO = Prefecture.兵庫県
NARA = Prefecture.奈良県
WAKAYAMA = Prefecture.和歌山県
TOTTORI = Prefecture.鳥取県
SHIMANE = Prefecture.島根県
OKAYAMA = Prefecture.岡山県
HIROSHIMA = Prefecture.広島県
YAMAGUCHI = Prefecture.山口県
TOKUSHIMA = Prefecture.徳島県
KAGAWA = Prefecture.香川県
EHIME = Prefecture.愛媛県
KOCHI = Prefecture.高知県
FUKUOKA = Prefecture.福岡県
SAGA = Prefecture.佐賀県
NAGASAKI = Prefecture.長崎県
KUMAMOTO = Prefecture.熊本県
OITA = Prefecture.大分県
MIYAZAKI = Prefecture.宮崎県
KAGOSHIMA = Prefecture.鹿児島県
OKINAWA = Prefecture.沖縄県
