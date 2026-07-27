from galene_ai._core.pagination import CursorPage


def test_cursor_auto_paging_iter_walks_all_pages():
    pages = {
        None: (["a", "b"], True, "b"),
        "b": (["c"], False, "c"),
    }

    def fetch(after):
        data, has_more, last_id = pages[after]
        return CursorPage(data=data, has_more=has_more, last_id=last_id, _fetch=fetch)

    first = fetch(None)
    assert list(first.auto_paging_iter()) == ["a", "b", "c"]
    assert list(first) == ["a", "b"]  # __iter__ is this page only


def test_cursor_auto_paging_terminates_when_has_more_but_no_cursor():
    # Degenerate/buggy server response: has_more=True but no cursor to advance.
    # auto_paging_iter must terminate instead of re-fetching last_id=None forever.
    calls = 0

    def fetch(after):
        nonlocal calls
        calls += 1
        return CursorPage(data=[], has_more=True, last_id=None, _fetch=fetch)

    first = CursorPage(data=["a"], has_more=True, last_id=None, _fetch=fetch)
    assert list(first.auto_paging_iter()) == ["a"]
    assert calls == 0  # never advanced past the cursorless first page


async def test_async_cursor_auto_paging_terminates_when_has_more_but_no_cursor():
    from galene_ai._core.pagination import AsyncCursorPage

    calls = 0

    async def fetch(after):
        nonlocal calls
        calls += 1
        return AsyncCursorPage(data=[], has_more=True, last_id=None, _fetch=fetch)

    first = AsyncCursorPage(data=["a"], has_more=True, last_id=None, _fetch=fetch)
    assert [x async for x in first] == ["a"]
    assert calls == 0
