import galene_ai


def test_package_exposes_versions():
    assert isinstance(galene_ai.__version__, str)
    assert isinstance(galene_ai.__api_version__, str)
