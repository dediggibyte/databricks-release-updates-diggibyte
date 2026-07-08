# Incremental refresh for materialized views in Databricks SQL

> date: 2026-06-02

Databricks SQL materialized views now support incremental refresh in Public
Preview. Instead of recomputing the entire result set on every refresh, the
engine detects changes in base tables and updates only the affected rows,
dramatically reducing refresh cost and latency for large aggregations.

Highlights:

- Incremental refresh for a broad set of SQL constructs including joins and
  aggregations.
- Automatic fallback to full refresh when incremental is not possible.
- Refresh scheduling and monitoring in the SQL editor.

Prerequisites:

- A SQL warehouse on the current channel.
- Base tables stored in Delta with change data feed available.

Limitations:

- Some non-deterministic functions force a full refresh.
- Incremental refresh statistics are not yet exposed in system tables.

Recommended for BI dashboards, pre-aggregated reporting tables, and cost-
sensitive scheduled refreshes. To use it, create a materialized view over
Delta base tables, enable change data feed, and schedule an incremental
refresh.
