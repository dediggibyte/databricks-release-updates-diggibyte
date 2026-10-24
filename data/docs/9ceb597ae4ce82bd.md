This page provides working code examples for real-time mode queries in Structured Streaming, from simple stateless transformations to complex stateful processing with custom state management. See [Real-time mode concepts](/aws/en/structured-streaming/real-time/concepts) for concepts and [Tutorial: Run a real-time streaming workload](/aws/en/structured-streaming/real-time/tutorial) for a hands-on tutorial.

## Prerequisites

To run the examples on this page, you need:

* A real-time mode cluster configured and running. See [Set up real-time mode](/aws/en/structured-streaming/real-time/setup) for requirements and configuration, or [Tutorial: Run a real-time streaming workload](/aws/en/structured-streaming/real-time/tutorial) for a step-by-step tutorial.
* Basic familiarity with Structured Streaming concepts. See [Structured Streaming concepts](/aws/en/structured-streaming/concepts) if you're new to streaming.
* Access to supported streaming sources and sinks:

  + For Kafka examples: A Kafka broker with input/output topics configured
  + For Kinesis examples: A Unity Catalog connection of type `KINESIS` and a stream configured for polling mode or Enhanced Fan-Out (EFO) mode. See [Kinesis authentication](/aws/en/connect/streaming/kinesis/authentication#kinesis-uc-connection).
  + For Lakebase examples: A Lakebase database. See [Requirements](/aws/en/structured-streaming/lakebase#reqs) for requirements.
  + For custom sink examples: Target database or service configured (PostgreSQL for the example provided)

note

The examples use placeholder values like `broker_address`, `input_topic`, and `checkpoint_location`. Replace these with your actual configuration values before running the code.

## Stateless query examples

Stateless queries process each record independently without maintaining any state between records. These queries are typically simpler and have lower latency than stateful queries because they don't need to manage state storage or perform lookups. Use stateless queries for transformations, filtering, joins with static data, and routing operations.

### Kafka source to Kafka sink

In this example, you read from a Kafka source and write to a Kafka sink.

* Python
* Scala

Python

```
query = (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("startingOffsets", "earliest")

.option("subscribe", input_topic)

.load()

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("topic", output_topic)

.option("checkpointLocation", checkpoint_location)

.trigger(realTime="5 minutes")

.outputMode("update")

.start()

)
```

Scala

```
import org.apache.spark.sql.streaming.OutputMode

import org.apache.spark.sql.execution.streaming.RealTimeTrigger

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("subscribe", inputTopic)

.load()

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("topic", outputTopic)

.option("checkpointLocation", checkpointLocation)

.trigger(RealTimeTrigger.apply())

.outputMode(OutputMode.Update())

.start()
```

### Repartition

In this example, you read from a Kafka source, repartition the data into 20 partitions, and write to a Kafka sink.

Due to a current implementation limitation, you must set the Spark configuration `spark.sql.execution.sortBeforeRepartition` to `false` before using the repartition.

* Python
* Scala

Python

```
# Sorting is not supported in repartition with real-time mode, so you must set this to false to achieve low latency.

spark.conf.set("spark.sql.execution.sortBeforeRepartition", "false")

query = (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("subscribe", input_topic)

.option("startingOffsets", "earliest")

.load()

.repartition(20)

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("topic", output_topic)

.option("checkpointLocation", checkpoint_location)

.trigger(realTime="5 minutes")

.outputMode("update")

.start()

)
```

Scala

```
import org.apache.spark.sql.streaming.OutputMode

import org.apache.spark.sql.execution.streaming.RealTimeTrigger

// Sorting is not supported in repartition with real-time mode, so you must set this to false to achieve low latency.

spark.conf.set("spark.sql.execution.sortBeforeRepartition", "false")

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("subscribe", inputTopic)

.load()

.repartition(20)

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("topic", outputTopic)

.option("checkpointLocation", checkpointLocation)

.trigger(RealTimeTrigger.apply())

.outputMode(OutputMode.Update())

.start()
```

### Stream-snapshot join (broadcast only)")

In this example, you read from Kafka, join the data with a static table, and write to a Kafka sink. Only stream-static joins that broadcast the static table are supported, which means the static table should fit in memory.

* Python
* Scala

Python

```
from pyspark.sql.functions import broadcast, expr

# We assume the static table in the path `static_table_location` has a column 'lookupKey'.

query = (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("subscribe", input_topic)

.option("startingOffsets", "earliest")

.load()

.withColumn("joinKey", expr("CAST(value AS STRING)"))

.join(

broadcast(spark.read.format("parquet").load(static_table_location)),

expr("joinKey = lookupKey")

)

.selectExpr("value AS key", "value")

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("topic", output_topic)

.option("checkpointLocation", checkpoint_location)

.trigger(realTime="5 minutes")

.outputMode("update")

.start()

)
```

Scala

```
import org.apache.spark.sql.functions.{broadcast, expr}

import org.apache.spark.sql.streaming.OutputMode

import org.apache.spark.sql.execution.streaming.RealTimeTrigger

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("subscribe", inputTopic)

.load()

.join(broadcast(spark.read.format("parquet").load(staticTableLocation)), expr("joinKey = lookupKey"))

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("topic", outputTopic)

.option("checkpointLocation", checkpointLocation)

.trigger(RealTimeTrigger.apply())

.outputMode(OutputMode.Update())

.start()
```

### Kinesis source to Kafka sink

Polling mode for Kinesis real-time queries is available in Databricks Runtime 19 and above. The following example reads from a Kinesis source and writes to a Kafka sink using a Unity Catalog connection:

* Python
* Scala

Python

```
query = (

spark.readStream

.format("kinesis")

.option("streamName", stream_name)

.option("databricks.connection", kinesis_connection)

.option("consumerMode", "polling")

.load()

.selectExpr("partitionKey AS key", "CAST(data AS STRING) AS value")

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("topic", output_topic)

.option("checkpointLocation", checkpoint_location)

.trigger(realTime="5 minutes")

.outputMode("update")

.start()

)
```

Scala

```
import org.apache.spark.sql.streaming.OutputMode

import org.apache.spark.sql.execution.streaming.RealTimeTrigger

spark.readStream

.format("kinesis")

.option("streamName", streamName)

.option("databricks.connection", kinesisConnection)

.option("consumerMode", "polling")

.load()

.select(

col("partitionKey").alias("key"),

col("data").cast("string").alias("value")

)

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("topic", outputTopic)

.option("checkpointLocation", checkpointLocation)

.trigger(RealTimeTrigger.apply())

.outputMode(OutputMode.Update())

.start()
```

To use Enhanced Fan-Out (EFO) mode instead, set `consumerMode` to `efo`. See [Configure Kinesis enhanced fan-out (EFO) for streaming query reads](/aws/en/connect/streaming/kinesis/#efo).

### Union

In this example, you union two Kafka DataFrames from two different topics and write to a Kafka sink.

* Python
* Scala

Python

```
df1 = (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("startingOffsets", "earliest")

.option("subscribe", input_topic_1)

.load()

)

df2 = (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("startingOffsets", "earliest")

.option("subscribe", input_topic_2)

.load()

)

query = (

df1.union(df2)

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("topic", output_topic)

.option("checkpointLocation", checkpoint_location)

.trigger(realTime="5 minutes")

.outputMode("update")

.start()

)
```

Scala

```
import org.apache.spark.sql.streaming.OutputMode

import org.apache.spark.sql.execution.streaming.RealTimeTrigger

val df1 = spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("subscribe", inputTopic1)

.load()

val df2 = spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("subscribe", inputTopic2)

.load()

df1.union(df2)

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("topic", outputTopic)

.option("checkpointLocation", checkpointLocation)

.trigger(RealTimeTrigger.apply())

.outputMode(OutputMode.Update())

.start()
```

### Kafka source to Lakebase sink

In these examples, you read from a Kafka source and write to a Lakebase database. For all connection options, see [Connect to Lakebase](/aws/en/structured-streaming/lakebase).

#### Lakebase tables registered with Unity Catalog

The following example uses the Unity Catalog connection method, which automatically manages credentials. The target Lakebase database must be registered with Unity Catalog. See [Register a Lakebase database in Unity Catalog](/aws/en/oltp/projects/register-uc).

* Python
* Scala

Python

```
query = (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("subscribe", input_topic)

.option("startingOffsets", "earliest")

.load()

.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

.writeStream

.outputMode("update")

.option("checkpointLocation", checkpoint_location)

.option("upsertkey", "<primary_key>")

.trigger(realTime="5 minutes")

.toTable("<catalog>.<schema>.<table>")

)
```

Scala

```
import org.apache.spark.sql.execution.streaming.RealTimeTrigger

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("subscribe", inputTopic)

.load()

.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

.writeStream

.outputMode("update")

.option("checkpointLocation", checkpointLocation)

.option("upsertkey", "<primary_key>")

.trigger(RealTimeTrigger.apply())

.toTable("<catalog>.<schema>.<table>")
```

Replace `<catalog>.<schema>.<table>` with the fully qualified name of the target table, and `<primary_key>` with the primary key column. If the table doesn't exist, the connector creates it using that key.

#### Lakebase tables not registered with Unity Catalog

For Lakebase tables not registered with Unity Catalog, use the `endpoint` and `dbtable` options:

* Python
* Scala

Python

```
query = (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("subscribe", input_topic)

.option("startingOffsets", "earliest")

.load()

.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

.writeStream

.format("postgresql")

.outputMode("update")

.option("endpoint", "<project-id>.<branch-id>.<endpoint-id>")

.option("dbtable", "<schema>.<table>")

.option("upsertkey", "<primary_key>")

.option("checkpointLocation", checkpoint_location)

.trigger(realTime="5 minutes")

.start()

)
```

Scala

```
import org.apache.spark.sql.execution.streaming.RealTimeTrigger

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", brokerAddress)

.option("subscribe", inputTopic)

.load()

.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

.writeStream

.format("postgresql")

.outputMode("update")

.option("endpoint", "<project-id>.<branch-id>.<endpoint-id>")

.option("dbtable", "<schema>.<table>")

.option("upsertkey", "<primary_key>")

.option("checkpointLocation", checkpointLocation)

.trigger(RealTimeTrigger.apply())

.start()
```

Replace `<catalog>.<schema>.<table>` with the fully qualified name of the target table, and `<primary_key>` with the primary key column.

See [Lakebase tables not registered with Unity Catalog](/aws/en/structured-streaming/lakebase#lakebase-no-uc) for all available options.

## Stateful query examples

Stateful queries maintain state information across records, enabling operations such as deduplication, aggregation, and windowing. These queries are essential for use cases that require tracking information over time or across multiple events. Real-time mode supports stateful operations with the same semantics as micro-batch mode, but processes data continuously for lower latency. Stateful queries require more memory and compute resources than stateless queries because they must maintain and update state.

### Deduplication

In this example, you deduplicate records based on the `timestamp` and `value` columns.

* Python
* Scala

Python

```
query = (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("startingOffsets", "earliest")

.option("subscribe", input_topic)

.load()

.dropDuplicates(["timestamp", "value"])

.writeStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("topic", output_topic)

.option("checkpointLocation", checkpoint_location)

.trigger(realTime="5 minutes")

.outputMode("update")

.start()

)
``