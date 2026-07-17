from __future__ import annotations

from typing import Any


def iter_implemented_operation_ids(client_cls: type[Any]) -> set[str]:
    ids: set[str] = set()
    for ns_cls in _namespace_classes(client_cls):
        for attr in vars(ns_cls).values():
            op_id = getattr(attr, "__galene_operation__", None)
            if op_id:
                ids.add(op_id)
    return ids


def _namespace_classes(client_cls: type[Any]) -> list[type[Any]]:
    # Populated by Galene._NAMESPACES / _ADMIN_NAMESPACES (resource classes,
    # incl. admin sub-resources).
    namespaces: list[type[Any]] = list(getattr(client_cls, "_NAMESPACES", []))
    namespaces += list(getattr(client_cls, "_ADMIN_NAMESPACES", []))
    return namespaces
