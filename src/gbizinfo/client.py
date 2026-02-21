"""gBizINFO API クライアント実装モジュール。

同期クライアント :class:`GbizClient` と非同期クライアント :class:`AsyncGbizClient` を提供する。
キャッシュ、レート制限、リトライ、ページネーション等の機能を内包する。
"""

from __future__ import annotations

import os
import time
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypedDict

import httpx

from gbizinfo._logging import logger
from gbizinfo._version import __version__
from gbizinfo.cache import FileCache
from gbizinfo.config import (
    DEFAULT_BASE_URL,
    CacheConfig,
    CacheMode,
    ClientConfig,
    RetryConfig,
)
from gbizinfo.enums.corporate_type import CorporateType
from gbizinfo.enums.ministry import Ministry
from gbizinfo.enums.prefecture import Prefecture
from gbizinfo.enums.source import Source
from gbizinfo.enums.workplace import (
    AverageAge,
    AverageContinuousServiceYears,
    FemaleWorkersProportion,
    MonthAverageOvertimeHours,
)
from gbizinfo.errors import (
    GbizApiError,
    GbizBadRequestError,
    GbizErrorContext,
    GbizForbiddenError,
    GbizHttpStatusError,
    GbizNotFoundError,
    GbizRateLimitError,
    GbizServerError,
    GbizTimeoutError,
    GbizTransportError,
    GbizUnauthorizedError,
    GbizValidationError,
)
from gbizinfo.http import (
    AsyncConcurrencyLimiter,
    AsyncRateLimiter,
    SyncRateLimiter,
    build_request_headers,
    build_user_agent,
    compute_wait_time,
    parse_retry_after,
    should_retry_http_status,
    should_retry_transport_error,
)
from gbizinfo.models._generated import (
    ApiError,
    HojinInfoResponseSearchV2,
    HojinInfoResponseV2,
    HojinInfoUpdateInfoResponseV2,
)
from gbizinfo.models.responses import (
    HojinInfo,
    HojinInfoSearch,
    SearchResult,
    UpdateResult,
)
from gbizinfo.pagination import (
    paginate_search_async,
    paginate_search_sync,
    paginate_update_async,
    paginate_update_sync,
)
from gbizinfo.validation import format_date, validate_corporate_number

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator, Sequence

_PARAM_MAPPING: dict[str, str] = {
    "corporate_number": "corporate_number",
    "name": "name",
    "exist_flg": "exist_flg",
    "corporate_type": "corporate_type",
    "prefecture": "prefecture",
    "city": "city",
    "capital_stock_from": "capital_stock_from",
    "capital_stock_to": "capital_stock_to",
    "employee_number_from": "employee_number_from",
    "employee_number_to": "employee_number_to",
    "founded_year": "founded_year",
    "net_sales_from": "net_sales_summary_of_business_results_from",
    "net_sales_to": "net_sales_summary_of_business_results_to",
    "total_assets_from": "total_assets_summary_of_business_results_from",
    "total_assets_to": "total_assets_summary_of_business_results_to",
    "average_continuous_service_years": "average_continuous_service_years",
    "average_age": "average_age",
    "month_average_predetermined_overtime_hours": "month_average_predetermined_overtime_hours",
    "female_workers_proportion": "female_workers_proportion",
    "patent": "patent",
    "procurement": "procurement",
    "procurement_amount_from": "procurement_amount_from",
    "procurement_amount_to": "procurement_amount_to",
    "subsidy": "subsidy",
    "subsidy_amount_from": "subsidy_amount_from",
    "subsidy_amount_to": "subsidy_amount_to",
    "certification": "certification",
    "ministry": "ministry",
    "source": "source",
    "page": "page",
    "limit": "limit",
    "metadata_flg": "metadata_flg",
}


class SearchParams(TypedDict, total=False):
    """search() メソッドのパラメータ型定義。

    各フィールドは gBizINFO API の検索条件に対応する。
    """

    corporate_number: str | None
    name: str | None
    exist_flg: bool | None
    corporate_type: CorporateType | Sequence[CorporateType] | None
    prefecture: Prefecture | None
    city: str | None
    capital_stock_from: int | None
    capital_stock_to: int | None
    employee_number_from: int | None
    employee_number_to: int | None
    founded_year: int | Sequence[int] | None
    net_sales_from: int | None
    net_sales_to: int | None
    total_assets_from: int | None
    total_assets_to: int | None
    average_continuous_service_years: AverageContinuousServiceYears | None
    average_age: AverageAge | None
    month_average_predetermined_overtime_hours: MonthAverageOvertimeHours | None
    female_workers_proportion: FemaleWorkersProportion | None
    patent: str | None
    procurement: str | None
    procurement_amount_from: int | None
    procurement_amount_to: int | None
    subsidy: str | None
    subsidy_amount_from: int | None
    subsidy_amount_to: int | None
    certification: str | None
    ministry: Ministry | Sequence[Ministry] | None
    source: Source | Sequence[Source] | None
    page: int
    limit: int
    metadata_flg: bool


def _convert_param_value(key: str, value: Any) -> str:
    """公開パラメータ値を API 用文字列に変換する。

    Enum 型、bool 型、リスト型などを API が受け取れる文字列形式に変換する。

    Args:
        key: パラメータ名。
        value: パラメータ値。

    Returns:
        API 用の文字列表現。
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return ",".join(str(v.value) if isinstance(v, (CorporateType, Ministry, Source)) else str(v) for v in value)
    if isinstance(value, (CorporateType, Prefecture, Ministry, Source,
                          AverageAge, AverageContinuousServiceYears,
                          MonthAverageOvertimeHours, FemaleWorkersProportion)):
        return value.value
    if isinstance(value, int):
        return str(value)
    return str(value)


def _build_query_params(kwargs: dict[str, Any]) -> dict[str, str]:
    """公開引数名を API クエリパラメータ名に変換する。

    None の値は除外し、Enum 型等は文字列に変換する。

    Args:
        kwargs: 公開メソッドのキーワード引数辞書。

    Returns:
        API クエリパラメータの辞書。
    """
    params: dict[str, str] = {}
    for pub_name, value in kwargs.items():
        if value is None:
            continue
        api_name = _PARAM_MAPPING.get(pub_name)
        if api_name is None:
            continue
        params[api_name] = _convert_param_value(pub_name, value)
    return params


def _raise_for_status(response: httpx.Response) -> None:
    """HTTP ステータスコードに応じた例外を送出する。

    レスポンスの JSON ボディからエラー情報を抽出し、ステータスコードに
    対応する具体的な例外クラスを使用して送出する。

    Args:
        response: HTTP レスポンスオブジェクト。

    Raises:
        GbizBadRequestError: 400 Bad Request の場合。
        GbizUnauthorizedError: 401 Unauthorized の場合。
        GbizForbiddenError: 403 Forbidden の場合。
        GbizNotFoundError: 404 Not Found の場合。
        GbizRateLimitError: 429 Too Many Requests の場合。
        GbizServerError: 5xx サーバーエラーの場合。
        GbizApiError: 上記以外でエラー配列がある場合。
        GbizHttpStatusError: その他のエラーステータスの場合。
    """
    ctx = GbizErrorContext(
        request_url=str(response.request.url),
        request_method=response.request.method,
        status_code=response.status_code,
        response_headers=dict(response.headers),
        body_snippet=response.text[:2048] if response.text else None,
    )

    # Retry-After
    ra_header = response.headers.get("Retry-After")
    if ra_header:
        retry_after = parse_retry_after(response)
        ctx.retry_after = retry_after

    # JSON パース試行
    errors_list: list[ApiError] = []
    try:
        body = response.json()
        if isinstance(body, dict):
            ctx.response_id = body.get("id")
            raw_errors = body.get("errors")
            if isinstance(raw_errors, list):
                errors_list = [ApiError.model_validate(e) for e in raw_errors]
    except Exception:
        pass

    status = response.status_code
    msg = f"HTTP {status}: {ctx.body_snippet[:200] if ctx.body_snippet else ''}"

    if status == 400 and errors_list:
        raise GbizBadRequestError(msg, context=ctx, errors=errors_list)
    if status == 401:
        raise GbizUnauthorizedError(msg, context=ctx)
    if status == 403:
        raise GbizForbiddenError(msg, context=ctx)
    if status == 404:
        raise GbizNotFoundError(msg, context=ctx)
    if status == 429:
        raise GbizRateLimitError(msg, context=ctx)
    if status >= 500:
        raise GbizServerError(msg, context=ctx)

    if errors_list:
        raise GbizApiError(msg, context=ctx, errors=errors_list)

    raise GbizHttpStatusError(msg, context=ctx)


def _resolve_token(api_token: str | None) -> str:
    """API トークンを解決する。

    引数が None の場合は環境変数 ``GBIZINFO_API_TOKEN`` にフォールバックする。

    Args:
        api_token: API トークン文字列。None の場合は環境変数を参照する。

    Returns:
        解決された API トークン文字列。

    Raises:
        GbizValidationError: トークンが引数・環境変数のいずれでも未指定の場合。
    """
    if api_token is not None:
        return api_token
    env_token = os.environ.get("GBIZINFO_API_TOKEN")
    if env_token:
        return env_token
    raise GbizValidationError(
        "api_token が未指定です。引数で渡すか環境変数 GBIZINFO_API_TOKEN を設定してください。"
    )


class GbizClient:
    """gBizINFO API 同期クライアント。

    コンテキストマネージャとして使用可能。内部で httpx.Client を管理し、
    キャッシュ、レート制限、リトライ機能を提供する。

    Args:
        api_token: gBizINFO API トークン。None の場合は環境変数を参照する。
        base_url: API のベース URL。
        timeout: HTTP タイムアウト秒数。
        user_agent: User-Agent ヘッダ値。None の場合は自動生成される。
        rate_limit_per_sec: 1秒あたりの最大リクエスト数。
        cache_dir: キャッシュディレクトリのパス。None でキャッシュ無効。
        cache_mode: キャッシュモード。
        cache_ttl: キャッシュの有効期間（秒）。
        retry_max_attempts: 最大リトライ回数。
        retry_base_delay: リトライの基本待機秒数。
        retry_cap_delay: リトライの最大待機秒数。
        http_client: 外部から注入する httpx.Client。None で内部生成。
        http2: HTTP/2 を使用するかどうか。
        proxy: プロキシ URL。
        limits: httpx の接続制限設定。

    Example:
        >>> with GbizClient(api_token="your-token") as client:
        ...     result = client.search(name="トヨタ")
    """

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        user_agent: str | None = None,
        rate_limit_per_sec: float = 1.0,
        cache_dir: str | Path | None = None,
        cache_mode: CacheMode | str = CacheMode.OFF,
        cache_ttl: int = 86400,
        retry_max_attempts: int = 5,
        retry_base_delay: float = 0.5,
        retry_cap_delay: float = 8.0,
        http_client: httpx.Client | None = None,
        http2: bool = False,
        proxy: str | None = None,
        limits: httpx.Limits | None = None,
    ) -> None:
        self._api_token = _resolve_token(api_token)
        ua = user_agent or build_user_agent(version=__version__)

        cache_mode_norm = cache_mode if isinstance(cache_mode, CacheMode) else CacheMode(cache_mode)
        cache_conf = CacheConfig(
            mode=cache_mode_norm,
            dir=Path(cache_dir) if cache_dir is not None else None,
            ttl_seconds=cache_ttl,
        )
        self._config = ClientConfig(
            base_url=base_url,
            timeout=timeout,
            user_agent=ua,
            rate_limit_per_sec=rate_limit_per_sec,
            cache=cache_conf,
        )
        self._retry = RetryConfig(
            max_attempts=retry_max_attempts,
            base_delay=retry_base_delay,
            cap_delay=retry_cap_delay,
        )
        self._cache = FileCache(cache_dir=cache_conf.dir, ttl_seconds=cache_conf.ttl_seconds)
        self._limiter = SyncRateLimiter(rate_limit_per_sec=rate_limit_per_sec)
        self._headers = build_request_headers(user_agent=ua, api_token=self._api_token)

        self._owns_client = http_client is None
        if http_client is None:
            kwargs: dict[str, Any] = {
                "base_url": base_url,
                "timeout": timeout,
                "http2": http2,
            }
            if proxy is not None:
                kwargs["proxy"] = proxy
            if limits is not None:
                kwargs["limits"] = limits
            self._http_client = httpx.Client(**kwargs)
        else:
            self._http_client = http_client

    def close(self) -> None:
        """HTTP クライアントを閉じてリソースを解放する。"""
        if self._owns_client:
            self._http_client.close()

    def __enter__(self) -> GbizClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _request(self, method: str, path: str, *, params: dict[str, str]) -> dict[str, Any]:
        """内部 HTTP リクエストを実行する。

        キャッシュ読み取り → レートリミット → HTTP リクエスト → リトライの
        順序で処理を行い、成功時はレスポンスの JSON を返す。

        Args:
            method: HTTP メソッド。
            path: リクエストパス。
            params: クエリパラメータの辞書。

        Returns:
            レスポンスの JSON データ。

        Raises:
            GbizHttpStatusError: HTTP ステータスエラーの場合。
            GbizTransportError: トランスポートエラーの場合。
        """
        cache_key = FileCache.make_key(method=method, path=path, params=params)

        # キャッシュ読み取り
        hit = self._cache.get(key=cache_key, mode=self._config.cache.mode)
        if hit is not None and not hit.stale:
            return hit.payload

        last_exc: Exception | None = None
        last_response: httpx.Response | None = None
        for attempt in range(self._retry.max_attempts):
            self._limiter.acquire()
            try:
                response = self._http_client.request(
                    method, path, params=params, headers=self._headers
                )
            except httpx.TimeoutException as e:
                if not should_retry_transport_error(e):
                    raise GbizTimeoutError(str(e), original=e, timeout_type="read") from e
                last_exc = e
                wait = compute_wait_time(
                    attempt=attempt, base=self._retry.base_delay,
                    cap=self._retry.cap_delay, retry_after=None,
                )
                logger.warning("Retrying after %.1fs (attempt %d/%d, transport error)",
                               wait, attempt + 1, self._retry.max_attempts)
                time.sleep(wait)
                continue
            except httpx.TransportError as e:
                if not should_retry_transport_error(e):
                    raise GbizTransportError(str(e), original=e) from e
                last_exc = e
                wait = compute_wait_time(
                    attempt=attempt, base=self._retry.base_delay,
                    cap=self._retry.cap_delay, retry_after=None,
                )
                logger.warning("Retrying after %.1fs (attempt %d/%d, transport error)",
                               wait, attempt + 1, self._retry.max_attempts)
                time.sleep(wait)
                continue

            if response.status_code == 200:
                data: dict[str, Any] = response.json()
                # キャッシュ書き込み
                if self._config.cache.mode in (CacheMode.READ_WRITE, CacheMode.FORCE_REFRESH):
                    self._cache.put(key=cache_key, payload=data)
                return data

            if should_retry_http_status(response.status_code):
                retry_after = parse_retry_after(response)
                wait = compute_wait_time(
                    attempt=attempt, base=self._retry.base_delay,
                    cap=self._retry.cap_delay, retry_after=retry_after,
                )
                logger.warning("Retrying after %.1fs (attempt %d/%d, status=%d)",
                               wait, attempt + 1, self._retry.max_attempts, response.status_code)
                time.sleep(wait)
                last_response = response
                last_exc = None
                continue

            _raise_for_status(response)

        if last_exc is not None:
            if isinstance(last_exc, httpx.TimeoutException):
                raise GbizTimeoutError(str(last_exc), original=last_exc, timeout_type="read") from last_exc
            raise GbizTransportError(str(last_exc), original=last_exc) from last_exc
        if last_response is not None:
            _raise_for_status(last_response)
        raise AssertionError("unreachable")  # pragma: no cover

    # === 法人検索 ===

    def search(
        self,
        *,
        corporate_number: str | None = None,
        name: str | None = None,
        exist_flg: bool | None = None,
        corporate_type: CorporateType | Sequence[CorporateType] | None = None,
        prefecture: Prefecture | None = None,
        city: str | None = None,
        capital_stock_from: int | None = None,
        capital_stock_to: int | None = None,
        employee_number_from: int | None = None,
        employee_number_to: int | None = None,
        founded_year: int | Sequence[int] | None = None,
        net_sales_from: int | None = None,
        net_sales_to: int | None = None,
        total_assets_from: int | None = None,
        total_assets_to: int | None = None,
        average_continuous_service_years: AverageContinuousServiceYears | None = None,
        average_age: AverageAge | None = None,
        month_average_predetermined_overtime_hours: MonthAverageOvertimeHours | None = None,
        female_workers_proportion: FemaleWorkersProportion | None = None,
        patent: str | None = None,
        procurement: str | None = None,
        procurement_amount_from: int | None = None,
        procurement_amount_to: int | None = None,
        subsidy: str | None = None,
        subsidy_amount_from: int | None = None,
        subsidy_amount_to: int | None = None,
        certification: str | None = None,
        ministry: Ministry | Sequence[Ministry] | None = None,
        source: Source | Sequence[Source] | None = None,
        page: int = 1,
        limit: int = 1000,
        metadata_flg: bool = False,
    ) -> SearchResult:
        """法人情報を検索する。

        gBizINFO API の ``/v2/hojin`` エンドポイントを使用して
        条件に一致する法人情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            name: 法人名（部分一致）。
            exist_flg: 登記の存在フラグ。
            corporate_type: 法人種別。複数指定可。
            prefecture: 都道府県。
            city: 市区町村名。
            capital_stock_from: 資本金（下限）。
            capital_stock_to: 資本金（上限）。
            employee_number_from: 従業員数（下限）。
            employee_number_to: 従業員数（上限）。
            founded_year: 創業年。複数指定可。
            net_sales_from: 売上高（下限）。
            net_sales_to: 売上高（上限）。
            total_assets_from: 総資産額（下限）。
            total_assets_to: 総資産額（上限）。
            average_continuous_service_years: 平均継続勤務年数の区分。
            average_age: 従業員の平均年齢の区分。
            month_average_predetermined_overtime_hours: 月平均所定外労働時間の区分。
            female_workers_proportion: 女性労働者割合の区分。
            patent: 特許キーワード。
            procurement: 調達キーワード。
            procurement_amount_from: 調達金額（下限）。
            procurement_amount_to: 調達金額（上限）。
            subsidy: 補助金キーワード。
            subsidy_amount_from: 補助金額（下限）。
            subsidy_amount_to: 補助金額（上限）。
            certification: 届出認定キーワード。
            ministry: 担当府省。複数指定可。
            source: 出典元。複数指定可。
            page: ページ番号（1始まり）。
            limit: 1ページあたりの取得件数。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            検索結果を格納した SearchResult オブジェクト。
        """
        params = _build_query_params({
            "corporate_number": corporate_number, "name": name, "exist_flg": exist_flg,
            "corporate_type": corporate_type, "prefecture": prefecture, "city": city,
            "capital_stock_from": capital_stock_from, "capital_stock_to": capital_stock_to,
            "employee_number_from": employee_number_from, "employee_number_to": employee_number_to,
            "founded_year": founded_year, "net_sales_from": net_sales_from, "net_sales_to": net_sales_to,
            "total_assets_from": total_assets_from, "total_assets_to": total_assets_to,
            "average_continuous_service_years": average_continuous_service_years,
            "average_age": average_age,
            "month_average_predetermined_overtime_hours": month_average_predetermined_overtime_hours,
            "female_workers_proportion": female_workers_proportion,
            "patent": patent, "procurement": procurement,
            "procurement_amount_from": procurement_amount_from, "procurement_amount_to": procurement_amount_to,
            "subsidy": subsidy, "subsidy_amount_from": subsidy_amount_from, "subsidy_amount_to": subsidy_amount_to,
            "certification": certification, "ministry": ministry, "source": source,
            "page": page, "limit": limit, "metadata_flg": metadata_flg,
        })
        data = self._request("GET", "/v2/hojin", params=params)
        resp = HojinInfoResponseSearchV2.model_validate(data)
        items = [HojinInfoSearch.model_validate(h.model_dump(by_alias=True)) for h in (resp.hojin_infos or [])]
        return SearchResult(items)

    # === 法人番号指定取得 ===

    def get(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """法人番号を指定して法人情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            法人情報オブジェクト。

        Raises:
            GbizCorporateNumberError: 法人番号が不正な場合。
            GbizNotFoundError: 該当する法人が見つからない場合。
        """
        validate_corporate_number(corporate_number)
        params = _build_query_params({"metadata_flg": metadata_flg})
        data = self._request("GET", f"/v2/hojin/{corporate_number}", params=params)
        resp = HojinInfoResponseV2.model_validate(data)
        infos = resp.hojin_infos or []
        if not infos:
            raise GbizNotFoundError(
                f"法人番号 {corporate_number} のデータが見つかりません。",
                context=GbizErrorContext(request_url=f"/v2/hojin/{corporate_number}", request_method="GET",
                                         status_code=200),
            )
        return HojinInfo.model_validate(infos[0].model_dump(by_alias=True))

    def _get_sub_resource(self, corporate_number: str, sub: str, *, metadata_flg: bool = False) -> HojinInfo:
        """サブリソースを共通的に取得する内部メソッド。

        Args:
            corporate_number: 法人番号（13桁）。
            sub: サブリソース名（``"certification"``, ``"finance"`` 等）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            法人情報オブジェクト。データが存在しない場合は空の HojinInfo。
        """
        validate_corporate_number(corporate_number)
        params = _build_query_params({"metadata_flg": metadata_flg})
        data = self._request("GET", f"/v2/hojin/{corporate_number}/{sub}", params=params)
        resp = HojinInfoResponseV2.model_validate(data)
        infos = resp.hojin_infos or []
        return HojinInfo.model_validate(infos[0].model_dump(by_alias=True)) if infos else HojinInfo.model_construct(corporate_number="")

    def get_certification(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """届出・認定情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            届出・認定情報を含む法人情報オブジェクト。
        """
        return self._get_sub_resource(corporate_number, "certification", metadata_flg=metadata_flg)

    def get_commendation(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """表彰情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            表彰情報を含む法人情報オブジェクト。
        """
        return self._get_sub_resource(corporate_number, "commendation", metadata_flg=metadata_flg)

    def get_corporation(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """事業所情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            事業所情報を含む法人情報オブジェクト。
        """
        return self._get_sub_resource(corporate_number, "corporation", metadata_flg=metadata_flg)

    def get_finance(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """財務情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            財務情報を含む法人情報オブジェクト。
        """
        return self._get_sub_resource(corporate_number, "finance", metadata_flg=metadata_flg)

    def get_patent(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """特許情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            特許情報を含む法人情報オブジェクト。
        """
        return self._get_sub_resource(corporate_number, "patent", metadata_flg=metadata_flg)

    def get_procurement(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """調達情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            調達情報を含む法人情報オブジェクト。
        """
        return self._get_sub_resource(corporate_number, "procurement", metadata_flg=metadata_flg)

    def get_subsidy(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """補助金情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            補助金情報を含む法人情報オブジェクト。
        """
        return self._get_sub_resource(corporate_number, "subsidy", metadata_flg=metadata_flg)

    def get_workplace(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """職場情報を取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            職場情報を含む法人情報オブジェクト。
        """
        return self._get_sub_resource(corporate_number, "workplace", metadata_flg=metadata_flg)

    # === 差分更新 ===

    def _update_request(self, path: str, *, from_date: date, to_date: date,
                        page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """差分更新 API の内部リクエスト処理。

        Args:
            path: API エンドポイントパス。
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        params: dict[str, str] = {
            "from": format_date(from_date),
            "to": format_date(to_date),
            "page": str(page),
        }
        if metadata_flg:
            params["metadata_flg"] = "true"
        data = self._request("GET", path, params=params)
        resp = HojinInfoUpdateInfoResponseV2.model_validate(data)
        items = [HojinInfo.model_validate(h.model_dump(by_alias=True)) for h in (resp.hojin_infos or [])]
        return UpdateResult(
            items=items,
            total_count=int(resp.totalCount) if resp.totalCount else 0,
            total_page=int(resp.totalPage) if resp.totalPage else 0,
            page_number=int(resp.pageNumber) if resp.pageNumber else page,
        )

    def get_update_info(self, *, from_date: date, to_date: date,
                        page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """法人情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    def get_update_certification(self, *, from_date: date, to_date: date,
                                 page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """届出・認定情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo/certification", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    def get_update_commendation(self, *, from_date: date, to_date: date,
                                page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """表彰情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo/commendation", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    def get_update_corporation(self, *, from_date: date, to_date: date,
                               page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """事業所情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo/corporation", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    def get_update_finance(self, *, from_date: date, to_date: date,
                           page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """財務情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo/finance", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    def get_update_patent(self, *, from_date: date, to_date: date,
                          page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """特許情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo/patent", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    def get_update_procurement(self, *, from_date: date, to_date: date,
                               page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """調達情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo/procurement", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    def get_update_subsidy(self, *, from_date: date, to_date: date,
                           page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """補助金情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo/subsidy", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    def get_update_workplace(self, *, from_date: date, to_date: date,
                             page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """職場情報の差分更新を取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        return self._update_request("/v2/hojin/updateInfo/workplace", from_date=from_date,
                                    to_date=to_date, page=page, metadata_flg=metadata_flg)

    # === ページネーション ===

    def paginate_search(self, *, limit: int = 1000, **kwargs: Any) -> Iterator[HojinInfoSearch]:
        """検索結果を透過的にページネーションして全件取得する。

        Args:
            limit: 1ページあたりの取得件数。
            **kwargs: search() メソッドと同じ検索条件。

        Yields:
            検索結果の法人情報。
        """
        yield from paginate_search_sync(self, kwargs, limit=limit)

    def paginate_update_info(self, *, from_date: date, to_date: date,
                             metadata_flg: bool = False) -> Iterator[HojinInfo]:
        """差分更新結果を透過的にページネーションして全件取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            metadata_flg: メタデータを含めるかどうか。

        Yields:
            更新された法人情報。
        """
        yield from paginate_update_sync(
            self, from_date=from_date, to_date=to_date, metadata_flg=metadata_flg
        )

    # === ヘルパー ===

    def get_recent_updates(self, *, days: int = 7, metadata_flg: bool = False) -> Iterator[HojinInfo]:
        """過去 N 日分の更新を取得する。

        今日から days 日前までの差分更新を自動ページネーションで取得する。

        Args:
            days: 遡る日数。
            metadata_flg: メタデータを含めるかどうか。

        Yields:
            更新された法人情報。
        """
        from datetime import timedelta
        to_date = date.today()
        from_date = to_date - timedelta(days=days)
        yield from self.paginate_update_info(
            from_date=from_date, to_date=to_date, metadata_flg=metadata_flg
        )


class AsyncGbizClient:
    """gBizINFO API 非同期クライアント。

    async コンテキストマネージャとして使用可能。内部で httpx.AsyncClient を管理し、
    キャッシュ、レート制限、同時実行数制限、リトライ機能を提供する。

    Args:
        api_token: gBizINFO API トークン。None の場合は環境変数を参照する。
        max_concurrent: 同時実行の最大リクエスト数。
        base_url: API のベース URL。
        timeout: HTTP タイムアウト秒数。
        user_agent: User-Agent ヘッダ値。None の場合は自動生成される。
        rate_limit_per_sec: 1秒あたりの最大リクエスト数。
        cache_dir: キャッシュディレクトリのパス。None でキャッシュ無効。
        cache_mode: キャッシュモード。
        cache_ttl: キャッシュの有効期間（秒）。
        retry_max_attempts: 最大リトライ回数。
        retry_base_delay: リトライの基本待機秒数。
        retry_cap_delay: リトライの最大待機秒数。
        http_client: 外部から注入する httpx.AsyncClient。None で内部生成。
        http2: HTTP/2 を使用するかどうか。
        proxy: プロキシ URL。
        limits: httpx の接続制限設定。

    Example:
        >>> async with AsyncGbizClient(api_token="your-token") as client:
        ...     result = await client.search(name="トヨタ")
    """

    def __init__(
        self,
        api_token: str | None = None,
        *,
        max_concurrent: int = 10,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        user_agent: str | None = None,
        rate_limit_per_sec: float = 1.0,
        cache_dir: str | Path | None = None,
        cache_mode: CacheMode | str = CacheMode.OFF,
        cache_ttl: int = 86400,
        retry_max_attempts: int = 5,
        retry_base_delay: float = 0.5,
        retry_cap_delay: float = 8.0,
        http_client: httpx.AsyncClient | None = None,
        http2: bool = False,
        proxy: str | None = None,
        limits: httpx.Limits | None = None,
    ) -> None:
        self._api_token = _resolve_token(api_token)
        ua = user_agent or build_user_agent(version=__version__)

        cache_mode_norm = cache_mode if isinstance(cache_mode, CacheMode) else CacheMode(cache_mode)
        cache_conf = CacheConfig(
            mode=cache_mode_norm,
            dir=Path(cache_dir) if cache_dir is not None else None,
            ttl_seconds=cache_ttl,
        )
        self._config = ClientConfig(
            base_url=base_url,
            timeout=timeout,
            user_agent=ua,
            rate_limit_per_sec=rate_limit_per_sec,
            cache=cache_conf,
        )
        self._retry = RetryConfig(
            max_attempts=retry_max_attempts,
            base_delay=retry_base_delay,
            cap_delay=retry_cap_delay,
        )
        self._cache = FileCache(cache_dir=cache_conf.dir, ttl_seconds=cache_conf.ttl_seconds)
        self._limiter = AsyncRateLimiter(rate_limit_per_sec=rate_limit_per_sec)
        self._concurrency = AsyncConcurrencyLimiter(max_concurrent)
        self._headers = build_request_headers(user_agent=ua, api_token=self._api_token)

        self._owns_client = http_client is None
        if http_client is None:
            kwargs: dict[str, Any] = {
                "base_url": base_url,
                "timeout": timeout,
                "http2": http2,
            }
            if proxy is not None:
                kwargs["proxy"] = proxy
            if limits is not None:
                kwargs["limits"] = limits
            self._http_client = httpx.AsyncClient(**kwargs)
        else:
            self._http_client = http_client

    async def aclose(self) -> None:
        """HTTP クライアントを閉じてリソースを解放する。"""
        if self._owns_client:
            await self._http_client.aclose()

    async def __aenter__(self) -> AsyncGbizClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    async def _request(self, method: str, path: str, *, params: dict[str, str]) -> dict[str, Any]:
        """非同期で内部 HTTP リクエストを実行する。

        キャッシュ読み取り → レートリミット → HTTP リクエスト → リトライの
        順序で処理を行い、成功時はレスポンスの JSON を返す。

        Args:
            method: HTTP メソッド。
            path: リクエストパス。
            params: クエリパラメータの辞書。

        Returns:
            レスポンスの JSON データ。

        Raises:
            GbizHttpStatusError: HTTP ステータスエラーの場合。
            GbizTransportError: トランスポートエラーの場合。
        """
        import anyio

        cache_key = FileCache.make_key(method=method, path=path, params=params)

        hit = await self._cache.aget(key=cache_key, mode=self._config.cache.mode)
        if hit is not None and not hit.stale:
            return hit.payload

        last_exc: Exception | None = None
        last_response: httpx.Response | None = None
        for attempt in range(self._retry.max_attempts):
            await self._limiter.acquire()
            async with self._concurrency:
                try:
                    response = await self._http_client.request(
                        method, path, params=params, headers=self._headers
                    )
                except httpx.TimeoutException as e:
                    if not should_retry_transport_error(e):
                        raise GbizTimeoutError(str(e), original=e, timeout_type="read") from e
                    last_exc = e
                    wait = compute_wait_time(
                        attempt=attempt, base=self._retry.base_delay,
                        cap=self._retry.cap_delay, retry_after=None,
                    )
                    logger.warning("Retrying after %.1fs (attempt %d/%d, transport error)",
                                   wait, attempt + 1, self._retry.max_attempts)
                    await anyio.sleep(wait)
                    continue
                except httpx.TransportError as e:
                    if not should_retry_transport_error(e):
                        raise GbizTransportError(str(e), original=e) from e
                    last_exc = e
                    wait = compute_wait_time(
                        attempt=attempt, base=self._retry.base_delay,
                        cap=self._retry.cap_delay, retry_after=None,
                    )
                    logger.warning("Retrying after %.1fs (attempt %d/%d, transport error)",
                                   wait, attempt + 1, self._retry.max_attempts)
                    await anyio.sleep(wait)
                    continue

                if response.status_code == 200:
                    data: dict[str, Any] = response.json()
                    if self._config.cache.mode in (CacheMode.READ_WRITE, CacheMode.FORCE_REFRESH):
                        await self._cache.aput(key=cache_key, payload=data)
                    return data

                if should_retry_http_status(response.status_code):
                    retry_after = parse_retry_after(response)
                    wait = compute_wait_time(
                        attempt=attempt, base=self._retry.base_delay,
                        cap=self._retry.cap_delay, retry_after=retry_after,
                    )
                    logger.warning("Retrying after %.1fs (attempt %d/%d, status=%d)",
                                   wait, attempt + 1, self._retry.max_attempts, response.status_code)
                    await anyio.sleep(wait)
                    last_response = response
                    last_exc = None
                    continue

                _raise_for_status(response)

        if last_exc is not None:
            if isinstance(last_exc, httpx.TimeoutException):
                raise GbizTimeoutError(str(last_exc), original=last_exc, timeout_type="read") from last_exc
            raise GbizTransportError(str(last_exc), original=last_exc) from last_exc
        if last_response is not None:
            _raise_for_status(last_response)
        raise AssertionError("unreachable")  # pragma: no cover

    # === 法人検索 ===

    async def search(
        self,
        *,
        corporate_number: str | None = None,
        name: str | None = None,
        exist_flg: bool | None = None,
        corporate_type: CorporateType | Sequence[CorporateType] | None = None,
        prefecture: Prefecture | None = None,
        city: str | None = None,
        capital_stock_from: int | None = None,
        capital_stock_to: int | None = None,
        employee_number_from: int | None = None,
        employee_number_to: int | None = None,
        founded_year: int | Sequence[int] | None = None,
        net_sales_from: int | None = None,
        net_sales_to: int | None = None,
        total_assets_from: int | None = None,
        total_assets_to: int | None = None,
        average_continuous_service_years: AverageContinuousServiceYears | None = None,
        average_age: AverageAge | None = None,
        month_average_predetermined_overtime_hours: MonthAverageOvertimeHours | None = None,
        female_workers_proportion: FemaleWorkersProportion | None = None,
        patent: str | None = None,
        procurement: str | None = None,
        procurement_amount_from: int | None = None,
        procurement_amount_to: int | None = None,
        subsidy: str | None = None,
        subsidy_amount_from: int | None = None,
        subsidy_amount_to: int | None = None,
        certification: str | None = None,
        ministry: Ministry | Sequence[Ministry] | None = None,
        source: Source | Sequence[Source] | None = None,
        page: int = 1,
        limit: int = 1000,
        metadata_flg: bool = False,
    ) -> SearchResult:
        """法人情報を非同期で検索する。

        引数は同期版 :meth:`GbizClient.search` と同一。

        Returns:
            検索結果を格納した SearchResult オブジェクト。
        """
        params = _build_query_params({
            "corporate_number": corporate_number, "name": name, "exist_flg": exist_flg,
            "corporate_type": corporate_type, "prefecture": prefecture, "city": city,
            "capital_stock_from": capital_stock_from, "capital_stock_to": capital_stock_to,
            "employee_number_from": employee_number_from, "employee_number_to": employee_number_to,
            "founded_year": founded_year, "net_sales_from": net_sales_from, "net_sales_to": net_sales_to,
            "total_assets_from": total_assets_from, "total_assets_to": total_assets_to,
            "average_continuous_service_years": average_continuous_service_years,
            "average_age": average_age,
            "month_average_predetermined_overtime_hours": month_average_predetermined_overtime_hours,
            "female_workers_proportion": female_workers_proportion,
            "patent": patent, "procurement": procurement,
            "procurement_amount_from": procurement_amount_from, "procurement_amount_to": procurement_amount_to,
            "subsidy": subsidy, "subsidy_amount_from": subsidy_amount_from, "subsidy_amount_to": subsidy_amount_to,
            "certification": certification, "ministry": ministry, "source": source,
            "page": page, "limit": limit, "metadata_flg": metadata_flg,
        })
        data = await self._request("GET", "/v2/hojin", params=params)
        resp = HojinInfoResponseSearchV2.model_validate(data)
        items = [HojinInfoSearch.model_validate(h.model_dump(by_alias=True)) for h in (resp.hojin_infos or [])]
        return SearchResult(items)

    async def get(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """法人番号を指定して法人情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            法人情報オブジェクト。

        Raises:
            GbizCorporateNumberError: 法人番号が不正な場合。
            GbizNotFoundError: 該当する法人が見つからない場合。
        """
        validate_corporate_number(corporate_number)
        params = _build_query_params({"metadata_flg": metadata_flg})
        data = await self._request("GET", f"/v2/hojin/{corporate_number}", params=params)
        resp = HojinInfoResponseV2.model_validate(data)
        infos = resp.hojin_infos or []
        if not infos:
            raise GbizNotFoundError(
                f"法人番号 {corporate_number} のデータが見つかりません。",
                context=GbizErrorContext(request_url=f"/v2/hojin/{corporate_number}", request_method="GET",
                                         status_code=200),
            )
        return HojinInfo.model_validate(infos[0].model_dump(by_alias=True))

    async def _get_sub_resource(self, corporate_number: str, sub: str, *, metadata_flg: bool = False) -> HojinInfo:
        """サブリソースを非同期で共通的に取得する内部メソッド。

        Args:
            corporate_number: 法人番号（13桁）。
            sub: サブリソース名。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            法人情報オブジェクト。データが存在しない場合は空の HojinInfo。
        """
        validate_corporate_number(corporate_number)
        params = _build_query_params({"metadata_flg": metadata_flg})
        data = await self._request("GET", f"/v2/hojin/{corporate_number}/{sub}", params=params)
        resp = HojinInfoResponseV2.model_validate(data)
        infos = resp.hojin_infos or []
        return HojinInfo.model_validate(infos[0].model_dump(by_alias=True)) if infos else HojinInfo.model_construct(corporate_number="")

    async def get_certification(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """届出・認定情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            届出・認定情報を含む法人情報オブジェクト。
        """
        return await self._get_sub_resource(corporate_number, "certification", metadata_flg=metadata_flg)

    async def get_commendation(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """表彰情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            表彰情報を含む法人情報オブジェクト。
        """
        return await self._get_sub_resource(corporate_number, "commendation", metadata_flg=metadata_flg)

    async def get_corporation(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """事業所情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            事業所情報を含む法人情報オブジェクト。
        """
        return await self._get_sub_resource(corporate_number, "corporation", metadata_flg=metadata_flg)

    async def get_finance(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """財務情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            財務情報を含む法人情報オブジェクト。
        """
        return await self._get_sub_resource(corporate_number, "finance", metadata_flg=metadata_flg)

    async def get_patent(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """特許情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            特許情報を含む法人情報オブジェクト。
        """
        return await self._get_sub_resource(corporate_number, "patent", metadata_flg=metadata_flg)

    async def get_procurement(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """調達情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            調達情報を含む法人情報オブジェクト。
        """
        return await self._get_sub_resource(corporate_number, "procurement", metadata_flg=metadata_flg)

    async def get_subsidy(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """補助金情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            補助金情報を含む法人情報オブジェクト。
        """
        return await self._get_sub_resource(corporate_number, "subsidy", metadata_flg=metadata_flg)

    async def get_workplace(self, corporate_number: str, *, metadata_flg: bool = False) -> HojinInfo:
        """職場情報を非同期で取得する。

        Args:
            corporate_number: 法人番号（13桁）。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            職場情報を含む法人情報オブジェクト。
        """
        return await self._get_sub_resource(corporate_number, "workplace", metadata_flg=metadata_flg)

    # === 差分更新 ===

    async def _update_request(self, path: str, *, from_date: date, to_date: date,
                              page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """差分更新 API の非同期内部リクエスト処理。

        Args:
            path: API エンドポイントパス。
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            page: ページ番号。
            metadata_flg: メタデータを含めるかどうか。

        Returns:
            差分更新結果。
        """
        params: dict[str, str] = {
            "from": format_date(from_date),
            "to": format_date(to_date),
            "page": str(page),
        }
        if metadata_flg:
            params["metadata_flg"] = "true"
        data = await self._request("GET", path, params=params)
        resp = HojinInfoUpdateInfoResponseV2.model_validate(data)
        items = [HojinInfo.model_validate(h.model_dump(by_alias=True)) for h in (resp.hojin_infos or [])]
        return UpdateResult(
            items=items,
            total_count=int(resp.totalCount) if resp.totalCount else 0,
            total_page=int(resp.totalPage) if resp.totalPage else 0,
            page_number=int(resp.pageNumber) if resp.pageNumber else page,
        )

    async def get_update_info(self, *, from_date: date, to_date: date,
                              page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """法人情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_info` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    async def get_update_certification(self, *, from_date: date, to_date: date,
                                       page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """届出・認定情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_certification` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo/certification", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    async def get_update_commendation(self, *, from_date: date, to_date: date,
                                      page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """表彰情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_commendation` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo/commendation", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    async def get_update_corporation(self, *, from_date: date, to_date: date,
                                     page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """事業所情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_corporation` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo/corporation", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    async def get_update_finance(self, *, from_date: date, to_date: date,
                                 page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """財務情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_finance` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo/finance", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    async def get_update_patent(self, *, from_date: date, to_date: date,
                                page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """特許情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_patent` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo/patent", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    async def get_update_procurement(self, *, from_date: date, to_date: date,
                                     page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """調達情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_procurement` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo/procurement", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    async def get_update_subsidy(self, *, from_date: date, to_date: date,
                                 page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """補助金情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_subsidy` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo/subsidy", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    async def get_update_workplace(self, *, from_date: date, to_date: date,
                                   page: int = 1, metadata_flg: bool = False) -> UpdateResult:
        """職場情報の差分更新を非同期で取得する。

        引数・戻り値は同期版 :meth:`GbizClient.get_update_workplace` と同一。
        """
        return await self._update_request("/v2/hojin/updateInfo/workplace", from_date=from_date,
                                          to_date=to_date, page=page, metadata_flg=metadata_flg)

    # === ページネーション ===

    async def paginate_search(self, *, limit: int = 1000, **kwargs: Any) -> AsyncIterator[HojinInfoSearch]:
        """検索結果を透過的にページネーションして非同期で全件取得する。

        Args:
            limit: 1ページあたりの取得件数。
            **kwargs: search() メソッドと同じ検索条件。

        Yields:
            検索結果の法人情報。
        """
        async for item in paginate_search_async(self, kwargs, limit=limit):
            yield item

    async def paginate_update_info(self, *, from_date: date, to_date: date,
                                   metadata_flg: bool = False) -> AsyncIterator[HojinInfo]:
        """差分更新結果を透過的にページネーションして非同期で全件取得する。

        Args:
            from_date: 更新期間の開始日。
            to_date: 更新期間の終了日。
            metadata_flg: メタデータを含めるかどうか。

        Yields:
            更新された法人情報。
        """
        async for item in paginate_update_async(
            self, from_date=from_date, to_date=to_date, metadata_flg=metadata_flg
        ):
            yield item

    # === ヘルパー ===

    async def get_recent_updates(self, *, days: int = 7, metadata_flg: bool = False) -> AsyncIterator[HojinInfo]:
        """過去 N 日分の更新を非同期で取得する。

        Args:
            days: 遡る日数。
            metadata_flg: メタデータを含めるかどうか。

        Yields:
            更新された法人情報。
        """
        from datetime import timedelta
        to_date = date.today()
        from_date = to_date - timedelta(days=days)
        async for item in self.paginate_update_info(
            from_date=from_date, to_date=to_date, metadata_flg=metadata_flg
        ):
            yield item
