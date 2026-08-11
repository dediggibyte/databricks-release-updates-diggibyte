Preview

This system table is in [Public Preview](/aws/en/release-notes/release-types).

This page includes information on the alert system tables, including an outline of each table's schema. Use these tables to query your workspace [alerts](/aws/en/sql/user/alerts/) and their evaluation history directly in SQL, so you can audit alert definitions, analyze evaluation trends, and monitor alert workloads at scale.

The `system.alert` schema contains two tables:

* [`system.alert.alerts`](#alerts): The configuration of every alert, including its definition, schedule, evaluation thresholds, subscribers, and lifecycle timestamps.
* [`system.alert.alert_evaluation_history`](#evaluation-history): One row per alert evaluation, capturing the evaluated state, result values, notification delivery status, and error details.

## Requirements

By default, only users with both the account admin and metastore admin roles have access to the alert system tables. To share a table's data with a user or group, Databricks recommends creating a dynamic view for each user or group. See [Create a dynamic view](/aws/en/views/dynamic).

## Alert configuration table schema

The `system.alert.alerts` table is a slow-changing dimension table. Each row captures the configuration of an alert at a point in time, so a single alert has multiple rows when its configuration changes.

**Table path**: This system table is located at `system.alert.alerts`.

The `system.alert.alerts` table uses the following schema:

| Column name | Data type | Description | Example |
| --- | --- | --- | --- |
| `account_id` | string | The ID of the account. | `23e22ba4-87b9-4cc2` `-9770-d10b894b7118` |
| `workspace_id` | string | The ID of the workspace where the alert is defined. | `1234567890123456` |
| `alert_id` | string | The ID of the alert. | `2762099691916865` |
| `display_name` | string | The display name of the alert. | `Test Alert` |
| `owned_by` | string | The username of the alert owner. Set to `Unavailable` if the user has been deleted. | `example@databricks.com` |
| `compute` | struct | A struct that represents the compute resource attached to the alert. The `type` value is either `WAREHOUSE` or `SERVERLESS_COMPUTE`. | `{` `type: WAREHOUSE,` `cluster_id: NULL,` `warehouse_id: 802f6d5283291c0d` `}` |
| `run_as` | string | The ID of the user or Databricks service principal whose credentials are used to run the alert. | `2967555311742259` |
| `schedule` | struct | A struct that represents the alert's schedule, including its pause status, cron schedule, and time zone. | `{` `pause_status: UNPAUSED,` `quartz_cron_schedule: 0 0 10 * * ?,` `timezone_id: UTC` `}` |
| `evaluation_source` | struct | A struct that represents the source column from the query result used to evaluate the alert, including the aggregation applied to it. | `{` `aggregation: SUM,` `display: x,` `name: x` `}` |
| `evaluation_comparison_operator` | string | The operator used to compare the source value against the threshold during evaluation. For example: `GREATER_THAN`, `LESS_THAN`, and `EQUAL`. | `LESS_THAN` |
| `evaluation_threshold` | struct | A struct that represents the threshold the source value is compared against. The threshold is either a static value or another column. | `{` `value: {`  `double_value: 1.25` `}` `}` |
| `evaluation_empty_result_state` | string | The state the alert reports when the query returns an empty result. Possible values are `OK`, `TRIGGERED`, and `ERROR`. | `OK` |
| `notify_on_ok` | boolean | Whether to notify subscribers when the alert returns to the `OK` state. | `true` |
| `retrigger_seconds` | int | The number of seconds the alert waits after being triggered before it can trigger again. If `0`, the alert does not trigger again. | `0` |
| `subscriptions` | array | An array of the subscribers that receive the alert notification. Each subscriber is identified by a user email or a notification destination ID. | `[` `{`  `user_email: example@databricks.com,`  `destination_id: null` `}` `]` |
| `change_time` | timestamp | The time the configuration was last changed. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |
| `create_time` | timestamp | The time the alert was created. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |
| `delete_time` | timestamp | The time the alert was permanently deleted. Alerts moved to trash are not recorded. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |

←✕

| Column name | Data type | Description | Example |
| --- | --- | --- | --- |
| `account_id` | string | The ID of the account. | `23e22ba4-87b9-4cc2` `-9770-d10b894b7118` |
| `workspace_id` | string | The ID of the workspace where the alert is defined. | `1234567890123456` |
| `alert_id` | string | The ID of the alert. | `2762099691916865` |
| `display_name` | string | The display name of the alert. | `Test Alert` |
| `owned_by` | string | The username of the alert owner. Set to `Unavailable` if the user has been deleted. | `example@databricks.com` |
| `compute` | struct | A struct that represents the compute resource attached to the alert. The `type` value is either `WAREHOUSE` or `SERVERLESS_COMPUTE`. | `{` `type: WAREHOUSE,` `cluster_id: NULL,` `warehouse_id: 802f6d5283291c0d` `}` |
| `run_as` | string | The ID of the user or Databricks service principal whose credentials are used to run the alert. | `2967555311742259` |
| `schedule` | struct | A struct that represents the alert's schedule, including its pause status, cron schedule, and time zone. | `{` `pause_status: UNPAUSED,` `quartz_cron_schedule: 0 0 10 * * ?,` `timezone_id: UTC` `}` |
| `evaluation_source` | struct | A struct that represents the source column from the query result used to evaluate the alert, including the aggregation applied to it. | `{` `aggregation: SUM,` `display: x,` `name: x` `}` |
| `evaluation_comparison_operator` | string | The operator used to compare the source value against the threshold during evaluation. For example: `GREATER_THAN`, `LESS_THAN`, and `EQUAL`. | `LESS_THAN` |
| `evaluation_threshold` | struct | A struct that represents the threshold the source value is compared against. The threshold is either a static value or another column. | `{` `value: {`  `double_value: 1.25` `}` `}` |
| `evaluation_empty_result_state` | string | The state the alert reports when the query returns an empty result. Possible values are `OK`, `TRIGGERED`, and `ERROR`. | `OK` |
| `notify_on_ok` | boolean | Whether to notify subscribers when the alert returns to the `OK` state. | `true` |
| `retrigger_seconds` | int | The number of seconds the alert waits after being triggered before it can trigger again. If `0`, the alert does not trigger again. | `0` |
| `subscriptions` | array | An array of the subscribers that receive the alert notification. Each subscriber is identified by a user email or a notification destination ID. | `[` `{`  `user_email: example@databricks.com,`  `destination_id: null` `}` `]` |
| `change_time` | timestamp | The time the configuration was last changed. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |
| `create_time` | timestamp | The time the alert was created. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |
| `delete_time` | timestamp | The time the alert was permanently deleted. Alerts moved to trash are not recorded. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |

## Alert evaluation history table schema

The `system.alert.alert_evaluation_history` table records one row for each alert evaluation, capturing the evaluated state and related statistics.

**Table path**: This system table is located at `system.alert.alert_evaluation_history`.

The `system.alert.alert_evaluation_history` table uses the following schema:

| Column name | Data type | Description | Example |
| --- | --- | --- | --- |
| `account_id` | string | The ID of the account. | `23e22ba4-87b9-4cc2` `-9770-d10b894b7118` |
| `workspace_id` | string | The ID of the workspace where the alert is defined. | `1234567890123456` |
| `alert_id` | string | The ID of the evaluated alert. Joins to `alert_id` in `system.alert.alerts`. | `2762099691916865` |
| `job_id` | string | The ID of the job that ran the alert. Joins to `job_id` in `system.lakeflow.jobs`. `NULL` when the alert runs on its own schedule instead of as part of a job. Use a `LEFT JOIN` when you query against `system.lakeflow.jobs`. | `906851285941474` |
| `task_key` | string | The reference key for the task within the job. Joins to `task_key` in `system.lakeflow.job_tasks`. `NULL` when the alert runs on its own schedule instead of as part of a job. Use a `LEFT JOIN` when you query against `system.lakeflow.job_tasks`. | `evaluate_alert` |
| `alert_run_id` | string | The ID of the alert evaluation run. | `4104302562320643` |
| `evaluated_state` | string | The evaluated state of the alert. Possible values are `OK`, `TRIGGERED`, and `ERROR`. | `TRIGGERED` |
| `evaluated_source_result` | struct | A struct that represents the source value produced by the evaluation. | `{` `double_value: 1.25` `}` |
| `evaluated_threshold_result` | struct | A struct that represents the threshold value from the evaluation, or the static value set in the alert configuration. | `{` `double_value: 1.25` `}` |
| `error_code` | string | The error code if the evaluation failed with an error. | `INTERNAL_ERROR` |
| `error_message` | string | The user-visible error message if the evaluation failed with an error. | `Query execution failed` |
| `notified_subscriptions` | array | An array of the subscribers that were successfully notified. Each subscriber is identified by a user email or a notification destination ID. | `[` `{`  `user_email: example@databricks.com,`  `destination_id: null` `}` `]` |
| `failed_subscriptions` | array | An array of the subscribers whose notifications failed to send. Each subscriber is identified by a user email or a notification destination ID. | `[` `{`  `user_email: example@databricks.com,`  `destination_id: null` `}` `]` |
| `start_time` | timestamp | The time the evaluation started. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |
| `end_time` | timestamp | The time the evaluation ended. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |

←✕

| Column name | Data type | Description | Example |
| --- | --- | --- | --- |
| `account_id` | string | The ID of the account. | `23e22ba4-87b9-4cc2` `-9770-d10b894b7118` |
| `workspace_id` | string | The ID of the workspace where the alert is defined. | `1234567890123456` |
| `alert_id` | string | The ID of the evaluated alert. Joins to `alert_id` in `system.alert.alerts`. | `2762099691916865` |
| `job_id` | string | The ID of the job that ran the alert. Joins to `job_id` in `system.lakeflow.jobs`. `NULL` when the alert runs on its own schedule instead of as part of a job. Use a `LEFT JOIN` when you query against `system.lakeflow.jobs`. | `906851285941474` |
| `task_key` | string | The reference key for the task within the job. Joins to `task_key` in `system.lakeflow.job_tasks`. `NULL` when the alert runs on its own schedule instead of as part of a job. Use a `LEFT JOIN` when you query against `system.lakeflow.job_tasks`. | `evaluate_alert` |
| `alert_run_id` | string | The ID of the alert evaluation run. | `4104302562320643` |
| `evaluated_state` | string | The evaluated state of the alert. Possible values are `OK`, `TRIGGERED`, and `ERROR`. | `TRIGGERED` |
| `evaluated_source_result` | struct | A struct that represents the source value produced by the evaluation. | `{` `double_value: 1.25` `}` |
| `evaluated_threshold_result` | struct | A struct that represents the threshold value from the evaluation, or the static value set in the alert configuration. | `{` `double_value: 1.25` `}` |
| `error_code` | string | The error code if the evaluation failed with an error. | `INTERNAL_ERROR` |
| `error_message` | string | The user-visible error message if the evaluation failed with an error. | `Query execution failed` |
| `notified_subscriptions` | array | An array of the subscribers that were successfully notified. Each subscriber is identified by a user email or a notification destination ID. | `[` `{`  `user_email: example@databricks.com,`  `destination_id: null` `}` `]` |
| `failed_subscriptions` | array | An array of the subscribers whose notifications failed to send. Each subscriber is identified by a user email or a notification destination ID. | `[` `{`  `user_email: example@databricks.com,`  `destination_id: null` `}` `]` |
| `start_time` | timestamp | The time the evaluation started. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |
| `end_time` | timestamp | The time the evaluation ended. Time zone information is recorded at the end of the value with `+00:00` representing UTC. | `2023-01-01T01:01:01.123+00:00` |

## Sample queries

The following sample queries show common ways to analyze alert configuration and evaluation history. Each query uses [named parameter markers](/aws/en/sql/language-manual/sql-ref-parameter-marker) for the alert and workspace IDs, so you're prompted for the values when you run the query.

### Find the most recent evaluation for an alert

This query returns the latest configuration of a specific alert alongside its most recent evaluation.

SQL

```
SELECT  
  c.alert_id,  
  c.display_name,  
  c.compute,  
  c.schedule.quartz_cr