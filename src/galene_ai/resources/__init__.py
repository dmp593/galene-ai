"""Resource namespace modules.

Every submodule ends with ``Galene._NAMESPACES.append(...)`` /
``AsyncGalene._NAMESPACES.append(...)`` (or the ``_ADMIN_NAMESPACES`` equivalents for
``admin/`` submodules), so importing a module registers its resource class(es) as a
side effect.

This package auto-imports every submodule and subpackage (recursively) on import, so a
new ``resources/<name>.py`` or ``resources/admin/<name>.py`` file registers itself with
no edit to this file. ``galene_ai/__init__.py`` imports this package, so ``Galene(...)``
and ``AsyncGalene(...)`` have every implemented namespace attached automatically.
"""

import importlib
import os
import pkgutil
from collections.abc import Iterable

# When GALENE_DEV_RESILIENT_IMPORT=1, a resource module that fails to import is
# skipped instead of breaking the whole package. This exists ONLY for parallel
# development (agents editing sibling modules concurrently); production and CI
# leave it unset, so a genuinely broken module fails loudly on import.
_RESILIENT = os.environ.get("GALENE_DEV_RESILIENT_IMPORT") == "1"


def _import_all(path: Iterable[str], prefix: str) -> None:
    for info in pkgutil.iter_modules(path, prefix):
        try:
            importlib.import_module(info.name)
        except Exception:
            if not _RESILIENT:
                raise
            continue
        if info.ispkg:
            subpackage = importlib.import_module(info.name)
            _import_all(subpackage.__path__, info.name + ".")


_import_all(__path__, __name__ + ".")
