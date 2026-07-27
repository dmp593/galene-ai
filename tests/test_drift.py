import json
from pathlib import Path

from galene_ai import Galene
from galene_ai._registry import iter_implemented_operation_ids

ROOT = Path(__file__).resolve().parent.parent


def _expected() -> set[str]:
    ops = json.loads((ROOT / "spec" / "operations.json").read_text())
    return {row["operationId"] for row in ops}


def test_no_method_maps_to_unknown_operation():
    # Every implemented method must correspond to a real spec operation.
    assert iter_implemented_operation_ids(Galene) <= _expected()


def test_every_operation_is_implemented():
    # All 317 spec operations must have a resource method (and vice versa).
    assert iter_implemented_operation_ids(Galene) == _expected()
