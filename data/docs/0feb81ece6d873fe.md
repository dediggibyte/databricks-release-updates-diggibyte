Synced tables let you serve lakehouse data through Lakebase Postgres. Unity Catalog tables sync into Postgres so applications can query lakehouse data directly with low latency. This process is commonly known as reverse ETL. The lakehouse is optimized for analytics and enrichment, while Lakebase is designed for operational workloads that require fast lookup-style queries and transactional consistency.

## What are synced tables?

Synced tables let you serve analytics-grade data from Unity Catalog through Lakebase Postgres, making it available to applications that need low-latency queries and full ACID transactions. They bridge the gap between analytical storage and operational systems by keeping your data ready to serve in real-time applications.

## Supported sources

Synced tables support the following Unity Catalog source types:

* Managed and external Delta tables
* Managed and external Iceberg tables
* Views and materialized views

## How it works

Databricks **synced tables** create a managed copy of your Unity Catalog data in Lakebase. When you create a synced table, you get:

1. A synced table in Unity Catalog that references the sync pipeline
2. **A Postgres table in Lakebase** (read-only, queryable by your applications)

For example, you can sync gold tables, engineered features, or ML outputs from `analytics.gold.user_profiles` into a new synced table `analytics.gold.user_profiles_synced`. In Postgres, the Unity Catalog schema name becomes the Postgres schema name, so this appears as `gold.user_profiles_synced`:

SQL

```
SELECT * FROM gold.user_profiles_synced WHERE user_id = 12345;
```

Applications connect with standard Postgres drivers and query the synced data alongside their own operational state.

warning

While it's possible to modify a synced table directly in Postgres, Databricks strictly recommends running only read queries to protect data integrity with the source. For supported operations on synced tables, see [Operations allowed on synced tables in Postgres](#synced-table-postgres-ops).

Sync pipelines use managed Lakeflow pipelines to continuously update both the Unity Catalog synced table and the Postgres table with changes from the source table. Each sync can use up to 16 connections to your Lakebase database.

Lakebase Postgres supports up to 1,000 concurrent connections with transactional guarantees, so applications can read enriched data while also handling inserts, updates, and deletes in the same database.

### Accelerated initial sync

LTAP Direct Writes is a beta capability of the [LTAP architecture](/aws/en/oltp/projects/ltap-overview) that reduces the time required for initial loads and full refreshes. It loads data directly into the storage layer backing your Lakebase branch instead of routing the bulk write through the live compute endpoint. As a result, large loads finish faster and don't add query load to the endpoint while they run.

The LTAP Direct Writes capability accelerates the *initial load for every sync mode*. Every synced table begins by loading a full copy of the source, and that first load uses LTAP Direct Writes whether you choose **Snapshot**, **Triggered**, or **Continuous** mode. It also accelerates full refreshes, including the recurring full loads that **Snapshot** mode runs on every subsequent sync.

note

LTAP Direct Writes isn't limited to **Snapshot** mode. Every sync mode gets an accelerated initial load. **Snapshot** mode additionally gets an accelerated full refresh on each subsequent sync, while **Triggered** and **Continuous** modes apply later updates incrementally through Change Data Feed rather than as bulk loads.

LTAP Direct Writes is in beta and requires a Lakebase project running Postgres 17. To use it, a workspace admin enables the **LTAP Direct Writes** preview from the **Previews** page in workspace settings.

### Sync modes

Choose the right sync mode based on your application needs:

| Mode | Description | When to use | Performance |
| --- | --- | --- | --- |
| **Snapshot** | One-time copy of all data | Source changes >10% of rows per cycle | 10x more efficient if modifying >10% of source data |
| **Triggered** | Scheduled updates that run on demand or at intervals | Source rows change on a known cadence. Inserts, updates, and deletes are propagated each refresh. | Good cost/lag balance. Expensive if run <5min intervals |
| **Continuous** | Real-time streaming with seconds of latency | Changes must appear in Lakebase in near real time | Lowest lag, highest cost. Minimum 15-second intervals |

←✕

| Mode | Description | When to use | Performance |
| --- | --- | --- | --- |
| **Snapshot** | One-time copy of all data | Source changes >10% of rows per cycle | 10x more efficient if modifying >10% of source data |
| **Triggered** | Scheduled updates that run on demand or at intervals | Source rows change on a known cadence. Inserts, updates, and deletes are propagated each refresh. | Good cost/lag balance. Expensive if run <5min intervals |
| **Continuous** | Real-time streaming with seconds of latency | Changes must appear in Lakebase in near real time | Lowest lag, highest cost. Minimum 15-second intervals |

The source requirement depends on the sync mode:

* **Snapshot** copies all data on each sync, so the source only needs to support `SELECT *`.
* **Triggered** and **Continuous** apply row-level changes incrementally, so the source must provide a change data feed. Enable write-time [change data feed](https://docs.databricks.com/aws/en/tables/features/change-data-feed) on the source, or use Automatic change data feed. If a Triggered or Continuous source has no change data feed, the UI shows a warning with the exact `ALTER TABLE` command to run.

[Automatic change data feed](https://docs.databricks.com/aws/en/tables/features/change-data-feed#automatic-change-data-feed) (Public Preview) computes row-level changes at read time instead of requiring write-time change data feed on the source. This lets more source types, including **Apache Iceberg** tables and **materialized views**, sync in **Triggered** or **Continuous** mode. For the source types that Automatic change data feed supports, see the [Automatic change data feed](https://docs.databricks.com/aws/en/tables/features/change-data-feed#automatic-change-data-feed) documentation.

Automatic change data feed for synced tables is in preview. While it's in preview, complete two extra steps:

1. **Enable the preview.** A workspace admin enables the **Automatic change data feed** preview from the **Previews** page in workspace settings.
2. **Set the pipeline channel to preview.** When you create the synced table, set the pipeline channel to `PREVIEW`. This option is currently available through the API only:

   JSON

   ```
   {  
     "spec": {  
       "new_pipeline_spec": {  
         "pipeline_channel": "PREVIEW"  
       }  
     }  
   }
   ```

## Example use cases

You can use synced tables for data-serving use cases like:

* Personalization engines that serve fresh user profiles to Databricks Apps
* Applications that serve model predictions or feature values computed in the lakehouse
* Customer-facing dashboards that serve KPIs in real time
* Fraud detection services that serve risk scores for immediate action
* Support tools that serve enriched customer records from lakehouse data

## Create a synced table

### Prerequisites

You need:

* A Databricks workspace with Lakebase enabled.
* A Lakebase project (see [Create a project](/aws/en/oltp/projects/manage-projects#create-projects)).
* A Unity Catalog table to sync.
* Permissions to create synced tables. You need **USE\_SCHEMA** and **CREATE\_TABLE** on any schema you use.

For **Triggered** or **Continuous** modes, the source must provide a change data feed. Either enable write-time change data feed on an eligible Delta source table, or use [Automatic change data feed](#modes) for sources such as Apache Iceberg tables and materialized views. Automatic change data feed is in Public Preview and requires the extra setup described in [Sync modes](#modes).

To enable write-time change data feed on a Delta source table, run:

SQL

```
ALTER TABLE your_catalog.your_schema.your_table  
SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
```

For capacity planning and data type compatibility, see [Data types and compatibility](#data-types) and [Capacity planning](#capacity).

* UI
* CLI
* Python SDK
* Java SDK
* curl

1. Go to **Catalog** in the workspace sidebar and select the Unity Catalog table you want to sync.
2. Click **Create** > **Synced table** from the table details view.
3. In the **Create synced table** dialog:

   The catalog and schema lists only include Unity Catalog schemas where the current user has **USE\_SCHEMA** and **CREATE\_TABLE** privileges. If you don't see a schema you expect, confirm your permissions with your catalog admin.

   1. **Table name**: Enter a name for your synced table (it is created in the same catalog and schema as your source table). This creates both a Unity Catalog synced table and a Postgres table you can query.
   2. **Database type**: Choose **Lakebase Serverless (Autoscaling)**.
   3. **Sync mode**: Choose **Snapshot**, **Triggered**, or **Continuous** based on your needs (see [sync modes](#modes) above).
   4. Configure your project, branch, and database selections.
   5. Verify the **Primary key** is correct (usually auto-detected).

      important

      Columns in the primary key are not nullable in the synced table. Rows with nulls in primary key columns are *excluded from the sync*.
   6. (Optional) If two rows can share the same primary key in the source table, select a **Timeseries key** to configure deduplication. When a timeseries key is specified, the synced table contains only the row with the latest timeseries key value for each primary key. For the failure mode without a timeseries key, see [Duplicate keys](#capacity).

   If you chose Triggered or Continuous mode and haven't enabled Change Data Feed yet, you'll see a warning with the exact command to run. For data type compatibility questions, see [Data types and compatibility](#data-types).

   Click **Create** to create the synced table.
4. Monitor the synced table in **Catalog**. The **Overview** tab shows sync status, configuration, pipeline status, and last sync timestamp. Use **Sync now** for manual refresh.

Bash

```
databricks postgres create-synced-table my-catalog.sales.orders \  
  --json '{  
    "spec": {  
      "source_table_full_name": "main.sales.orders",  
      "branch": "projects/my-project/branches/production",  
      "primary_key_columns": ["order_id"],  
      "scheduling_policy": "SNAPSHOT",  
      "postgres_database": "mydb",  
      "create_database_objects_if_missing": true  
    }  
  }'
```

The `SYNCED_TABLE_ID` positional argument uses the format `catalog.schema.table`. In Postgres, the table `{table}` is created in schema `{schema}`, inside the database you set with `postgres_database` (here, `mydb`). The command waits for the operation to complete by default. For all available options, see [databricks postgres create-synced-table](/aws/en/dev-tools/cli/reference/postgres-commands#databricks-postgres-create-synced-table).

Python

```
from databricks.sdk import WorkspaceClient  
from databricks.sdk.service.postgres import (  
    SyncedTable,  
    SyncedTableSyncedTableSpec,  
    SyncedTableSyncedTableSpecSyncedTableSchedulingPolicy,  
)  
  
w = WorkspaceClient()  
  
synced_table = w.postgres.create_synced_table(  
    synced_table=SyncedTable(spec=SyncedTableSyncedTableSpec(  
        source_table_full_name="main.sales.orders",  
        branch="projects/my-project/branches/production",  
        primary_key_columns=["order_id"],  
        scheduling_policy=SyncedTableSyncedTableSpecSyncedTableSchedulingPolicy.SNAPSHOT,  
        postgres_database="mydb",  
        create_database_objects_if_missing=True,  
    )),  
    synced_table_id="my-catalog.sales.orders",  
).wait()  
  
print(f"Synced table created: {synced_table.name}")
```

The `synced_table_id` uses the format `catalog.schema.table` and becomes the Unity Catalog synced table name. In Postgres, the table `{table}` is created in schema `{schema}`, inside the database you set with `postgres_database` (here, `mydb`).

Java

```
import com.databricks.sdk.WorkspaceClient;  
import com.databricks.sdk.service.postgres.*;  
import java.util.List;  
  
WorkspaceClient w = new WorkspaceClient();  
  
SyncedTable syncedTable = w.postgres().createSyncedTable(  
    new CreateSyncedTableRequest()  
        .setSyncedTableId("my-catalog.sales.orders")  
        .setSyncedTable(new SyncedTable()  
            .setSpec(new SyncedTableSyncedTableSpec()  
                .setSourceTableFullName("main.sales.orders")  
                .setBranch("projects/my-project/branches/production")  
                .setPrimaryKeyColumns(List.of("order_id"))  
                .setSchedulingPolicy(SyncedTableSyncedTableSpecSyncedTableSchedulingPolicy.SNAPSHOT)  
                .setPostgresDatabase("mydb")  
                .setCreateDatabaseObjectsIfMissing(true))))  
    .waitForCompletion();  
  
System.out.println("Synced table created: " + syncedTable.getName());
```

Bash

```
curl -X POST "https://your-workspace.cloud.databricks.com/api/2.0/postgres/synced_tables?synced_table_id=my-catalog.sales.orders" \  
  -H "Authorization: Bearer ${DATABRICKS_TOKEN}" \  
  -H "Content-Type: application/json" \  
  -d '{  
    "spec": {  
      "source_table_full_name": "main.sales.orders",  
      "branch": "projects/my-project/branches/production",  
      "primary_key_columns": ["order_id"],  
      "scheduling_policy": "SNAPSHOT",  
      "postgres_database": "mydb",  
      "create_database_objects_if_missing": true  
    }  
  }'
```

This returns a long-running operation. Poll the returned `name` field until `done: true`. See [Long-running operations](/aws/en/oltp/projec