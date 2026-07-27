"""`observability` resource: traces, observations, read audits, and metrics.

Covers `/observability/*`: trace listing/retrieval, per-trace observations and
read-audit events (each with a CSV export sibling), plus the aggregate metrics
endpoints (overview, top agents/users/tools, model usage, guardrail filters,
shield token series, and RAG similarity).

Notes on shapes (all pre-computed in `.superpowers/sdd/impl/observability.json`):
- The list/observation/read-audit endpoints envelope their payload
  (`{success, message, result: [...]}`), so they decode with `envelope=True`
  and return plain `list[...]`. The spec marks them `offset`-paginated, which is
  surfaced here purely as `limit`/`offset` query kwargs — the envelope carries no
  `has_more`/cursor metadata to hang an `OffsetPage` off of, so the return type
  follows the directive's `envelope_list` kind (a bare list).
- The `.csv` export endpoints have an empty/untyped 200 schema in the spec, so
  they decode as `dict` per the directive's `empty` kind.
- Four of the GET endpoints additionally accept a small JSON body (`tags_any` /
  `tags_all` / `columns`); it is exposed as an optional `body:` model argument.
"""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    ActiveUsersDailyPoint,
    AuditItem,
    BodyExportObservationsObservabilityTracesTraceIdObservationsExportCsvGet,
    BodyExportTracesObservabilityTracesExportCsvGet,
    BodyGetTraceObservationsObservabilityTracesTraceIdObservationsGet,
    BodyGetTracesObservabilityTracesGet,
    FilterItem,
    MetricsOverview,
    ModelUsageItem,
    ObservationItem,
    RagSimilarityItem,
    ShieldSeriesPoint,
    ToolItem,
    TopItem,
    TraceItem,
)


class Observability(SyncResource):
    """Traces, observations, read audits, and aggregate metrics."""

    namespace: ClassVar[str] = "observability"

    @operation("get_traces_observability_traces_get")
    def list_traces(
        self,
        *,
        organization_id: str | None = None,
        conversation_id: str | None = None,
        status: str | None = None,
        name_q: str | None = None,
        user_id: str | None = None,
        metadata_contains: str | None = None,
        started_after: str | None = None,
        started_before: str | None = None,
        sort_dir: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        body: BodyGetTracesObservabilityTracesGet | None = None,
    ) -> list[TraceItem]:
        """List traces."""
        return cast(
            list[TraceItem],
            self._client.get(
                "/observability/traces",
                params={
                    "organization_id": organization_id,
                    "conversation_id": conversation_id,
                    "status": status,
                    "name_q": name_q,
                    "user_id": user_id,
                    "metadata_contains": metadata_contains,
                    "started_after": started_after,
                    "started_before": started_before,
                    "sort_dir": sort_dir,
                    "limit": limit,
                    "offset": offset,
                },
                json_body=body,
                cast_to=list[TraceItem],
                envelope=True,
            ),
        )

    @operation("export_traces_observability_traces_export_csv_get")
    def export_traces(
        self,
        *,
        organization_id: str | None = None,
        conversation_id: str | None = None,
        status: str | None = None,
        name_q: str | None = None,
        user_id: str | None = None,
        metadata_contains: str | None = None,
        started_after: str | None = None,
        started_before: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        columns: str | None = None,
        sort_dir: str | None = None,
        body: BodyExportTracesObservabilityTracesExportCsvGet | None = None,
    ) -> bytes:
        """Export traces as CSV."""
        return cast(
            bytes,
            self._client.get(
                "/observability/traces/export.csv",
                params={
                    "organization_id": organization_id,
                    "conversation_id": conversation_id,
                    "status": status,
                    "name_q": name_q,
                    "user_id": user_id,
                    "metadata_contains": metadata_contains,
                    "started_after": started_after,
                    "started_before": started_before,
                    "limit": limit,
                    "offset": offset,
                    "columns": columns,
                    "sort_dir": sort_dir,
                },
                json_body=body,
                cast_to=bytes,
            ),
        )

    @operation("get_trace_by_id_observability_traces__trace_id__get")
    def retrieve_trace(self, trace_id: str) -> TraceItem:
        """Get a single trace by ID."""
        return cast(
            TraceItem,
            self._client.get(f"/observability/traces/{trace_id}", cast_to=TraceItem, envelope=True),
        )

    @operation("get_trace_observations_observability_traces__trace_id__observations_get")
    def list_observations(
        self,
        trace_id: str,
        *,
        type_: str | None = None,
        status: str | None = None,
        name_q: str | None = None,
        parent_observation_id: str | None = None,
        metadata_contains: str | None = None,
        sort_dir: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        body: BodyGetTraceObservationsObservabilityTracesTraceIdObservationsGet | None = None,
    ) -> list[ObservationItem]:
        """List observations for a trace."""
        return cast(
            list[ObservationItem],
            self._client.get(
                f"/observability/traces/{trace_id}/observations",
                params={
                    "type_": type_,
                    "status": status,
                    "name_q": name_q,
                    "parent_observation_id": parent_observation_id,
                    "metadata_contains": metadata_contains,
                    "sort_dir": sort_dir,
                    "limit": limit,
                    "offset": offset,
                },
                json_body=body,
                cast_to=list[ObservationItem],
                envelope=True,
            ),
        )

    @operation("export_observations_observability_traces__trace_id__observations_export_csv_get")
    def export_observations(
        self,
        trace_id: str,
        *,
        type_: str | None = None,
        status: str | None = None,
        name_q: str | None = None,
        parent_observation_id: str | None = None,
        metadata_contains: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        columns: str | None = None,
        sort_dir: str | None = None,
        body: BodyExportObservationsObservabilityTracesTraceIdObservationsExportCsvGet
        | None = None,
    ) -> bytes:
        """Export observations for a trace as CSV."""
        return cast(
            bytes,
            self._client.get(
                f"/observability/traces/{trace_id}/observations/export.csv",
                params={
                    "type_": type_,
                    "status": status,
                    "name_q": name_q,
                    "parent_observation_id": parent_observation_id,
                    "metadata_contains": metadata_contains,
                    "limit": limit,
                    "offset": offset,
                    "columns": columns,
                    "sort_dir": sort_dir,
                },
                json_body=body,
                cast_to=bytes,
            ),
        )

    @operation("post_trace_read_observability_traces__trace_id__reads_post")
    def create_read(self, trace_id: str) -> bool:
        """Audit a trace read (sensitive content viewed)."""
        return cast(
            bool,
            self._client.post(
                f"/observability/traces/{trace_id}/reads", cast_to=bool, envelope=True
            ),
        )

    @operation("get_trace_reads_observability_traces__trace_id__reads_get")
    def list_reads(
        self,
        trace_id: str,
        *,
        user_id: str | None = None,
        read_after: str | None = None,
        read_before: str | None = None,
        sort_dir: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[AuditItem]:
        """List audit events for a trace read."""
        return cast(
            list[AuditItem],
            self._client.get(
                f"/observability/traces/{trace_id}/reads",
                params={
                    "user_id": user_id,
                    "read_after": read_after,
                    "read_before": read_before,
                    "sort_dir": sort_dir,
                    "limit": limit,
                    "offset": offset,
                },
                cast_to=list[AuditItem],
                envelope=True,
            ),
        )

    @operation("export_reads_observability_traces__trace_id__reads_export_csv_get")
    def export_reads(
        self,
        trace_id: str,
        *,
        user_id: str | None = None,
        read_after: str | None = None,
        read_before: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_dir: str | None = None,
    ) -> bytes:
        """Export trace read audit as CSV."""
        return cast(
            bytes,
            self._client.get(
                f"/observability/traces/{trace_id}/reads/export.csv",
                params={
                    "user_id": user_id,
                    "read_after": read_after,
                    "read_before": read_before,
                    "limit": limit,
                    "offset": offset,
                    "sort_dir": sort_dir,
                },
                cast_to=bytes,
            ),
        )

    @operation("metrics_overview_observability_metrics_overview_get")
    def metrics_overview(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
    ) -> MetricsOverview:
        """Metrics overview."""
        return cast(
            MetricsOverview,
            self._client.get(
                "/observability/metrics/overview",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                },
                cast_to=MetricsOverview,
            ),
        )

    @operation("top_agents_observability_metrics_agents_get")
    def top_agents(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        order: str | None = None,
        limit: int | None = None,
    ) -> list[TopItem]:
        """Top agents by usage."""
        return cast(
            list[TopItem],
            self._client.get(
                "/observability/metrics/agents",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "order": order,
                    "limit": limit,
                },
                cast_to=list[TopItem],
            ),
        )

    @operation("top_users_observability_metrics_users_get")
    def top_users(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[TopItem]:
        """Top users by usage."""
        return cast(
            list[TopItem],
            self._client.get(
                "/observability/metrics/users",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "limit": limit,
                },
                cast_to=list[TopItem],
            ),
        )

    @operation("top_tools_observability_metrics_tools_get")
    def top_tools(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[ToolItem]:
        """Top tools by usage."""
        return cast(
            list[ToolItem],
            self._client.get(
                "/observability/metrics/tools",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "limit": limit,
                },
                cast_to=list[ToolItem],
            ),
        )

    @operation("models_usage_observability_metrics_models_get")
    def models_usage(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[ModelUsageItem]:
        """Model usage breakdown."""
        return cast(
            list[ModelUsageItem],
            self._client.get(
                "/observability/metrics/models",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "limit": limit,
                },
                cast_to=list[ModelUsageItem],
            ),
        )

    @operation("guardrail_filters_observability_metrics_guardrail_filters_get")
    def guardrail_filters(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[FilterItem]:
        """Guardrail filter hits."""
        return cast(
            list[FilterItem],
            self._client.get(
                "/observability/metrics/guardrail/filters",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "limit": limit,
                },
                cast_to=list[FilterItem],
            ),
        )

    @operation("shield_tokens_daily_observability_metrics_shield_tokens_daily_get")
    def shield_tokens_daily(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
    ) -> list[ShieldSeriesPoint]:
        """Shield tokens daily series."""
        return cast(
            list[ShieldSeriesPoint],
            self._client.get(
                "/observability/metrics/shield/tokens_daily",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                },
                cast_to=list[ShieldSeriesPoint],
            ),
        )

    @operation("active_users_daily_observability_metrics_active_users_daily_get")
    def active_users_daily(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
    ) -> list[ActiveUsersDailyPoint]:
        """Daily active users (one point per UTC day, ascending).

        Pass an explicit `from_ts`/`to_ts` window: verified live, this backend
        (like the sibling daily-series metrics) returns HTTP 500 when the time
        window is omitted, even though the spec marks both bounds optional.
        """
        return cast(
            list[ActiveUsersDailyPoint],
            self._client.get(
                "/observability/metrics/active-users-daily",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                },
                cast_to=list[ActiveUsersDailyPoint],
            ),
        )

    @operation("rag_similarity_observability_metrics_rag_similarity_get")
    def rag_similarity(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
    ) -> list[RagSimilarityItem]:
        """RAG retrieval similarity."""
        return cast(
            list[RagSimilarityItem],
            self._client.get(
                "/observability/metrics/rag/similarity",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                },
                cast_to=list[RagSimilarityItem],
            ),
        )


class AsyncObservability(AsyncResource):
    """Async counterpart of `Observability`."""

    namespace: ClassVar[str] = "observability"

    @operation("get_traces_observability_traces_get")
    async def list_traces(
        self,
        *,
        organization_id: str | None = None,
        conversation_id: str | None = None,
        status: str | None = None,
        name_q: str | None = None,
        user_id: str | None = None,
        metadata_contains: str | None = None,
        started_after: str | None = None,
        started_before: str | None = None,
        sort_dir: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        body: BodyGetTracesObservabilityTracesGet | None = None,
    ) -> list[TraceItem]:
        """List traces."""
        return cast(
            list[TraceItem],
            await self._client.get(
                "/observability/traces",
                params={
                    "organization_id": organization_id,
                    "conversation_id": conversation_id,
                    "status": status,
                    "name_q": name_q,
                    "user_id": user_id,
                    "metadata_contains": metadata_contains,
                    "started_after": started_after,
                    "started_before": started_before,
                    "sort_dir": sort_dir,
                    "limit": limit,
                    "offset": offset,
                },
                json_body=body,
                cast_to=list[TraceItem],
                envelope=True,
            ),
        )

    @operation("export_traces_observability_traces_export_csv_get")
    async def export_traces(
        self,
        *,
        organization_id: str | None = None,
        conversation_id: str | None = None,
        status: str | None = None,
        name_q: str | None = None,
        user_id: str | None = None,
        metadata_contains: str | None = None,
        started_after: str | None = None,
        started_before: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        columns: str | None = None,
        sort_dir: str | None = None,
        body: BodyExportTracesObservabilityTracesExportCsvGet | None = None,
    ) -> bytes:
        """Export traces as CSV."""
        return cast(
            bytes,
            await self._client.get(
                "/observability/traces/export.csv",
                params={
                    "organization_id": organization_id,
                    "conversation_id": conversation_id,
                    "status": status,
                    "name_q": name_q,
                    "user_id": user_id,
                    "metadata_contains": metadata_contains,
                    "started_after": started_after,
                    "started_before": started_before,
                    "limit": limit,
                    "offset": offset,
                    "columns": columns,
                    "sort_dir": sort_dir,
                },
                json_body=body,
                cast_to=bytes,
            ),
        )

    @operation("get_trace_by_id_observability_traces__trace_id__get")
    async def retrieve_trace(self, trace_id: str) -> TraceItem:
        """Get a single trace by ID."""
        return cast(
            TraceItem,
            await self._client.get(
                f"/observability/traces/{trace_id}", cast_to=TraceItem, envelope=True
            ),
        )

    @operation("get_trace_observations_observability_traces__trace_id__observations_get")
    async def list_observations(
        self,
        trace_id: str,
        *,
        type_: str | None = None,
        status: str | None = None,
        name_q: str | None = None,
        parent_observation_id: str | None = None,
        metadata_contains: str | None = None,
        sort_dir: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        body: BodyGetTraceObservationsObservabilityTracesTraceIdObservationsGet | None = None,
    ) -> list[ObservationItem]:
        """List observations for a trace."""
        return cast(
            list[ObservationItem],
            await self._client.get(
                f"/observability/traces/{trace_id}/observations",
                params={
                    "type_": type_,
                    "status": status,
                    "name_q": name_q,
                    "parent_observation_id": parent_observation_id,
                    "metadata_contains": metadata_contains,
                    "sort_dir": sort_dir,
                    "limit": limit,
                    "offset": offset,
                },
                json_body=body,
                cast_to=list[ObservationItem],
                envelope=True,
            ),
        )

    @operation("export_observations_observability_traces__trace_id__observations_export_csv_get")
    async def export_observations(
        self,
        trace_id: str,
        *,
        type_: str | None = None,
        status: str | None = None,
        name_q: str | None = None,
        parent_observation_id: str | None = None,
        metadata_contains: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        columns: str | None = None,
        sort_dir: str | None = None,
        body: BodyExportObservationsObservabilityTracesTraceIdObservationsExportCsvGet
        | None = None,
    ) -> bytes:
        """Export observations for a trace as CSV."""
        return cast(
            bytes,
            await self._client.get(
                f"/observability/traces/{trace_id}/observations/export.csv",
                params={
                    "type_": type_,
                    "status": status,
                    "name_q": name_q,
                    "parent_observation_id": parent_observation_id,
                    "metadata_contains": metadata_contains,
                    "limit": limit,
                    "offset": offset,
                    "columns": columns,
                    "sort_dir": sort_dir,
                },
                json_body=body,
                cast_to=bytes,
            ),
        )

    @operation("post_trace_read_observability_traces__trace_id__reads_post")
    async def create_read(self, trace_id: str) -> bool:
        """Audit a trace read (sensitive content viewed)."""
        return cast(
            bool,
            await self._client.post(
                f"/observability/traces/{trace_id}/reads", cast_to=bool, envelope=True
            ),
        )

    @operation("get_trace_reads_observability_traces__trace_id__reads_get")
    async def list_reads(
        self,
        trace_id: str,
        *,
        user_id: str | None = None,
        read_after: str | None = None,
        read_before: str | None = None,
        sort_dir: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[AuditItem]:
        """List audit events for a trace read."""
        return cast(
            list[AuditItem],
            await self._client.get(
                f"/observability/traces/{trace_id}/reads",
                params={
                    "user_id": user_id,
                    "read_after": read_after,
                    "read_before": read_before,
                    "sort_dir": sort_dir,
                    "limit": limit,
                    "offset": offset,
                },
                cast_to=list[AuditItem],
                envelope=True,
            ),
        )

    @operation("export_reads_observability_traces__trace_id__reads_export_csv_get")
    async def export_reads(
        self,
        trace_id: str,
        *,
        user_id: str | None = None,
        read_after: str | None = None,
        read_before: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_dir: str | None = None,
    ) -> bytes:
        """Export trace read audit as CSV."""
        return cast(
            bytes,
            await self._client.get(
                f"/observability/traces/{trace_id}/reads/export.csv",
                params={
                    "user_id": user_id,
                    "read_after": read_after,
                    "read_before": read_before,
                    "limit": limit,
                    "offset": offset,
                    "sort_dir": sort_dir,
                },
                cast_to=bytes,
            ),
        )

    @operation("metrics_overview_observability_metrics_overview_get")
    async def metrics_overview(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
    ) -> MetricsOverview:
        """Metrics overview."""
        return cast(
            MetricsOverview,
            await self._client.get(
                "/observability/metrics/overview",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                },
                cast_to=MetricsOverview,
            ),
        )

    @operation("top_agents_observability_metrics_agents_get")
    async def top_agents(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        order: str | None = None,
        limit: int | None = None,
    ) -> list[TopItem]:
        """Top agents by usage."""
        return cast(
            list[TopItem],
            await self._client.get(
                "/observability/metrics/agents",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "order": order,
                    "limit": limit,
                },
                cast_to=list[TopItem],
            ),
        )

    @operation("top_users_observability_metrics_users_get")
    async def top_users(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[TopItem]:
        """Top users by usage."""
        return cast(
            list[TopItem],
            await self._client.get(
                "/observability/metrics/users",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "limit": limit,
                },
                cast_to=list[TopItem],
            ),
        )

    @operation("top_tools_observability_metrics_tools_get")
    async def top_tools(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[ToolItem]:
        """Top tools by usage."""
        return cast(
            list[ToolItem],
            await self._client.get(
                "/observability/metrics/tools",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "limit": limit,
                },
                cast_to=list[ToolItem],
            ),
        )

    @operation("models_usage_observability_metrics_models_get")
    async def models_usage(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[ModelUsageItem]:
        """Model usage breakdown."""
        return cast(
            list[ModelUsageItem],
            await self._client.get(
                "/observability/metrics/models",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "limit": limit,
                },
                cast_to=list[ModelUsageItem],
            ),
        )

    @operation("guardrail_filters_observability_metrics_guardrail_filters_get")
    async def guardrail_filters(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
        limit: int | None = None,
    ) -> list[FilterItem]:
        """Guardrail filter hits."""
        return cast(
            list[FilterItem],
            await self._client.get(
                "/observability/metrics/guardrail/filters",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "limit": limit,
                },
                cast_to=list[FilterItem],
            ),
        )

    @operation("shield_tokens_daily_observability_metrics_shield_tokens_daily_get")
    async def shield_tokens_daily(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
    ) -> list[ShieldSeriesPoint]:
        """Shield tokens daily series."""
        return cast(
            list[ShieldSeriesPoint],
            await self._client.get(
                "/observability/metrics/shield/tokens_daily",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                },
                cast_to=list[ShieldSeriesPoint],
            ),
        )

    @operation("active_users_daily_observability_metrics_active_users_daily_get")
    async def active_users_daily(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
    ) -> list[ActiveUsersDailyPoint]:
        """Daily active users (one point per UTC day, ascending).

        Pass an explicit `from_ts`/`to_ts` window: verified live, this backend
        (like the sibling daily-series metrics) returns HTTP 500 when the time
        window is omitted, even though the spec marks both bounds optional.
        """
        return cast(
            list[ActiveUsersDailyPoint],
            await self._client.get(
                "/observability/metrics/active-users-daily",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                },
                cast_to=list[ActiveUsersDailyPoint],
            ),
        )

    @operation("rag_similarity_observability_metrics_rag_similarity_get")
    async def rag_similarity(
        self,
        *,
        organization_id: str,
        from_ts: str | None = None,
        to_ts: str | None = None,
    ) -> list[RagSimilarityItem]:
        """RAG retrieval similarity."""
        return cast(
            list[RagSimilarityItem],
            await self._client.get(
                "/observability/metrics/rag/similarity",
                params={
                    "organization_id": organization_id,
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                },
                cast_to=list[RagSimilarityItem],
            ),
        )


Galene._NAMESPACES.append(Observability)
AsyncGalene._NAMESPACES.append(AsyncObservability)
