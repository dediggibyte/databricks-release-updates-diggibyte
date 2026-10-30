Real-time mode enables ultra-low-latency data processing, with end-to-end latency as low as five milliseconds. Use real-time mode for operational workloads that require immediate response to streaming data, such as fraud detection and real-time personalization.

Real-time mode is also available directly in Structured Streaming outside of pipelines. See [Real-time mode in Structured Streaming](/aws/en/structured-streaming/real-time/).

## How real-time mode achieves low latency

Real-time mode differs from standard continuous processing in three key ways:

* **Long-running batches**: The system processes data as it becomes available in the source within long-running batches (default is five minutes).
* **Simultaneous stage scheduling**: All query stages are scheduled at the same time. The compute resource must have enough available task slots to cover all stages concurrently. See [Compute sizing](#compute-sizing).
* **Streaming shuffle**: Data is passed between stages as soon as it is produced, rather than waiting for an upstream stage to complete before starting the downstream stage.

The checkpoint interval (configured via `pipelines.trigger.interval`) controls how frequently state and source offsets are persisted to durable storage. Longer intervals reduce checkpointing overhead but increase recovery time after a failure and delay metrics reporting. Shorter intervals improve durability but add overhead.

## Real-time mode and continuous pipelines

Real-time mode is a specialized type of continuous trigger. Continuous mode is still required; real-time mode adds flow-level latency optimizations on top. To use real-time mode, the pipeline must first run in continuous mode. Real-time mode then applies additional optimizations at the flow level to achieve sub-second latency beyond what standard continuous processing provides.

Enabling real-time mode requires three configuration steps:

1. Set the pipeline to continuous mode.
2. Enable real-time mode at the pipeline level.
3. Define a real-time update flow.

## Requirements

| Requirement | Value |
| --- | --- |
| Compute type | Classic compute or serverless |
| Pipeline mode | Continuous |

←✕

| Requirement | Value |
| --- | --- |
| Compute type | Classic compute or serverless |
| Pipeline mode | Continuous |

## Configure real-time mode

### Step 1: Set the pipeline to continuous mode

In your pipeline settings, set **Pipeline mode** to **Continuous**, or set it in the pipeline JSON:

JSON

```
{

"continuous": true

}
```

### Step 2: Enable real-time mode at the pipeline level

In your pipeline settings, add the following key to the Spark configuration under **Advanced > Spark config**:

ini

```
spark.databricks.streaming.realTimeMode.enabled = true
```

You can also set this in the pipeline JSON:

JSON

```
{

"continuous": true,

"spark_conf": {

"spark.databricks.streaming.realTimeMode.enabled": "true"

}

}
```

### Step 3: Define a real-time update flow

Real-time mode requires an update flow. Use `dp.create_sink()` or `@dp.foreach_sink` to define the output target, then use the [`@dp.update_flow`](/aws/en/ldp/developer/ldp-python-ref-update-flow) decorator with `pipelines.trigger` set to `"RealTime"` and `target` pointing to the sink.

Python

```
from pyspark import pipelines as dp

# Define the output sink

dp.create_sink(

"my_kafka_sink",

"kafka",

{

"kafka.bootstrap.servers": "<bootstrap-servers>",

"topic": "<output-topic>",

}

)

# Define the real-time update flow targeting the sink

@dp.update_flow(

name="my_rtm_flow",

target="my_kafka_sink",

spark_conf={

"pipelines.trigger": "RealTime",

"pipelines.trigger.interval": "5 minutes",  # optional; defaults to 5 minutes

}

)

def my_real_time_flow():

return (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", "<bootstrap-servers>")

.option("subscribe", "<input-topic>")

.load()

)
```

Flow-level configuration parameters:

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `pipelines.trigger` | Yes | — | Set to `"RealTime"` to enable real-time mode for this flow. |
| `pipelines.trigger.interval` | No | `"5 minutes"` | Checkpoint interval. Controls how often state and offsets are committed. Shorter values improve recoverability; longer values reduce overhead. |

←✕

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `pipelines.trigger` | Yes | — | Set to `"RealTime"` to enable real-time mode for this flow. |
| `pipelines.trigger.interval` | No | `"5 minutes"` | Checkpoint interval. Controls how often state and offsets are committed. Shorter values improve recoverability; longer values reduce overhead. |

## Code examples

### Kafka to Kafka

Read from a Kafka topic and write to a Kafka output target:

Python

```
from pyspark import pipelines as dp

dp.create_sink("kafka_output_sink", "kafka", {

"kafka.bootstrap.servers": broker_address,

"topic": output_topic,

})

@dp.update_flow(

name="kafka_rtm_flow",

target="kafka_output_sink",

spark_conf={

"pipelines.trigger": "RealTime",

"pipelines.trigger.interval": "5 minutes",

}

)

def kafka_rtm_flow():

return (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("subscribe", input_topic)

.option("startingOffsets", "latest")

.load()

.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")

)
```

### Kinesis to Kafka

Polling mode for Kinesis real-time pipelines is available in Databricks Runtime 19 and above. The following example reads from a Kinesis stream and writes to a Kafka sink using a Unity Catalog connection:

Python

```
from pyspark import pipelines as dp

dp.create_sink("kafka_output_sink", "kafka", {

"kafka.bootstrap.servers": broker_address,

"topic": output_topic,

})

@dp.update_flow(

name="kinesis_rtm_flow",

target="kafka_output_sink",

spark_conf={

"pipelines.trigger": "RealTime",

"pipelines.trigger.interval": "5 minutes",

}

)

def kinesis_rtm_flow():

return (

spark.readStream

.format("kinesis")

.option("streamName", stream_name)

.option("databricks.connection", kinesis_connection)

.option("initialPosition", "latest")

.option("consumerMode", "polling")

.load()

.selectExpr("CAST(partitionKey AS STRING) AS key", "data AS value")

)
```

For more information on Unity Catalog connections, see [Unity Catalog connections](/aws/en/connect/uc-connections).

### Kafka to a `ForEach` sink

Read from a Kafka topic and handle each row with a Python function in a [`ForEach` sink](/aws/en/ldp/for-each-sink):

Python

```
from pyspark import pipelines as dp

@dp.foreach_sink(name="events_foreach_sink")

def handle_event(row):

# Custom per-row logic here, such as a call to an external API.

...

@dp.update_flow(

name="foreach_rtm_flow",

target="events_foreach_sink",

spark_conf={

"pipelines.trigger": "RealTime",

"pipelines.trigger.interval": "5 minutes",

}

)

def foreach_rtm_flow():

return (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("subscribe", input_topic)

.option("startingOffsets", "latest")

.load()

.selectExpr("CAST(key AS STRING) AS key", "CAST(value AS STRING) AS value")

)
```

### Enrich with a broadcast join

Join a Kafka stream against a static lookup table. Only broadcast (stream-to-static) joins are supported. Stream-to-stream joins are not supported in real-time mode.

Python

```
from pyspark import pipelines as dp

from pyspark.sql.functions import broadcast, expr

dp.create_sink("enriched_output_sink", "kafka", {

"kafka.bootstrap.servers": broker_address,

"topic": enriched_output_topic,

})

@dp.update_flow(

name="enriched_events_flow",

target="enriched_output_sink",

spark_conf={

"pipelines.trigger": "RealTime",

"pipelines.trigger.interval": "5 minutes",

}

)

def enriched_events():

lookup = spark.read.table("catalog.schema.lookup_table")

return (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("subscribe", input_topic)

.load()

.withColumn("event_key", expr("CAST(value AS STRING)"))

.join(broadcast(lookup), expr("event_key = lookup_key"))

.select("event_key", "lookup_value", "timestamp")

)
```

### Aggregation

Count events by key using a stateful `groupBy`. Set `spark.sql.shuffle.partitions` to match the input partition count for stateful operations:

Python

```
from pyspark import pipelines as dp

from pyspark.sql.functions import col

dp.create_sink("event_counts_sink", "kafka", {

"kafka.bootstrap.servers": broker_address,

"topic": output_topic,

})

@dp.update_flow(

name="event_counts_flow",

target="event_counts_sink",

spark_conf={

"pipelines.trigger": "RealTime",

"pipelines.trigger.interval": "5 minutes",

"spark.sql.shuffle.partitions": "8",

}

)

def event_counts():

return (

spark.readStream

.format("kafka")

.option("kafka.bootstrap.servers", broker_address)

.option("subscribe", input_topic)

.load()

.selectExpr("CAST(key AS STRING) AS event_type", "timestamp")

.groupBy(col("event_type"))

.count()

)
```

## Supported sources and sinks

| Connector | As source | As sink | Notes |
| --- | --- | --- | --- |
| Apache Kafka | ✓ | ✓ | — |
| Azure Event Hubs (Kafka connector) | ✓ | ✓ | Uses the Kafka-compatible interface. |
| Delta | Not supported | Not supported | — |
| `ForEach` sink | Not applicable | ✓ | Runs your Python function or writer object for each row. See [Use a `ForEach` sink to write each row in pipelines](/aws/en/ldp/for-each-sink). |

←✕

| Connector | As source | As sink | Notes |
| --- | --- | --- | --- |
| Apache Kafka | ✓ | ✓ | — |
| Azure Event Hubs (Kafka connector) | ✓ | ✓ | Uses the Kafka-compatible interface. |
| Delta | Not supported | Not supported | — |
| `ForEach` sink | Not applicable | ✓ | Runs your Python function or writer object for each row. See [Use a `ForEach` sink to write each row in pipelines](/aws/en/ldp/for-each-sink). |

### AWS connectors

| Connector | As source | As sink | Notes |
| --- | --- | --- | --- |
| AWS MSK | ✓ | ✓ | Uses the Kafka-compatible interface. |
| Amazon Kinesis | ✓ | Not supported | Supports polling mode and Enhanced Fan-Out (EFO) mode. Polling mode requires Databricks Runtime 19 and above. See [Kinesis source to Kafka sink](/aws/en/structured-streaming/real-time/examples#kinesis-source-to-kafka-sink). |

←✕

| Connector | As source | As sink | Notes |
| --- | --- | --- | --- |
| AWS MSK | ✓ | ✓ | Uses the Kafka-compatible interface. |
| Amazon Kinesis | ✓ | Not supported | Supports polling mode and Enhanced Fan-Out (EFO) mode. Polling mode requires Databricks Runtime 19 and above. See [Kinesis source to Kafka sink](/aws/en/structured-streaming/real-time/examples#kinesis-source-to-kafka-sink). |

## Compute sizing

### Serverless pipelines on the preview channel

Beta

Running multiple real-time flows per pipeline without task slot contention, and source stage adaptive repartitioning, are in [Beta](/aws/en/release-notes/release-types). They are available only on serverless pipelines that use the [preview channel](/aws/en/release-notes/dlt/#runtime-channels).

Databricks reserves task slots for each real-time flow, so you can run multiple real-time flows in one pipeline without the flows competing for task slots. You don't need to size compute.

Source stage adaptive repartitioning automatically adjusts the number of tasks that read from each Kafka or Kinesis source to match its traffic. To use it, leave `maxPartitions` unset on Kafka sources, and leave `maxPartitions` and `shardsPerTask` unset on Kinesis sources. If you set these options, the source uses the fixed number of tasks you configured instead. Shuffle partition counts are not adjusted, so set `spark.sql.shuffle.partitions` for stateful flows as shown in [Aggregation](#aggregation).

### Serverless pipelines on the current channel

Databricks sizes compute for you. The number of tasks that read from each source is fixed, so set `maxPartitions` on Kafka sources, or `maxPartitions` or `shardsPerTask` on Kinesis sources to handle your peak traffic.

### Classic compute

The compute must have enough task slots to run all tasks across all query stages at the same time. The following table shows the required task slots for common pipeline types:

| Pipeline type | Configuration | Required task slots |
| --- | --- | --- |
| Single-stage stateless (Kafka source + sink) | `maxPartitions` = 8 | 8 |
| Two-stage stateful (Kafka source + shuffle) | `maxPartitions` = 8, shuffle partitions = 20 | 28 (8 + 20) |
| Three-stage (Kafka source + two shuffles) | `maxPartitions` = 8, two shuffle stages of 20 each | 48 (8 + 20 + 20) |

←✕

| Pipeline type | Configuration | Required task slots |
| --- | --- | --- |
| Single-stage stateless (Kafka source + sink) | `maxPartitions` = 8 | 8 |
| Two-stage stateful (Kafka source + shuffle) | `maxPartitions` = 8, shuffle partitions = 20 | 28 (8 + 20) |
| Three-stage (Kafka source + two shuffles) | `maxPartitions` = 8, two shuffle stages of 20 each | 48 (8 + 20 + 20) |

If you don't set `maxPartitions`, use the number of partitions in the Kafka topic.

## Operator support

| Category | Operator | Supported |
| --- | --- | --- |
| Stateless | Selection, Projection | ✓ |
| UDFs | Scala UDF | ✓ (with limitations) |
| UDFs | Python UDF | ✓ (with limitations) |
| Aggregation | sum, count, max, min, avg | ✓ |
| Windowing | Tumbling, Sliding | ✓ |
| Windowing | Session | Not supported |
| Deduplication | `dropDuplicates` | ✓ (unbounded state) |
| Deduplication | `dropDuplicatesWithinWatermark` | Not supported |
| Joins | Broadcast table join | ✓ |
| Joins | Stream-to-stream join | Not supported |
| Custom | `transformWithState` | ✓ (with behavioral differences) |
| Custom | `union` | ✓ (with limitations) |
| Custom | `forEach` | ✓ |
| Custom | `flatMapGroupsWithState` | Not supported |
| Custom | `mapPartitions` | Not supported |
| Custom | `forEachBatch` | Not supported |

←✕

| Category | Operator | Support