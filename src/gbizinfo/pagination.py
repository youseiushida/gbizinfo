"""ページネーション処理モジュール。

検索結果および差分更新結果の透過的なページネーションを提供する。
同期・非同期の両方に対応したジェネレータ関数を含む。
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from gbizinfo._logging import logger
from gbizinfo.config import MAX_PAGE, MAX_TOTAL_RECORDS
from gbizinfo.errors import PaginationLimitExceededError

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator
    from datetime import date

    from gbizinfo.client import AsyncGbizClient, GbizClient
    from gbizinfo.models.responses import HojinInfo, HojinInfoSearch


def paginate_search_sync(
    client: GbizClient,
    params: dict[str, Any],
    *,
    start_page: int = 1,
    limit: int = 1000,
) -> Iterator[HojinInfoSearch]:
    """検索結果を透過的にページネーションする（同期版）。

    全ページを自動で取得し、各アイテムを順に yield する。
    ページネーション上限に達した場合は PaginationLimitExceededError を送出する。

    Args:
        client: 同期 gBizINFO クライアント。
        params: 検索パラメータの辞書。
        start_page: 開始ページ番号。
        limit: 1ページあたりの取得件数。

    Yields:
        検索結果の法人情報。

    Raises:
        PaginationLimitExceededError: ページネーション上限に到達した場合。
    """
    page = start_page
    while True:
        if page > MAX_PAGE:
            raise PaginationLimitExceededError(
                f"検索結果がページネーション上限（{MAX_PAGE}ページ / {MAX_TOTAL_RECORDS:,}件）に到達しました。"
                " 検索条件を絞り込む（都道府県・法人種別等の追加）か、limit を調整してください。",
                max_retrievable=MAX_TOTAL_RECORDS,
            )
        logger.debug("Fetching page %d/%d", page, MAX_PAGE)
        result = client.search(**params, page=page, limit=limit)
        yield from result.items
        if len(result.items) < limit:
            break
        page += 1


async def paginate_search_async(
    client: AsyncGbizClient,
    params: dict[str, Any],
    *,
    start_page: int = 1,
    limit: int = 1000,
) -> AsyncIterator[HojinInfoSearch]:
    """検索結果を透過的にページネーションする（非同期版）。

    全ページを自動で取得し、各アイテムを順に yield する。
    ページネーション上限に達した場合は PaginationLimitExceededError を送出する。

    Args:
        client: 非同期 gBizINFO クライアント。
        params: 検索パラメータの辞書。
        start_page: 開始ページ番号。
        limit: 1ページあたりの取得件数。

    Yields:
        検索結果の法人情報。

    Raises:
        PaginationLimitExceededError: ページネーション上限に到達した場合。
    """
    page = start_page
    while True:
        if page > MAX_PAGE:
            raise PaginationLimitExceededError(
                f"検索結果がページネーション上限（{MAX_PAGE}ページ / {MAX_TOTAL_RECORDS:,}件）に到達しました。"
                " 検索条件を絞り込む（都道府県・法人種別等の追加）か、limit を調整してください。",
                max_retrievable=MAX_TOTAL_RECORDS,
            )
        logger.debug("Fetching page %d/%d", page, MAX_PAGE)
        result = await client.search(**params, page=page, limit=limit)
        for item in result.items:
            yield item
        if len(result.items) < limit:
            break
        page += 1


def paginate_update_sync(
    client: GbizClient,
    *,
    from_date: date,
    to_date: date,
    metadata_flg: bool = False,
) -> Iterator[HojinInfo]:
    """差分更新結果を透過的にページネーションする（同期版）。

    全ページを自動で取得し、各アイテムを順に yield する。

    Args:
        client: 同期 gBizINFO クライアント。
        from_date: 更新期間の開始日。
        to_date: 更新期間の終了日。
        metadata_flg: メタデータを含めるかどうか。

    Yields:
        更新された法人情報。

    Raises:
        PaginationLimitExceededError: ページネーション上限に到達した場合。
    """
    page = 1
    while True:
        if page > MAX_PAGE:
            raise PaginationLimitExceededError(
                f"差分更新結果がページネーション上限（{MAX_PAGE}ページ）に到達しました。"
                " 期間を短くして分割取得してください。",
                max_retrievable=MAX_TOTAL_RECORDS,
            )
        logger.debug("Fetching update page %d", page)
        result = client.get_update_info(
            from_date=from_date, to_date=to_date, page=page, metadata_flg=metadata_flg
        )
        yield from result.items
        if page >= result.total_page:
            break
        page += 1


async def paginate_update_async(
    client: AsyncGbizClient,
    *,
    from_date: date,
    to_date: date,
    metadata_flg: bool = False,
) -> AsyncIterator[HojinInfo]:
    """差分更新結果を透過的にページネーションする（非同期版）。

    全ページを自動で取得し、各アイテムを順に yield する。

    Args:
        client: 非同期 gBizINFO クライアント。
        from_date: 更新期間の開始日。
        to_date: 更新期間の終了日。
        metadata_flg: メタデータを含めるかどうか。

    Yields:
        更新された法人情報。

    Raises:
        PaginationLimitExceededError: ページネーション上限に到達した場合。
    """
    page = 1
    while True:
        if page > MAX_PAGE:
            raise PaginationLimitExceededError(
                f"差分更新結果がページネーション上限（{MAX_PAGE}ページ）に到達しました。"
                " 期間を短くして分割取得してください。",
                max_retrievable=MAX_TOTAL_RECORDS,
            )
        logger.debug("Fetching update page %d", page)
        result = await client.get_update_info(
            from_date=from_date, to_date=to_date, page=page, metadata_flg=metadata_flg
        )
        for item in result.items:
            yield item
        if page >= result.total_page:
            break
        page += 1
