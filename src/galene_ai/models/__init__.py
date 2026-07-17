# src/galene_ai/models/__init__.py
"""msgspec models for the Galene API.

Combines the generated models (`_generated.py`, do not hand-edit) with the
hand-written models for response shapes the OpenAPI spec leaves untyped
(`_extra.py`, see its module docstring).

`_extra.py` names are re-exported via a `__all__`-scoped star-import (rather than
the `globals().update()` trick used for the generated names below) so that
`from galene_ai.models import File` etc. is visible to `mypy --strict` — every
resource module that wants a hand-written model imports it this way. `_extra.py`
defines its own `__all__` so the star-import can't leak its `msgspec`/`Any`
imports into this namespace. The generated module has no stable, hand-maintained
name list (it's regenerated from the spec), so its public names are still
collected dynamically via the `__module__` filter, which keeps that path
correct but not mypy-visible from here; import `galene_ai.models._generated`
directly if a resource needs static typing for a generated model.
"""

from galene_ai.models import _generated as _g
from galene_ai.models._extra import *  # noqa: F403
from galene_ai.models._extra import __all__ as _extra_names

_generated_names = [
    name
    for name in dir(_g)
    if not name.startswith("_") and getattr(getattr(_g, name), "__module__", None) == _g.__name__
]

__all__ = sorted(set(_generated_names) | set(_extra_names))

globals().update({name: getattr(_g, name) for name in _generated_names})
