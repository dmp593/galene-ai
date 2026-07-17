import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_registry_covers_all_operations():
    spec = json.loads((ROOT / "spec" / "openapi.json").read_text())
    ops = json.loads((ROOT / "spec" / "operations.json").read_text())
    spec_ids = {
        op["operationId"]
        for item in spec["paths"].values()
        for method, op in item.items()
        if method in {"get", "post", "put", "patch", "delete"}
    }
    reg_ids = {row["operationId"] for row in ops}
    assert reg_ids == spec_ids
    assert len(ops) == 316
