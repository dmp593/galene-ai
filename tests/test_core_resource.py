from galene_ai._core.resource import SyncResource, operation


class _Fake(SyncResource):
    @operation("_list_files_v1_files_get")
    def list(self):
        return "ok"


def test_operation_decorator_tags_method():
    assert _Fake.list.__galene_operation__ == "_list_files_v1_files_get"


def test_resource_holds_client():
    r = _Fake(client="CLIENT")
    assert r._client == "CLIENT"
    assert r.list() == "ok"
