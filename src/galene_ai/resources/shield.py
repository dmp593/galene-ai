"""`shield` resource: manage shields and their organization/agent attachments."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import ShieldEntity, ShieldUpsert


class Shield(SyncResource):
    """Manage shields and attach them to organizations and agents."""

    namespace: ClassVar[str] = "shield"

    @operation("_list_shields_shield__get")
    def list(self) -> list[ShieldEntity]:
        """List all shields."""
        return cast(
            list[ShieldEntity],
            self._client.get("/shield/", cast_to=list[ShieldEntity], envelope=True),
        )

    @operation("_create_shield_shield_post")
    def create(self, body: ShieldUpsert) -> ShieldEntity:
        """Create a new shield."""
        return cast(
            ShieldEntity,
            self._client.post("/shield", json_body=body, cast_to=ShieldEntity, envelope=True),
        )

    @operation("_get_shield_shield__shield_uuid__get")
    def retrieve(self, shield_uuid: str) -> ShieldEntity:
        """Get shield by UUID."""
        return cast(
            ShieldEntity,
            self._client.get(f"/shield/{shield_uuid}", cast_to=ShieldEntity, envelope=True),
        )

    @operation("_update_shield_shield__shield_uuid__put")
    def update(self, shield_uuid: str, body: ShieldUpsert) -> ShieldEntity:
        """Update an existing shield."""
        return cast(
            ShieldEntity,
            self._client.put(
                f"/shield/{shield_uuid}",
                json_body=body,
                cast_to=ShieldEntity,
                envelope=True,
            ),
        )

    @operation("_delete_shield_shield__shield_uuid__delete")
    def delete(self, shield_uuid: str) -> dict[str, Any]:
        """Delete a shield."""
        return cast(
            dict[str, Any],
            self._client.delete(f"/shield/{shield_uuid}", cast_to=dict, envelope=True),
        )

    @operation(
        "_attach_organization_to_shield_shield__shield_uuid__attach_organization__organization_uuid__post"
    )
    def attach_organization(self, shield_uuid: str, organization_uuid: str) -> bool:
        """Attach an organization to a shield."""
        return cast(
            bool,
            self._client.post(
                f"/shield/{shield_uuid}/attach/organization/{organization_uuid}",
                cast_to=bool,
                envelope=True,
            ),
        )

    @operation("_attach_agent_to_shield_shield__shield_uuid__attach_agent__agent_uuid__post")
    def attach_agent(self, shield_uuid: str, agent_uuid: str) -> bool:
        """Attach an agent to a shield."""
        return cast(
            bool,
            self._client.post(
                f"/shield/{shield_uuid}/attach/agent/{agent_uuid}",
                cast_to=bool,
                envelope=True,
            ),
        )

    @operation("_get_shield_for_organization_shield_organization__organization_uuid__get")
    def retrieve_for_organization(self, organization_uuid: str) -> ShieldEntity:
        """Get shield attached to an organization."""
        return cast(
            ShieldEntity,
            self._client.get(
                f"/shield/organization/{organization_uuid}",
                cast_to=ShieldEntity,
                envelope=True,
            ),
        )

    @operation("_get_shield_for_agent_shield_agent__agent_uuid__get")
    def retrieve_for_agent(self, agent_uuid: str) -> ShieldEntity:
        """Get shield attached to an agent."""
        return cast(
            ShieldEntity,
            self._client.get(
                f"/shield/agent/{agent_uuid}",
                cast_to=ShieldEntity,
                envelope=True,
            ),
        )


class AsyncShield(AsyncResource):
    """Async counterpart of `Shield`."""

    namespace: ClassVar[str] = "shield"

    @operation("_list_shields_shield__get")
    async def list(self) -> list[ShieldEntity]:
        """List all shields."""
        return cast(
            list[ShieldEntity],
            await self._client.get("/shield/", cast_to=list[ShieldEntity], envelope=True),
        )

    @operation("_create_shield_shield_post")
    async def create(self, body: ShieldUpsert) -> ShieldEntity:
        """Create a new shield."""
        return cast(
            ShieldEntity,
            await self._client.post("/shield", json_body=body, cast_to=ShieldEntity, envelope=True),
        )

    @operation("_get_shield_shield__shield_uuid__get")
    async def retrieve(self, shield_uuid: str) -> ShieldEntity:
        """Get shield by UUID."""
        return cast(
            ShieldEntity,
            await self._client.get(f"/shield/{shield_uuid}", cast_to=ShieldEntity, envelope=True),
        )

    @operation("_update_shield_shield__shield_uuid__put")
    async def update(self, shield_uuid: str, body: ShieldUpsert) -> ShieldEntity:
        """Update an existing shield."""
        return cast(
            ShieldEntity,
            await self._client.put(
                f"/shield/{shield_uuid}",
                json_body=body,
                cast_to=ShieldEntity,
                envelope=True,
            ),
        )

    @operation("_delete_shield_shield__shield_uuid__delete")
    async def delete(self, shield_uuid: str) -> dict[str, Any]:
        """Delete a shield."""
        return cast(
            dict[str, Any],
            await self._client.delete(f"/shield/{shield_uuid}", cast_to=dict, envelope=True),
        )

    @operation(
        "_attach_organization_to_shield_shield__shield_uuid__attach_organization__organization_uuid__post"
    )
    async def attach_organization(self, shield_uuid: str, organization_uuid: str) -> bool:
        """Attach an organization to a shield."""
        return cast(
            bool,
            await self._client.post(
                f"/shield/{shield_uuid}/attach/organization/{organization_uuid}",
                cast_to=bool,
                envelope=True,
            ),
        )

    @operation("_attach_agent_to_shield_shield__shield_uuid__attach_agent__agent_uuid__post")
    async def attach_agent(self, shield_uuid: str, agent_uuid: str) -> bool:
        """Attach an agent to a shield."""
        return cast(
            bool,
            await self._client.post(
                f"/shield/{shield_uuid}/attach/agent/{agent_uuid}",
                cast_to=bool,
                envelope=True,
            ),
        )

    @operation("_get_shield_for_organization_shield_organization__organization_uuid__get")
    async def retrieve_for_organization(self, organization_uuid: str) -> ShieldEntity:
        """Get shield attached to an organization."""
        return cast(
            ShieldEntity,
            await self._client.get(
                f"/shield/organization/{organization_uuid}",
                cast_to=ShieldEntity,
                envelope=True,
            ),
        )

    @operation("_get_shield_for_agent_shield_agent__agent_uuid__get")
    async def retrieve_for_agent(self, agent_uuid: str) -> ShieldEntity:
        """Get shield attached to an agent."""
        return cast(
            ShieldEntity,
            await self._client.get(
                f"/shield/agent/{agent_uuid}",
                cast_to=ShieldEntity,
                envelope=True,
            ),
        )


Galene._NAMESPACES.append(Shield)
AsyncGalene._NAMESPACES.append(AsyncShield)
