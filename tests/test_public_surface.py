"""The public `galene_ai` surface is a stability contract — guard it."""

import galene_ai


def test_core_exports_importable():
    from galene_ai import (  # noqa: F401
        ApiKeyAuth,
        AsyncGalene,
        AsyncStream,
        CursorPage,
        Galene,
        GaleneError,
        NotFoundError,
        OffsetPage,
        SessionAuth,
        Stream,
    )


def test_error_hierarchy_is_catchable():
    from galene_ai import AuthenticationError, GaleneError

    assert issubclass(AuthenticationError, GaleneError)


def test_versions_are_strings():
    assert isinstance(galene_ai.__version__, str)
    assert isinstance(galene_ai.__api_version__, str)


def test_all_names_resolve():
    for name in galene_ai.__all__:
        assert hasattr(galene_ai, name), name
