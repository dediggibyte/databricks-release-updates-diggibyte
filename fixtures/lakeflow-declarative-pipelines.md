# Lakeflow Declarative Pipelines is now generally available

> date: 2026-06-16

Lakeflow Declarative Pipelines is now generally available on the Databricks
platform. Declarative Pipelines let you define end-to-end data pipelines in SQL
or Python by describing the transformations you want, while the runtime manages
orchestration, incremental processing, checkpointing, and recovery for you.

The generally available release adds:

- Serverless compute for pipeline execution with automatic scaling.
- Native change data capture (CDC) ingestion from operational databases.
- Data quality expectations with quarantine and alerting on failed rows.
- Unity Catalog governance for all pipeline tables and lineage.

Prerequisites:

- A workspace enabled for Unity Catalog.
- A region that supports serverless compute.
- Appropriate permissions to create pipelines and target schemas.

Limitations:

- Continuous mode is not yet supported for all sink types.
- Pipelines authored in the legacy DLT UI must be migrated to the new editor.

Recommended use cases include incremental ETL, CDC ingestion, medallion
architecture pipelines, and streaming aggregations. To get started, enable
serverless in your account, create a new pipeline in the Lakeflow editor,
define your tables, and run the pipeline.
