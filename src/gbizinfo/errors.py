"""gBizINFO ライブラリの例外階層を定義するモジュール。

全ての例外は GbizError を基底クラスとし、HTTP ステータスエラー・
トランスポートエラー・バリデーションエラー等に分類される。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gbizinfo.models._generated import ApiError


@dataclass(slots=True)
class GbizErrorContext:
    """例外に付随するリクエスト/レスポンス情報。

    HTTP リクエストやレスポンスの詳細情報を保持し、
    デバッグやエラーハンドリングに利用する。

    Attributes:
        request_url: リクエスト先の URL。
        request_method: HTTP メソッド（GET, POST 等）。
        status_code: HTTP ステータスコード。レスポンスがない場合は None。
        response_headers: レスポンスヘッダの辞書。
        body_snippet: レスポンスボディの先頭部分（最大2048文字）。
        response_id: API が返すレスポンス ID。
        retry_after: Retry-After ヘッダから算出した待機秒数。
    """

    request_url: str = ""
    request_method: str = ""
    status_code: int | None = None
    response_headers: dict[str, str] = field(default_factory=dict)
    body_snippet: str | None = None
    response_id: str | None = None
    retry_after: float | None = None


class GbizError(Exception):
    """gBizINFO ライブラリ例外の基底クラス。

    全てのライブラリ固有例外はこのクラスを継承する。
    """


class GbizHttpStatusError(GbizError):
    """HTTP ステータスが 200 以外の場合に発生する例外。

    Attributes:
        context: リクエスト/レスポンスの詳細情報。

    Args:
        message: エラーメッセージ。
        context: リクエスト/レスポンスの詳細情報。
    """

    def __init__(self, message: str, *, context: GbizErrorContext) -> None:
        super().__init__(message)
        self.context = context


class GbizApiError(GbizHttpStatusError):
    """API がエラーレスポンスを返した場合の例外。

    HTTP ステータスが 200 以外かつ JSON パースに成功し、
    errors 配列が取得できた場合に発生する。

    Attributes:
        errors: API から返されたエラー情報のリスト。

    Args:
        message: エラーメッセージ。
        context: リクエスト/レスポンスの詳細情報。
        errors: API エラー情報のリスト。
    """

    def __init__(
        self,
        message: str,
        *,
        context: GbizErrorContext,
        errors: list[ApiError],
    ) -> None:
        super().__init__(message, context=context)
        self.errors = errors


class GbizBadRequestError(GbizApiError):
    """400 Bad Request エラー。

    リクエストパラメータが不正な場合に発生する。
    """


class GbizUnauthorizedError(GbizHttpStatusError):
    """401 Unauthorized エラー。

    API トークンが無効または未指定の場合に発生する。
    """


class GbizForbiddenError(GbizHttpStatusError):
    """403 Forbidden エラー。

    リソースへのアクセス権限がない場合に発生する。
    """


class GbizNotFoundError(GbizHttpStatusError):
    """404 Not Found エラー。

    指定されたリソースが存在しない場合に発生する。
    """


class GbizRateLimitError(GbizHttpStatusError):
    """429 Too Many Requests エラー。

    API のレート制限に到達した場合に発生する。
    """


class GbizServerError(GbizHttpStatusError):
    """5xx サーバーエラー。

    API サーバー側で内部エラーが発生した場合に送出される。
    """


class GbizTransportError(GbizError):
    """HTTP 通信層の例外。

    接続失敗、タイムアウト等のトランスポート層エラーで発生する。

    Attributes:
        original: 元の例外オブジェクト。

    Args:
        message: エラーメッセージ。
        original: 元の例外オブジェクト。
    """

    def __init__(self, message: str, *, original: Exception) -> None:
        super().__init__(message)
        self.original = original


class GbizTimeoutError(GbizTransportError):
    """HTTP リクエストのタイムアウトエラー。

    Attributes:
        timeout_type: タイムアウトの種別（``"read"``, ``"connect"`` 等）。

    Args:
        message: エラーメッセージ。
        original: 元の例外オブジェクト。
        timeout_type: タイムアウトの種別。
    """

    def __init__(
        self,
        message: str,
        *,
        original: Exception,
        timeout_type: str,
    ) -> None:
        super().__init__(message, original=original)
        self.timeout_type = timeout_type


class GbizValidationError(GbizError):
    """送信前バリデーションエラー。

    API リクエスト送信前のパラメータ検証で不正が見つかった場合に発生する。
    """


class GbizCorporateNumberError(GbizValidationError):
    """法人番号バリデーションエラー。

    法人番号の桁数やチェックデジットが不正な場合に発生する。
    """


class PaginationLimitExceededError(GbizError):
    """API のページネーション上限に到達した場合の例外。

    gBizINFO API はページネーションの上限があり、それを超えるデータは
    取得できない。検索条件の絞り込みが必要。

    Attributes:
        total_count: API が返した総件数。不明な場合は None。
        max_retrievable: 取得可能な最大件数。

    Args:
        message: エラーメッセージ。
        total_count: API が返した総件数。
        max_retrievable: 取得可能な最大件数。
    """

    def __init__(
        self,
        message: str,
        *,
        total_count: int | None = None,
        max_retrievable: int,
    ) -> None:
        super().__init__(message)
        self.total_count = total_count
        self.max_retrievable = max_retrievable
