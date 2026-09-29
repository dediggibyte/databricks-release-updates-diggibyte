The Spark Data Source API lets you read from and write to external databases directly from Databricks. Use it only when you need the full flexibility of the Spark engine, want to execute native queries on the source, or require write access to external systems. In general, Databricks recommends governed, read-only access with automatic Spark or SQL query pushdown. See [What is query federation?](/aws/en/query-federation/database-federation).

The Spark Data Source API has specific behaviors for connectivity, query execution, and schema detection.

* The primary workload and any subsequent Spark transformations run on the Databricks Spark cluster.
* When using the `query` option, the specified SQL statement runs entirely on the external data source. Spark fetches the results without performing transformation pushdown on the query string.
* The connection requires either a Databricks-bundled connector, a user-provided JDBC driver, or a PySpark custom data source.
* Spark automatically reads the schema from the external database table and maps its types to Spark SQL types.

## Use a bundled connector

Databricks Runtime includes optimized connectors for common data sources. See [Supported bundled connectors](#supported-connectors) for the complete list.

Bundled connectors use `host` and `port` as separate options instead of a full JDBC URL string.

### Read data using a pass-through query

Using the `query` option ensures that filter and join logic executes on the source database before data reaches Spark. For governed read access with automatic query pushdown and Unity Catalog permission delegation through views, consider [remote queries](/aws/en/query-federation/remote-queries) instead.

Python

```
df = (spark.read  
  .format("sqlserver")  
  .option("host", "<your-sql-server-instance>.database.windows.net")  
  .option("user", dbutils.secrets.get(scope="<scope>", key="<user>"))  
  .option("password", dbutils.secrets.get(scope="<scope>", key="<password>"))  
  .option("database", "<database-name>")  
  .option("query", "SELECT id, name FROM users WHERE active = 1")  
  .load())
```

### Write data

Specify a write mode with `.mode()` to control how data is written. Use `append` to add rows to an existing table or `overwrite` to replace its contents.

Python

```
(df.write  
  .format("sqlserver")  
  .mode("overwrite")  
  .option("host", "<your-sql-server-instance>.database.windows.net")  
  .option("user", dbutils.secrets.get(scope="<scope>", key="<user>"))  
  .option("password", dbutils.secrets.get(scope="<scope>", key="<password>"))  
  .option("database", "<database-name>")  
  .option("dbtable", "<table-name>")  
  .save())
```

## Use a JDBC Unity Catalog connection

If a source-specific connector is not bundled, or if you want to use a specific JDBC driver version, use a JDBC Unity Catalog connection. This lets you centralize credential management and bring your own JDBC driver.

A JDBC Unity Catalog connection offers several advantages over using a bundled connector or raw JDBC driver directly. With a JDBC Unity Catalog connection, you can:

* Bring your own JDBC driver JAR for any database that supports JDBC.
* Create the connection once and reuse it across serverless, standard, and dedicated compute.
* Utilize governed access to the data source using a Unity Catalog connection object.
* Hide connection credentials from the querying user.
* Read from and write to external databases through the Spark Data Source API.

To use a JDBC Unity Catalog connection, specify `databricks.connection` in your Spark options:

Python

```
df = (spark.read  
  .format("jdbc")  
  .option("databricks.connection", "<connection-name>")  
  .option("query", "SELECT * FROM external_table")  
  .load())
```

For setup instructions, see [JDBC connection](/aws/en/connect/jdbc-connection).

## Use a custom connector on dedicated compute

On dedicated (classic) compute, you can install third-party Spark data source connectors or JDBC drivers that are not bundled with Databricks Runtime.

Use this approach when:

* You need a third-party Spark connector for systems such as MongoDB, Cassandra, Couchbase, or Elasticsearch.
* You need a specific driver version that is not bundled in the runtime.
* You want to install a JDBC driver directly on the cluster without setting up a Unity Catalog connection.

### Install a connector or driver

Install the library on your cluster through **Compute** > **your cluster** > **Libraries** > **Install new**. You can use Maven coordinates directly without downloading or uploading any JARs. Restart the cluster for the library to take effect.

### Read data

Once the connector is installed, use the connector's format name and its required connection options to read data.

Python

```
df = (spark.read  
  .format("mongodb")  
  .option("connection.uri", "mongodb://<hostname>:27017")  
  .option("database", "<database-name>")  
  .option("collection", "<collection-name>")  
  .load())
```

### Write data

Use the same format name and connection options to write data back to the source.

Python

```
(df.write  
  .format("mongodb")  
  .mode("overwrite")  
  .option("connection.uri", "mongodb://<hostname>:27017")  
  .option("database", "<database-name>")  
  .option("collection", "<collection-name>")  
  .save())
```

### Considerations

Keep the following in mind when using custom connectors on dedicated compute.

* The driver or connector is available only on the cluster where it is installed.
* Custom third-party Spark JARs are not supported on Databricks SQL, serverless, or standard access mode compute. For those compute types, use bundled connectors or JDBC Unity Catalog connections.

## PySpark custom data sources

The Python DataSource API lets you build custom data connectors entirely in Python, without JARs or JVM-based libraries. Use this when you need to connect to REST APIs, SaaS applications, or any system without a JDBC interface, or when you want to generate synthetic data programmatically. The API supports both batch and streaming reads and writes.

note

PySpark custom data sources require Databricks Runtime 15.4 LTS or above.

For setup, examples, and API reference, see [PySpark custom data sources](/aws/en/pyspark/datasources).

## Compare integration strategies

The following table compares the Spark Data Source API against Lakehouse Federation and Lakeflow Connect to help you choose the right approach for your use case.

| Feature | Spark Data Source API | Lakehouse Federation | Lakeflow Connect |
| --- | --- | --- | --- |
| Primary use case | Complex ETL, custom Spark logic, pass-through queries | Ad-hoc queries, BI reporting | High-scale, automated ingestion |
| Data movement | Loaded into Spark memory (ephemeral) | Loaded into Spark memory (ephemeral) | Copied to Delta Lake (persistent) |
| Query execution | Manual pushdown using the native `query` option | Automatic pushdown of Spark and SQL filters, joins, and aggregations | Not applicable (full table replication) |
| Governance | Unity Catalog connection (JDBC) or secret scopes | Unity Catalog (federated catalog) | Unity Catalog (managed pipeline) |
| Best for | Power users needing full Spark flexibility | Minimizing data movement while preserving governance | Production CDC and ingestion pipelines |

←✕

| Feature | Spark Data Source API | Lakehouse Federation | Lakeflow Connect |
| --- | --- | --- | --- |
| Primary use case | Complex ETL, custom Spark logic, pass-through queries | Ad-hoc queries, BI reporting | High-scale, automated ingestion |
| Data movement | Loaded into Spark memory (ephemeral) | Loaded into Spark memory (ephemeral) | Copied to Delta Lake (persistent) |
| Query execution | Manual pushdown using the native `query` option | Automatic pushdown of Spark and SQL filters, joins, and aggregations | Not applicable (full table replication) |
| Governance | Unity Catalog connection (JDBC) or secret scopes | Unity Catalog (federated catalog) | Unity Catalog (managed pipeline) |
| Best for | Power users needing full Spark flexibility | Minimizing data movement while preserving governance | Production CDC and ingestion pipelines |

## Supported bundled connectors

The following data sources are bundled in Databricks Runtime and can be called directly through Spark. Reads and writes are supported on dedicated and standard compute.

note

Writes on serverless compute are supported for PostgreSQL, SQL Server, MySQL, Snowflake, and Redshift. See [Serverless write options for bundled connectors](/aws/en/connect/spark-data-sources-serverless-writes) for supported connector options.

| Data source | `spark.format()` name |
| --- | --- |
| PostgreSQL | `"postgresql"` |
| SQL Server | `"sqlserver"` |
| MySQL and MariaDB | `"mysql"` |
| Snowflake | `"snowflake"` |
| Amazon Redshift | `"redshift"` |
| Google BigQuery | `"bigquery"` |
| Azure Synapse | `"SQLDW"` |
| HTTP | `"http"` |

←✕

| Data source | `spark.format()` name |
| --- | --- |
| PostgreSQL | `"postgresql"` |
| SQL Server | `"sqlserver"` |
| MySQL and MariaDB | `"mysql"` |
| Snowflake | `"snowflake"` |
| Amazon Redshift | `"redshift"` |
| Google BigQuery | `"bigquery"` |
| Azure Synapse | `"SQLDW"` |
| HTTP | `"http"` |

## Migrate BigQuery JDBC workloads for Databricks Runtime 20

Starting with Databricks Runtime 20, Databricks Runtime no longer includes the bundled BigQuery JDBC driver. Databricks Runtime 19 and earlier continue to include the driver. This change affects classic compute workloads that use Spark JDBC with a `jdbc:bigquery:` URL.

To find affected workloads, search their code and configuration for a `jdbc:bigquery:` URL. This JDBC path is separate from the bundled Google BigQuery connector, which uses `.format("bigquery")` and remains available. Without an installed BigQuery JDBC driver, affected workloads fail with a driver-not-found error.

Before moving an affected workload to Databricks Runtime 20 or later, choose one of the following options:

* For read-only workloads, use [Lakehouse Federation](/aws/en/query-federation/bigquery) to query BigQuery through a foreign catalog.
* Replace Spark JDBC reads and writes with the bundled Google BigQuery connector. See [Use a bundled connector](#bundled-connector) and [Supported bundled connectors](#supported-connectors).
* [Use a JDBC Unity Catalog connection](#jdbc-uc-connection) with your own BigQuery JDBC driver.
* On dedicated classic compute, [install your own BigQuery JDBC driver](#custom-connector).
* Keep the workload on Databricks Runtime 19 or earlier until you complete one of these changes.

For information about the drivers available from Google, see [BigQuery ODBC and JDBC drivers](https://cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers).

## Limitations

The following limitations apply when using the Spark Data Source API in Databricks.

* Spark options for bundled data sources are limited to `query`, `dbtable`, and a small set of connector-specific options.
* Custom third-party Spark JARs can only be installed on dedicated compute. For serverless or standard compute, use bundled connectors or JDBC Unity Catalog connections.
* PySpark custom data sources require Databricks Runtime 15.4 LTS or above.