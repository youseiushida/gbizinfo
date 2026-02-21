"""カスタム基底モデルモジュール。

gBizINFO ライブラリ全体で使用する Pydantic 基底モデルを定義する。
"""

from __future__ import annotations

from pydantic import BaseModel as _PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(_PydanticBaseModel):
    """gBizINFO 共通基底モデル。

    全ての API レスポンスモデルが継承する基底クラス。

    設定:
        - ``populate_by_name``: ハイフン alias と Python フィールド名の
          両方でアクセス可能にする。
        - ``extra="ignore"``: API にフィールドが追加されても
          パースが壊れないようにする。
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )
