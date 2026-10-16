Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To use it, a workspace admin must turn on **Lakeflow Connect for SurveyMonkey** from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

The managed SurveyMonkey connector in Lakeflow Connect ingests surveys, survey structure, collectors, survey responses, and contacts from SurveyMonkey into Databricks.

## Feature availability

| Feature | Availability |
| --- | --- |
| UI-based pipeline authoring | Supported |
| API-based pipeline authoring | Supported |
| Declarative Automation Bundles | Supported |
| Incremental ingestion | Supported |
| Unity Catalog governance | Supported |
| Orchestration using Lakeflow Jobs | Supported |
| API-based column selection and deselection | Supported |
| API-based row filtering | Not supported |
| Slowly changing dimension (SCD) type 2 | Supported  Tables with VARIANT columns (`surveys`, `collectors`, `survey_responses`, `contact_list_contacts`, `collector_recipients`) do not support SCD type 2. |
| Automated schema evolution: New and deleted columns | Supported |
| Automated schema evolution: Data type changes | Not supported |
| Automated schema evolution: Column renames | Not supported  Requires a full refresh. |

←✕

| Feature | Availability |
| --- | --- |
| UI-based pipeline authoring | Supported |
| API-based pipeline authoring | Supported |
| Declarative Automation Bundles | Supported |
| Incremental ingestion | Supported |
| Unity Catalog governance | Supported |
| Orchestration using Lakeflow Jobs | Supported |
| API-based column selection and deselection | Supported |
| API-based row filtering | Not supported |
| Slowly changing dimension (SCD) type 2 | Supported  Tables with VARIANT columns (`surveys`, `collectors`, `survey_responses`, `contact_list_contacts`, `collector_recipients`) do not support SCD type 2. |
| Automated schema evolution: New and deleted columns | Supported |
| Automated schema evolution: Data type changes | Not supported |
| Automated schema evolution: Column renames | Not supported  Requires a full refresh. |

## Authentication methods

| Authentication method | Availability |
| --- | --- |
| OAuth user-to-machine (U2M) | Supported |
| OAuth machine-to-machine (M2M) | Not supported |
| Basic authentication (username/password) | Not supported |
| Basic authentication (API key) | Not supported |

←✕

| Authentication method | Availability |
| --- | --- |
| OAuth user-to-machine (U2M) | Supported |
| OAuth machine-to-machine (M2M) | Not supported |
| Basic authentication (username/password) | Not supported |
| Basic authentication (API key) | Not supported |

## Ingest from SurveyMonkey in 3 steps

note

Before starting, review the [Databricks user persona](/aws/en/connect/managed-ingestion), [supported interfaces](/aws/en/ingestion/lakeflow-connect/faq#interfaces), [ingestion frequency](/aws/en/ldp/concepts/pipeline-mode), and [common patterns](/aws/en/ingestion/lakeflow-connect/common-patterns).

1. **[Configure SurveyMonkey for ingestion](/aws/en/ingestion/lakeflow-connect/surveymonkey-source-setup)** (Admins): Set up SurveyMonkey to authenticate with Databricks.
2. **[Create a Unity Catalog connection](/aws/en/ingestion/lakeflow-connect/surveymonkey-connection)** (Admins): Create a connection in Catalog Explorer to store credentials for Databricks to authenticate with SurveyMonkey.
3. **[Create an ingestion pipeline](/aws/en/ingestion/lakeflow-connect/surveymonkey-pipeline)** (Admins or non-admins): Select any supported interface and create a pipeline from an existing connection.