On this page

Last updated on **Jun 5, 2026**

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). Workspace admins can control access to this feature from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

The managed SharePoint connector in Lakeflow Connect allows you to ingest files from SharePoint into Databricks. Ingest unstructured files as binary data, parse structured formats (`CSV`, `JSON`, `XML`, `EXCEL`, and more) into Delta tables, or capture file metadata without loading file contents.

## Feature availability[​](#feature-availability "Direct link to Feature availability")

| Feature | Availability |
| --- | --- |
| UI-based pipeline authoring | Not supported |
| API-based pipeline authoring | Supported |
| Declarative Automation Bundles | Supported |
| Incremental ingestion | Supported |
| Unity Catalog governance | Supported |
| Orchestration using Databricks Workflows | Supported |
| SCD type 2 | Not supported |
| Schema evolution | Supported  Configurable via `schema_evolution_mode`. See [Microsoft SharePoint connector reference](/aws/en/ingestion/lakeflow-connect/sharepoint-reference). |
| API-based column selection and deselection | Not supported |
| API-based row filtering | Not supported |

## Authentication methods[​](#authentication-methods "Direct link to Authentication methods")

| Authentication method | Availability |
| --- | --- |
| OAuth U2M | Supported |
| OAuth M2M | Supported |
| OAuth (manual refresh token) | Supported |
| Basic authentication (username/password) | Not supported |
| Basic authentication (API key) | Not supported |
| Basic authentication (service account JSON key) | Not supported |

## What to know before you start[​](#what-to-know-before-you-start "Direct link to What to know before you start")

| Topic | Why it matters |
| --- | --- |
| [Databricks user persona](/aws/en/connect/managed-ingestion) | The workflow depends on your Databricks user persona:   * Single-user: An admin user creates a Unity Catalog connection and an ingestion pipeline. * Multi-user: An admin user creates a connection for non-admin users to create pipelines with. |
| [Authentication method](#authentication-methods) | The steps to create a connection depend on the authentication method you choose. |
| [Interface](/aws/en/ingestion/lakeflow-connect/faq) | The steps to create a pipeline depend on the interface. |
| [Ingestion frequency](/aws/en/ldp/pipeline-mode) | The pipeline schedule depends on your latency and cost requirements. |
| [Common patterns](/aws/en/ingestion/lakeflow-connect/common-patterns) | Depending on your ingestion needs, the pipeline might use configurations like history tracking, column selection, and row filtering. Supported configurations vary by connector. See [Feature availability](#feature-availability). |

## Start ingesting from SharePoint[​](#start-ingesting-from-sharepoint "Direct link to Start ingesting from SharePoint")

The following table provides an overview of the end-to-end SharePoint ingestion flow, based on user type:

| User | Steps |
| --- | --- |
| Admin | 1. Configure SharePoint authentication. See [Overview of SharePoint ingestion setup](/aws/en/ingestion/lakeflow-connect/sharepoint-source-setup-overview). 2. Use Catalog Explorer to create a connection to SharePoint so that non-admins can create pipelines. See [Create a SharePoint connection](/aws/en/ingestion/lakeflow-connect/sharepoint-connection). |
| Non-admin | Use any supported interface to create a pipeline from an existing connection. See [Ingest data from SharePoint](/aws/en/ingestion/lakeflow-connect/sharepoint-pipeline). |