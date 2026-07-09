On this page

Last updated on **Jun 9, 2026**

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). Workspace admins can control access to this feature from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

The managed RabbitMQ connector in Lakeflow Connect allows you to stream messages from RabbitMQ classic queues into streaming tables in Databricks. The connector provides at-least-once delivery semantics and handles authentication, message decoding, acknowledgement, and pipeline lifecycle management, so you don't need to write Structured Streaming code directly.

## RabbitMQ connector components[​](#rabbitmq-connector-components "Direct link to RabbitMQ connector components")

| Component | Description |
| --- | --- |
| Connection | A Unity Catalog securable object that stores the broker endpoint and authentication credentials for your RabbitMQ broker. The managed RabbitMQ connector uses this connection to authenticate without requiring credentials in your pipeline configuration. |
| Ingestion pipeline | A pipeline that continuously consumes messages from one or more RabbitMQ classic queues and writes the results to streaming tables. The pipeline runs on serverless compute. |
| Destination tables | The [streaming tables](/aws/en/ldp/concepts/streaming-tables) where the ingestion pipeline writes the data. |

## Start ingesting from RabbitMQ[​](#start-ingesting-from-rabbitmq "Direct link to Start ingesting from RabbitMQ")

The following table provides an overview of the end-to-end RabbitMQ ingestion flow, based on user type:

| User | Steps |
| --- | --- |
| Admin | Use Catalog Explorer to create a connection so that any user with `USE CONNECTION` or `ALL PRIVILEGES` can create pipelines. See [Create a RabbitMQ connection](/aws/en/ingestion/lakeflow-connect/rabbitmq-connection). |
| Non-admin | Use any supported interface to create a pipeline from an existing connection. See [Ingest data from RabbitMQ](/aws/en/ingestion/lakeflow-connect/rabbitmq-pipeline). |

## Feature availability[​](#feature-availability "Direct link to Feature availability")

| Feature | Availability |
| --- | --- |
| UI-based pipeline authoring | Not supported (Beta) |
| API-based pipeline authoring | Supported |
| Declarative Automation Bundles | Supported |
| Continuous streaming ingestion | Supported |
| Unity Catalog governance | Supported |
| Orchestration using Databricks Workflows | Not supported |
| SCD type 2 | Not supported |
| Column selection and deselection | Not supported (Beta) |
| Row filtering | Not supported |

## Authentication methods[​](#authentication-methods "Direct link to Authentication methods")

| Authentication method | Availability |
| --- | --- |
| Username and password | Supported |
| Service Credential | Not supported |
| OAuth U2M | Not supported |
| OAuth M2M | Not supported |