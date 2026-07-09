On this page

Last updated on **Jul 1, 2026**

important

Databricks highly discourages you from moving this data outside the platform because it can expose sensitive data and put your deployment at risk. Due to the nature of system table information, you are reminded that you are responsible to maintain the security, and prevent misuse, of any exported system table information.

System tables provide a Databricks-hosted analytical store of your account's operational data. Use them to monitor costs, audit security events, track compute and job performance, and observe data and AI workloads.

## What are system tables?[​](#what-are-system-tables "Direct link to What are system tables?")

System tables are a Databricks-hosted analytical store of your account's operational data found in the `system` catalog. System tables can be used for historical observability across your account.

note

The information schema tables (`system.information_schema`) work differently from other system tables. See [Information schema](/aws/en/sql/language-manual/sql-ref-information-schema).

## Requirements[​](#requirements "Direct link to Requirements")

* To access system tables, your workspace must be enabled for Unity Catalog. For more information, see [Enable system tables](#enable).

* Only a subset of system tables are available in Databricks on AWS GovCloud. See [Supported system tables](/aws/en/security/privacy/gov-cloud#system-tables).

## Which system tables are available?[​](#which-system-tables-are-available "Direct link to which-system-tables-are-available")

Currently, Databricks hosts the following system tables:

| Table | Description | Supports streaming | Free retention period | Includes global or regional data |
| --- | --- | --- | --- | --- |
| [Audit logs](/aws/en/admin/system-tables/audit-logs) (Public Preview) | Includes records for all audit events from workspaces in your region. For a list of available audit events, see [Audit log reference](/aws/en/admin/account-settings/audit-logs).  **Table path**: `system.access.audit` | Yes | 365 days | Regional for workspace-level events. Global for account-level events. |
| [Billable usage](/aws/en/admin/system-tables/billing) | Includes records for all billable usage across your account.  **Table path**: `system.billing.usage` | Yes | 365 days | Global |
| [Clean room events](/aws/en/admin/system-tables/clean-rooms) (Public Preview) | Captures events related to clean rooms.  **Table path**: `system.access.clean_room_events` | Yes | 365 days | Regional |
| [Clusters](/aws/en/admin/system-tables/compute) | A slow-changing dimension table that contains the full history of compute configurations over time for any cluster. | Yes | 365 days | Regional |
| [Column lineage](/aws/en/admin/system-tables/lineage) | Includes a record for each read or write event on a Unity Catalog column (but does not include events that do not have a source).  **Table path**: `system.access.column_lineage` | Yes | 365 days | Regional |
| [Data classification results](/aws/en/admin/system-tables/data-classification) (Public Preview) | Stores column-level detections of sensitive data classes across enabled catalogs in your metastore.  **Table path**: `system.data_classification.results` | No | 13 months | Regional |
| [Data quality monitoring results](/aws/en/admin/system-tables/data-quality-monitoring) (Public Preview) | Stores results of data quality monitoring checks (freshness, completeness) and incident information, including downstream impact and root cause analysis, across enabled tables in your metastore.  **Table path**: `system.data_quality_monitoring.table_results` | No | Indefinite | Regional |
| [Genie Code events](/aws/en/admin/system-tables/assistant) (Public Preview) | Tracks user messages sent to the Genie Code.  **Table path**: `system.access.assistant_events` | No | 365 days | Regional |
| [AI Gateway usage](/aws/en/ai-gateway/usage-tracking) (Beta) | Captures request and response details for AI Gateway endpoints including token usage, latency, performance metrics, and routing information.  **Table path**: `system.ai_gateway.usage` | Yes | 365 days | Regional |
| [OpenSharing data materialization events](/aws/en/admin/system-tables/materialization) | Captures data materialization events created from view, materialized view, and streaming table sharing.  **Table path**: `system.sharing.materialization_history` | Yes | 365 days | Regional for workspace-level events. |
| [Instance events](/aws/en/admin/system-tables/compute#instance-events) (Public Preview) | Captures state transitions of classic compute instances.  **Table path**: `system.compute.instance_events` | Yes | 365 days | Regional |
| [Instance pools](/aws/en/admin/system-tables/compute#instance-pools) (Public Preview) | A slow-changing dimension table that contains the full history of instance pool configurations over time.  **Table path**: `system.compute.instance_pools` | Yes | 365 days | Regional |
| [Job run timeline](/aws/en/admin/system-tables/jobs#runs) | Tracks the start and end times of job runs.  **Table path**: `system.lakeflow.job_run_timeline` | Yes | 365 days | Regional |
| [Job task timeline](/aws/en/admin/system-tables/jobs#task-timeline) | Tracks the start and end times and compute resources used for job task runs.  **Table path**: `system.lakeflow.job_task_run_timeline` | Yes | 365 days | Regional |
| [Job tasks](/aws/en/admin/system-tables/jobs#job-tasks) | Tracks all job tasks that run in the account.  **Table path**: `system.lakeflow.job_tasks` | Yes | 365 days | Regional |
| [Jobs](/aws/en/admin/system-tables/jobs#jobs) | Tracks all jobs created in the account.  **Table path**: `system.lakeflow.jobs` | Yes | 365 days | Regional |
| [Marketplace funnel events](/aws/en/admin/system-tables/marketplace#funnel) (Public Preview) | Includes consumer impression and funnel data for your listings.  **Table path**: `system.marketplace.listing_funnel_events` | Yes | 365 days | Regional |
| [Marketplace listing access](/aws/en/admin/system-tables/marketplace#access) (Public Preview) | Includes consumer info for completed *request data* or *get data* events on your listings.  **Table path**: `system.marketplace.listing_access_events` | Yes | 365 days | Regional |
| [MLflow tracking experiment metadata](/aws/en/admin/system-tables/mlflow) (Public Preview) | Each row represents an experiment created in the Databricks-managed MLflow system.  **Table path**: `system.mlflow.experiments_latest` | Yes | 180 days | Regional |
| [MLflow tracking run metadata](/aws/en/admin/system-tables/mlflow) (Public Preview) | Each row represents a run created in the Databricks-managed MLflow system.  **Table path**: `system.mlflow.runs_latest` | Yes | 180 days | Regional |
| [MLflow tracking run metrics](/aws/en/admin/system-tables/mlflow) (Public Preview) | Holds the timeseries metrics logged to MLflow associated with a given model training, evaluation, or agent development.  **Table path**: `system.mlflow.run_metrics_history` | Yes | 180 days | Regional |
| [Model serving endpoint data](/aws/en/ai-gateway/configure-ai-gateway-endpoints#usage-schema) (Public Preview) | A slow-changing dimension table that stores metadata for each served foundation model in a model serving endpoint.  **Table path**: `system.serving.served_entities` | Yes | 365 days | Regional |
| [Model serving endpoint usage](/aws/en/ai-gateway/configure-ai-gateway-endpoints#usage-schema) (Public Preview) | Captures token counts for each request to a model serving endpoint and its responses. To capture the endpoint usage in this table, you must [enable usage tracking on your serving endpoint](/aws/en/ai-gateway/configure-ai-gateway-endpoints#configure).  **Table path**: `system.serving.endpoint_usage` | Yes | 90 days | Regional |
| [Network access events (Inbound)](/aws/en/admin/system-tables/network#inbound) (Public Preview) | A table that records an event for every time inbound access to a workspace is denied by an ingress policy.  **Table path**: `system.access.inbound_network` | Yes | 30 days | Regional |
| [Network access events (Outbound)](/aws/en/admin/system-tables/network#outbound) (Public Preview) | A table that records an event every time outbound internet access is denied from your account.  **Table path**: `system.access.outbound_network` | Yes | 365 days | Regional |
| [Node timeline](/aws/en/admin/system-tables/compute#node-timeline) | Captures the utilization metrics of your all-purpose and jobs compute resources.  **Table path**: `system.compute.node_timeline` | Yes | 90 days | Regional |
| [Node types](/aws/en/admin/system-tables/compute#node-types) | Captures the currently available node types with their basic hardware information.  **Table path**: `system.compute.node_types` | No | Indefinite | Regional |
| [Pipeline update timeline](/aws/en/admin/system-tables/jobs#pipeline-update-timeline) (Public Preview) | Tracks the start and end times and compute resources used for pipeline updates.  **Table path**: `system.lakeflow.pipeline_update_timeline` | Yes | 365 days | Regional |
| [Pipelines](/aws/en/admin/system-tables/jobs#pipelines) (Public Preview) | Tracks all pipelines created in the account.  **Table path**: `system.lakeflow.pipelines` | Yes | 365 days | Regional |
| [Predictive optimization](/aws/en/admin/system-tables/predictive-optimization) (Public Preview) | Tracks the operation history of the predictive optimization feature.  **Table path**: `system.storage.predictive_optimization_operations_history` | No | 180 days | Regional |
| [Pricing](/aws/en/admin/system-tables/pricing) | A historical log of SKU pricing. A record gets added each time there is a change to a SKU price.  **Table path**: `system.billing.list_prices` | No | Indefinite | Global |
| [Query history](/aws/en/admin/system-tables/query-history) (Public Preview) | Captures records for all queries run on SQL warehouses and serverless compute for [notebooks](/aws/en/compute/serverless/notebooks) and [jobs](/aws/en/jobs/run-serverless-jobs).  **Table path**: `system.query.history` | No | 365 days | Regional |
| [Replication](/aws/en/admin/system-tables/replication) (Private Preview) | Tracks replication status for Databricks managed disaster recovery (DR).  **Table path**: `system.replication.states` | Yes | 365 days | Global |
| [SQL warehouse events](/aws/en/admin/system-tables/warehouse-events) | Captures events related to SQL warehouses. For example, starting, stopping, running, scaling up and down.  **Table path**: `system.compute.warehouse_events` | Yes | 365 days | Regional |
| [SQL warehouses](/aws/en/admin/system-tables/warehouses) | Contains the full history of configurations over time for any SQL warehouse.  **Table path**: `system.compute.warehouses` | Yes | 365 days | Regional |
| [Table lineage](/aws/en/admin/system-tables/lineage) | Includes a record for each read or write event on a Unity Catalog table or path.  **Table path**: `system.access.table_lineage` | Yes | 365 days | Regional |
| [Workspaces](/aws/en/admin/system-tables/workspaces) (Public Preview) | The workspaces\_latest table is a slow-changing dimension table of metadata for all the workspaces in the account.  **Table path**: `system.access.workspaces_latest` | No | Indefinite | Global |
| [Zerobus Ingest (Streams)](/aws/en/admin/system-tables/zerobus-ingest#zerobus-stream) (Beta) | A table that stores all data related to stream events incurred by Zerobus Ingest usage.  **Table path**: `system.lakeflow.zerobus_stream` | Yes | 365 days | Regional |
| [Zerobus Ingest (Ingestion)](/aws/en/admin/system-tables/zerobus-ingest#zerobus-ingest) (Beta) | A table that stores all data related to records ingested using Zerobus Ingest.  **Table path**: `system.lakeflow.zerobus_ingest` | Yes | 365 days | Regional |

The billable usage and pricing tables are free to use. Tables in Public Preview are also free to use during the preview, but could incur a charge in the future.

note

You may see other system tables in your account, in addition to the ones listed above. Those tables are currently in Private Preview and are empty by default. If you are interested in using any of these tables, please reach out to your Databricks account team.

## System tables relationships[​](#system-tables-relationships "Direct link to system-tables-relationships")

The following entity-relationship diagram outlines how the currently available system tables relate to one another. This diagram highlights the primary and foreign keys of each table.

## Enable system tables[​](#enable-system-tables "Direct link to enable-system-tables")

Because system tables are governed by Unity Catalog, you need to have at least one Unity Catalog-enabled workspace in your account to enable your account's system tables. System tables include data from all workspaces in your account, but they can only be accessed from a Unity Catalog-enabled workspace.

The metastore needs to be on Unity Catalog Privilege Model Version 1.0 to access system tables. See [Upgrade to privilege inheritance](/aws/en/archive/unity-catalog/upgrade-privilege-model).

## Grant access to system tables[​](#grant-access-to-system-tables "Direct link to grant-access-to-system-tables")

Access to system tables is governed by Unity Catalog. Users with both the account admin and metastore admin roles have access to system tables by default. To allow other users to query system tables, the admin must grant users the following permissions: `USE CATALOG` on the system catalog, `USE SCHEMA` on the system schemas, and `SELECT` on the system schemas. See [Manage privileges in Unity Catalog](/aws/en/data-governance/unity-catalog/manage-privileges/).

System tables are read-only and cannot be modified.

note

If your account was created after November 8, 2023, you might not have a metastore admin by default. For more information, see [Get started with Unity Catalog](/aws/en/data-governance/unity-catalog/get-star