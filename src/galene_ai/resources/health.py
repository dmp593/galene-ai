"""`health` resource: application readiness and liveness probes.

Both `/readiness` and `/liveness` have empty (`{}`) 200 response schemas in
`spec/openapi.json`, so there is no generated model to decode into; the raw JSON
body is returned as a plain `dict`.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation

# Health probes are meant to answer "is the server up?" fast. So they default to
# a short timeout and DO NOT retry — when the backend is down you get a quick
# failure instead of waiting out the client's full request timeout (60s) times
# the retry budget. Pass a different `timeout=` to override.
DEFAULT_HEALTH_TIMEOUT = 5.0


class Health(SyncResource):
    """Application readiness and liveness health checks."""

    namespace: ClassVar[str] = "health"

    @operation("readiness_readiness_get")
    def readiness(self, *, timeout: float = DEFAULT_HEALTH_TIMEOUT) -> dict[str, Any]:
        """Application Readiness Check. Fails fast (default 5s, no retries)."""
        return cast(
            dict[str, Any],
            self._client.get(
                "/readiness", cast_to=dict, timeout=timeout, max_retries=0
            ),  # spec: untyped response
        )

    @operation("liveness_liveness_get")
    def liveness(self, *, timeout: float = DEFAULT_HEALTH_TIMEOUT) -> dict[str, Any]:
        """Application Liveness Check. Fails fast (default 5s, no retries)."""
        return cast(
            dict[str, Any],
            self._client.get(
                "/liveness", cast_to=dict, timeout=timeout, max_retries=0
            ),  # spec: untyped response
        )


class AsyncHealth(AsyncResource):
    """Async counterpart of `Health`."""

    namespace: ClassVar[str] = "health"

    @operation("readiness_readiness_get")
    async def readiness(self, *, timeout: float = DEFAULT_HEALTH_TIMEOUT) -> dict[str, Any]:
        """Application Readiness Check. Fails fast (default 5s, no retries)."""
        return cast(
            dict[str, Any],
            await self._client.get(
                "/readiness", cast_to=dict, timeout=timeout, max_retries=0
            ),  # spec: untyped response
        )

    @operation("liveness_liveness_get")
    async def liveness(self, *, timeout: float = DEFAULT_HEALTH_TIMEOUT) -> dict[str, Any]:
        """Application Liveness Check. Fails fast (default 5s, no retries)."""
        return cast(
            dict[str, Any],
            await self._client.get(
                "/liveness", cast_to=dict, timeout=timeout, max_retries=0
            ),  # spec: untyped response
        )


Galene._NAMESPACES.append(Health)
AsyncGalene._NAMESPACES.append(AsyncHealth)
