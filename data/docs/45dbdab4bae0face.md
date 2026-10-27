Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To use it, a workspace admin must turn on **Lakeflow Connect for Zoho CRM** from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

The managed Zoho CRM connector in Lakeflow Connect ingests CRM data such as leads, contacts, accounts, deals, and activities, plus custom modules from Zoho CRM into Databricks.

## Feature availability

| Feature | Availability |
| --- | --- |
| UI-based pipeline authoring | Not supported |
| API-based pipeline authoring | Supported |
| Declarative Automation Bundles | Supported |
| Incremental ingestion | Supported |
| Unity Catalog governance | Supported |
| Orchestration using Databricks Lakeflow Jobs | Supported |
| API-based column selection and deselection | Supported |
| API-based row filtering | Not supported |
| SCD Type 2 | Supported  Tables with VARIANT columns (module tables, custom module tables, item tables, `users`, and `territories`) don't support SCD type 2. |
| Automated schema evolution: New and deleted columns | Supported |
| Automated schema evolution: Data type changes | Not supported |
| Automated schema evolution: Column renames | Not supported  Requires a full refresh. |

←✕

| Feature | Availability |
| --- | --- |
| UI-based pipeline authoring | Not supported |
| API-based pipeline authoring | Supported |
| Declarative Automation Bundles | Supported |
| Incremental ingestion | Supported |
| Unity Catalog governance | Supported |
| Orchestration using Databricks Lakeflow Jobs | Supported |
| API-based column selection and deselection | Supported |
| API-based row filtering | Not supported |
| SCD Type 2 | Supported  Tables with VARIANT columns (module tables, custom module tables, item tables, `users`, and `territories`) don't support SCD type 2. |
| Automated schema evolution: New and deleted columns | Supported |
| Automated schema evolution: Data type changes | Not supported |
| Automated schema evolution: Column renames | Not supported  Requires a full refresh. |

## Authentication methods

| Authentication method | Availability |
| --- | --- |
| OAuth U2M | Not supported |
| OAuth M2M (OAuth Client Credentials) | Supported |
| Basic authentication (username/password) | Not supported |

←✕

| Authentication method | Availability |
| --- | --- |
| OAuth U2M | Not supported |
| OAuth M2M (OAuth Client Credentials) | Supported |
| Basic authentication (username/password) | Not supported |

## Ingest from Zoho CRM in 3 steps

note

Before starting, review the [Databricks user persona](/aws/en/connect/managed-ingestion), [supported interfaces](/aws/en/ingestion/lakeflow-connect/faq#interfaces), [ingestion frequency](/aws/en/ldp/concepts/pipeline-mode), and [common patterns](/aws/en/ingestion/lakeflow-connect/common-patterns).

1. **[Configure Zoho CRM for ingestion](/aws/en/ingestion/lakeflow-connect/zoho-crm-source-setup)** (Admins): Set up Zoho CRM to authenticate with Databricks.
2. **[Create a Unity Catalog connection](/aws/en/ingestion/lakeflow-connect/zoho-crm-connection)** (Admins): Create a connection in Catalog Explorer so non-admins can create pipelines.
3. **[Create an ingestion pipeline](/aws/en/ingestion/lakeflow-connect/zoho-crm-pipeline)** (Admins or non-admins): Select any supported interface and create a pipeline from an existing connection.