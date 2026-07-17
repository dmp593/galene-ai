"""Admin resource namespaces (attached under ``client.admin.*``).

Each submodule ends with ``Galene._ADMIN_NAMESPACES.append(...)`` /
``AsyncGalene._ADMIN_NAMESPACES.append(...)``. The parent ``resources`` package
auto-imports this subpackage's modules, so a new ``admin/<name>.py`` registers itself.
"""
