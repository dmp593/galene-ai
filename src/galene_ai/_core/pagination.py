from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from dataclasses import dataclass


@dataclass
class CursorPage[T]:
    data: list[T]
    has_more: bool
    last_id: str | None
    _fetch: Callable[[str | None], CursorPage[T]]

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def auto_paging_iter(self) -> Iterator[T]:
        page: CursorPage[T] | None = self
        while page is not None:
            yield from page.data
            # Stop when the server claims more but hands us no cursor to advance
            # (e.g. `has_more=True` with an empty page): re-fetching the same
            # `last_id` would loop forever.
            if page.has_more and page.last_id is not None:
                page = page._fetch(page.last_id)
            else:
                page = None


@dataclass
class OffsetPage[T]:
    data: list[T]
    has_more: bool
    limit: int
    offset: int
    _fetch: Callable[[int, int], OffsetPage[T]]

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def auto_paging_iter(self) -> Iterator[T]:
        page: OffsetPage[T] | None = self
        while page is not None:
            yield from page.data
            page = page._fetch(page.limit, page.offset + page.limit) if page.has_more else None


@dataclass
class AsyncCursorPage[T]:
    data: list[T]
    has_more: bool
    last_id: str | None
    _fetch: Callable[[str | None], Awaitable[AsyncCursorPage[T]]]

    async def __aiter__(self) -> AsyncIterator[T]:
        page: AsyncCursorPage[T] | None = self
        while page is not None:
            for item in page.data:
                yield item
            # See `CursorPage.auto_paging_iter`: never re-fetch without a cursor.
            if page.has_more and page.last_id is not None:
                page = await page._fetch(page.last_id)
            else:
                page = None


@dataclass
class AsyncOffsetPage[T]:
    data: list[T]
    has_more: bool
    limit: int
    offset: int
    _fetch: Callable[[int, int], Awaitable[AsyncOffsetPage[T]]]

    async def __aiter__(self) -> AsyncIterator[T]:
        page: AsyncOffsetPage[T] | None = self
        while page is not None:
            for item in page.data:
                yield item
            page = (
                await page._fetch(page.limit, page.offset + page.limit) if page.has_more else None
            )
