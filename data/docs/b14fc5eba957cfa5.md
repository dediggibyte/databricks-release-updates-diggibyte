AI Search endpoint metrics report health, query rate, latency, errors by source, and ingestion rate for the last 169 hours. Use these metrics to monitor endpoints and debug issues. View the metrics on the endpoint's **Metrics** tab, or retrieve them with the REST API, the Databricks CLI, or the Databricks SDK.

Use endpoint metrics to:

* Find out whether failed queries come from the embedding model endpoint or from AI Search.
* See why queries return 429 (Too Many Requests) errors.
* Check whether writes to an index happen at the same time as latency spikes or errors.

## Requirements

* An AI Search endpoint. See [Create AI Search endpoints and indexes](/aws/en/ai-search/create-ai-search).
* Permission to view the endpoint. See [AI Search endpoint ACLs](/aws/en/security/auth/access-control/#vector-search-endpoints).
* To use the API, CLI, or SDK, authentication to your workspace. See [Data protection and authentication](/aws/en/ai-search/ai-search#authentication).

## View metrics in the UI

To view the metrics for an endpoint:

1. In the left sidebar, click **Compute**.
2. Click the **AI Search** tab, and then click the name of the endpoint.
3. On the endpoint page, click the **Metrics** tab.
4. Select a time range: **Past 15 minutes**, **Past hour**, **Past 6 hours**, **Past day**, or **Past week**.

The **Metrics** tab shows the following charts:

| Chart | What it shows |
| --- | --- |
| **Health status** | The health of the endpoint over time. |
| **Endpoint concurrency** | The concurrency provisioned for the endpoint. |
| **Requests per second** | Queries per second, by route (optimized and non-optimized). |
| **Error rate (%)** | The percentage of queries that returned errors, including 429 errors. Use the source filter to see where errors come from. See [Filter errors by source](#error-source). |
| **Request latency (ms)** | Query latency at p50 and p99, by route. Use the query type filter to show **ANN**, **Hybrid**, or **Full-text** queries. |
| **Ingestion rate (rows/sec)** | Rows written to the endpoint's indexes per second, by operation. Standard endpoints only. See [Read the ingestion rate](#ingestion-rate). When the endpoint has two or more indexes, use the index filter to show one index. |

←✕

| Chart | What it shows |
| --- | --- |
| **Health status** | The health of the endpoint over time. |
| **Endpoint concurrency** | The concurrency provisioned for the endpoint. |
| **Requests per second** | Queries per second, by route (optimized and non-optimized). |
| **Error rate (%)** | The percentage of queries that returned errors, including 429 errors. Use the source filter to see where errors come from. See [Filter errors by source](#error-source). |
| **Request latency (ms)** | Query latency at p50 and p99, by route. Use the query type filter to show **ANN**, **Hybrid**, or **Full-text** queries. |
| **Ingestion rate (rows/sec)** | Rows written to the endpoint's indexes per second, by operation. Standard endpoints only. See [Read the ingestion rate](#ingestion-rate). When the endpoint has two or more indexes, use the index filter to show one index. |

The following image shows the **Error rate (%)** chart with its error source filter.

### Filter errors by source

On the **Error rate (%)** chart, filter by error source:

* **All**: every failed query.
* **Embedding**: the call to the embedding model endpoint failed.
* **AI Search**: the failure came from the AI Search endpoint or from the request itself, such as an invalid filter or a permission error.
* **Uncategorized**: the source of the failure wasn't reported. This can happen on storage-optimized endpoints, for example when a query times out.

Errors that occurred before source tracking was available appear only under **All**.

### Read the ingestion rate

The **Ingestion rate (rows/sec)** chart shows rows written to the endpoint's indexes by sync pipelines and by direct upserts and deletes:

* **Inserts**, **Updates**, and **Deletes**: rows written, by operation. These include updates that don't change a row and deletes of rows that don't exist.
* **Total**: the sum of inserts, updates, and deletes.
* **Embedded**: rows embedded for Delta Sync indexes that use Databricks-managed embeddings. If a sync re-runs, the same rows count again. Embedded rows are not part of **Total**.

A rate of 0 rows per second means no writes happened in that interval. It doesn't mean the index is up to date, and infrequent small writes might not show.

The following image shows the **Ingestion rate (rows/sec)** chart for an endpoint with Delta Sync indexes.

## Retrieve metrics with the API

AI Search (formerly Vector Search) keeps the Vector Search name in the metrics API path, the CLI command group, and the Databricks SDK service. To retrieve metrics programmatically, send a `POST` request to `/api/2.0/vector-search/endpoints/{name}/metrics`. The request body contains:

* `start_time` (required): the start of the time range, as an RFC 3339 timestamp. It must be within the last 169 hours.
* `end_time`: the end of the time range, as an RFC 3339 timestamp. The default is the current time.
* `granularity_in_seconds`: the interval between data points. The minimum is 60. See [Limitations](#limitations).
* `metrics`: the list of metrics to return. Each entry has a `name`, optional `labels`, and, for latency, a `percentile`. See [Available metrics](#available-metrics).

Each label has a `name` and a `value`. The `value` is a regular expression, not an exact match. A label both filters the result and splits it by that label, so a value of `.+` returns one series for each value of the label.

The following example uses `curl` to return the failed queries per second over a one-hour window, with one series for each error source:

Bash

```
curl -X POST "https://<workspace-url>/api/2.0/vector-search/endpoints/my-endpoint/metrics" \

-H "Authorization: Bearer $DATABRICKS_TOKEN" \

-H "Content-Type: application/json" \

-d '{

"start_time": "2026-11-06T20:00:00Z",

"end_time": "2026-11-06T21:00:00Z",

"granularity_in_seconds": 60,

"metrics": [

{

"name": "IndexRequestErrorSourceCount",

"labels": [{ "name": "error_source", "value": ".+" }]

}

]

}'
```

The response contains one entry in `metric_values` for each series. Each `timestamp` is in seconds since the Unix epoch:

JSON

```
{

"metric_values": [

{

"metric": {

"name": "IndexRequestErrorSourceCount",

"labels": [{ "name": "error_source", "value": "EMBEDDING" }]

},

"values": [

{ "timestamp": 1793995200, "value": 0.0 },

{ "timestamp": 1793995260, "value": 1.5 }

]

}

]

}
```

The following example uses the [Databricks SDK for Python](/aws/en/dev-tools/sdk-python) to return the p99 query latency for the last day:

Python

```
from datetime import datetime, timedelta, timezone

from databricks.sdk import WorkspaceClient

from databricks.sdk.service.vectorsearch import Metric

w = WorkspaceClient()

end = datetime.now(timezone.utc)

start = end - timedelta(days=1)

response = w.vector_search_endpoints.retrieve_user_visible_metrics(

name="my-endpoint",

start_time=start.isoformat(),

end_time=end.isoformat(),

granularity_in_seconds=300,

metrics=[Metric(name="IndexRequestLatency", percentile=0.99)],

)

for series in response.metric_values:

print(series.metric.labels, series.values[-1])
```

The `databricks-ai-search` Python package doesn't include a metrics method. Use the Databricks SDK, the Databricks CLI, or the REST API.

The following example uses the [Databricks CLI](/aws/en/dev-tools/cli/reference/vector-search-endpoints-commands) to return the ingested rows per second, with one series for each operation. Pass the metrics with `--json`:

Bash

```
databricks vector-search-endpoints retrieve-user-visible-metrics my-endpoint --json '{

"start_time": "2026-11-06T00:00:00Z",

"metrics": [

{

"name": "IndexIngestedRows",

"labels": [{ "name": "operation", "value": ".+" }]

}

]

}'
```

The API doesn't paginate. The `page_token` request field is ignored, and the response doesn't include a `next_page_token`. Every response returns all data points in one page.

## Available metrics

### Endpoint metrics

Endpoint metrics describe the endpoint as a whole and don't accept labels.

| Metric | Unit | Description |
| --- | --- | --- |
| `EndpointHealthStatus` | State code | The endpoint state: `0` PROVISIONING, `1` ONLINE, `2` OFFLINE, `3` NOT\_READY, `4` RED\_STATE, `5` YELLOW\_STATE, `6` DELETED, `7` STOPPING, `8` STOPPED, `9` STARTING. |
| `EndpointConcurrency` | Count | The concurrency provisioned for the endpoint. |

←✕

| Metric | Unit | Description |
| --- | --- | --- |
| `EndpointHealthStatus` | State code | The endpoint state: `0` PROVISIONING, `1` ONLINE, `2` OFFLINE, `3` NOT\_READY, `4` RED\_STATE, `5` YELLOW\_STATE, `6` DELETED, `7` STOPPING, `8` STOPPED, `9` STARTING. |
| `EndpointConcurrency` | Count | The concurrency provisioned for the endpoint. |

### Query metrics

Query metrics cover query requests only.

| Metric | Unit | Description |
| --- | --- | --- |
| `IndexRequestCount` | Requests per second | The query rate. |
| `IndexRequestLatency` | Milliseconds | Query latency. Requires `percentile`: one of `0.5`, `0.75`, `0.9`, `0.95`, or `0.99`. |

←✕

| Metric | Unit | Description |
| --- | --- | --- |
| `IndexRequestCount` | Requests per second | The query rate. |
| `IndexRequestLatency` | Milliseconds | Query latency. Requires `percentile`: one of `0.5`, `0.75`, `0.9`, `0.95`, or `0.99`. |

Both metrics accept these labels:

* `request_path`: `NETWORK_OPTIMIZED_ROUTE` (optimized route) or `HIGH_LATENCY_ROUTE` (non-optimized route). The response contains one series for each route.
* `query_type`: `ANN`, `HYBRID`, or `FULL_TEXT`.
* `response_code`: the HTTP status code, such as `200` or `429`.
* `index_name`: the full index name.

### Error source metric

| Metric | Unit | Description |
| --- | --- | --- |
| `IndexRequestErrorSourceCount` | Failed queries per second | Failed queries, by the source of the failure. |

←✕

| Metric | Unit | Description |
| --- | --- | --- |
| `IndexRequestErrorSourceCount` | Failed queries per second | Failed queries, by the source of the failure. |

The `error_source` label has these values:

| Value | UI name | Meaning |
| --- | --- | --- |
| `EMBEDDING` | **Embedding** | The call to the embedding model endpoint failed. |
| `VECTOR_SEARCH` | **AI Search** | The failure came from the AI Search endpoint or from the request itself. Use `response_code` to separate caller errors such as `400` or `403` from endpoint errors. |
| `UNATTRIBUTED` | **Uncategorized** | The source of the failure wasn't reported. This can happen on storage-optimized endpoints, for example when a query times out. |

←✕

| Value | UI name | Meaning |
| --- | --- | --- |
| `EMBEDDING` | **Embedding** | The call to the embedding model endpoint failed. |
| `VECTOR_SEARCH` | **AI Search** | The failure came from the AI Search endpoint or from the request itself. Use `response_code` to separate caller errors such as `400` or `403` from endpoint errors. |
| `UNATTRIBUTED` | **Uncategorized** | The source of the failure wasn't reported. This can happen on storage-optimized endpoints, for example when a query times out. |

This metric also accepts the `response_code`, `request_path`, `query_type`, and `index_name` labels.

### 429 guidance metrics

The 429 guidance metrics apply to standard endpoints.

| Metric | Unit | Description |
| --- | --- | --- |
| `IndexRequestGuidanceCount` | Requests per second | Queries, by the cause of any 429 error. |
| `IndexRequestGuidancePeakRate` | Requests per second | The hourly peak query rate on the non-optimized route (`HIGH_LATENCY_ROUTE`). Excludes optimized-route traffic and doesn't accept labels. |

←✕

| Metric | Unit | Description |
| --- | --- | --- |
| `IndexRequestGuidanceCount` | Requests per second | Queries, by the cause of any 429 error. |
| `IndexRequestGuidancePeakRate` | Requests per second | The hourly peak query rate on the non-optimized route (`HIGH_LATENCY_ROUTE`). Excludes optimized-route traffic and doesn't accept labels. |

`IndexRequestGuidanceCount` accepts the `failure_cause` label. For a response other than 429, the value is `NONE`. For a 429 response, the value is one of:

| Value | Meaning |
| --- | --- |
| `REJECTED` | The endpoint rejected the query because its request queue was full. |
| `CIRCUIT_BREAKER` | The endpoint ran low on memory and rejected the query. |
| `CAPACITY_BLOCK` | The endpoint or index exceeded its capacity. |
| `PAGINATION` | Too many open pagination contexts. |
| `EMBEDDING_LIMIT` | The embedding model endpoint rate-limited the query. |
| `UC_LIMIT` | The query hit a Unity Catalog rate limit. |
| `TIMEOUT` | The query timed out because of overload, a slow query, or warmup. |
| `OTHER` | Any other 429 error. |

←✕

| Value | Meaning |
| --- | --- |
| `REJECTED` | The endpoint rejected the query because its request queue was full. |
| `CIRCUIT_BREAKER` | The endpoint ran low on memory and rejected the query. |
| `CAPACITY_BLOCK` | The endpoint or index exceeded its capacity. |
| `PAGINATION` | Too many open pagination contexts. |
| `EMBEDDING_LIMIT` | The embedding model endpoint rate-limited the query. |
| `UC_LIMIT` | The query hit a Unity Catalog rate limit. |
| `TIMEOUT` | The query timed out because of overload, a slow query, or warmup. |
| `OTHER` | Any other 429 error. |

`IndexRequestGuidanceCount` also accepts the `auth_type` (`OAUTH`, `TOKEN`, or `OTHER`), `num_results_bucket` (`LE_10` or `GT_10`), `request_path`, `query_type`, and `index_name` labels.

### Ingestion metrics

Ingestion metrics are available only for standard endpoints.

| Metric | Unit | Description |
| --- | --- | --- |
| `IndexIngestedRows` | Rows per second | Rows written by Delta Sync pipelines and by Direct Vector Access upserts and deletes. Accepts the `operation` label (`INSERT`, `UPDATE`, or `DELETE`) and the `index_name` label. |
| `IndexEmbedd