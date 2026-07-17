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
