On this page

Last updated on **Jun 29, 2026**

Use a SQL alert task to evaluate a Databricks SQL alert as part of a job. SQL alert tasks allow you to integrate alert-based monitoring into your data pipelines, enabling automated condition checks and notifications alongside other job tasks. To learn more about Databricks SQL alerts, see [Databricks SQL alerts](/aws/en/sql/user/alerts/).

## Requirements[​](#requirements "Direct link to requirements")

To use the SQL alert task, you must meet the following prerequisites:

* You must have an existing Databricks SQL alert in your workspace. To create an alert, see [Create an alert](/aws/en/sql/user/alerts/create#create-alert).
* You must have at least CAN RUN permission on the alert you want to use.
* You must have access to a [serverless or pro SQL warehouse](/aws/en/compute/sql-warehouse/warehouse-types).

## Configure a SQL alert task[​](#configure-a-sql-alert-task "Direct link to configure-a-sql-alert-task")

The jobs UI displays options dynamically based on other configured settings. To configure a `SQL Alert` task:

1. In your workspace, click  **Jobs & Pipelines** in the sidebar.
2. Click **Create**, then **Job**.
3. Click **Add another task type**. Search for **SQL Alert** and click the tile to select it.
4. Enter a **Task name**.
5. In the **Alert** drop-down menu, select the Databricks SQL alert that you want to evaluate.
6. (Optional) In the **SQL warehouse** drop-down menu, select the SQL warehouse to use for running the alert query. If not set, the alert's internal warehouse is used. You must use a serverless or pro SQL warehouse for SQL alert tasks.
7. (Optional) In the **Subscribers** drop-down, choose the users and notification destinations that should receive notifications with the alert results. If not set, the alert's internal subscribers (if applicable) receive notifications. To customize the notification subject and body, including query results, configure the notification template on the underlying Databricks SQL alert. See [Notification templates](/aws/en/sql/user/alerts/create#notification-templates).
8. (Optional) Use **Notifications** to notify email addresses or webhooks when runs of this task begin, complete, or fail:
   1. Click  **Add** to open the **Task notifications** dialog.
   2. Click **Add notification** to add a new notification, or edit an existing one.
   3. From the **Destination** drop-down menu, choose a destination. If the destination you want isn't available and you have the appropriate permissions, click  **Add new system destination** to set up a new one. You must be a workspace admin to add a system destination. See [Manage notification destinations](/aws/en/admin/workspace-settings/notification-destinations).
   4. Click **Save** to apply your settings.
9. (Optional) To configure **Duration threshold** or **Retries**, see  [Advanced task settings](/aws/en/jobs/configure-task#advanced).
10. Click **Save task**.

To edit, clone, disable, or delete this task, see [Configure and edit tasks in Lakeflow Jobs](/aws/en/jobs/configure-task).

## SQL alert task behavior[​](#sql-alert-task-behavior "Direct link to sql-alert-task-behavior")

When a job runs a SQL alert task, the following occurs:

1. The alert's query executes on the specified SQL warehouse.
2. The alert condition is evaluated against the query results.
3. Subscribers configured on the task receive notifications based on the alert outcome.

The SQL alert task reports one of the following statuses:

* **Succeeded**: The alert was evaluated successfully, regardless of whether the alert condition was triggered or not.
* **Failed**: An error occurred during alert evaluation, such as a SQL warehouse connectivity issue or a query error.

note

The SQL alert task evaluates the alert independently from any schedule configured on the alert itself. Schedules on the underlying alert are not affected by the job run.

## Limitations[​](#limitations "Direct link to limitations")

* SQL alert tasks do not support parameters. If you need to use parameterized queries, consider using a [SQL task](/aws/en/jobs/tasks/sql) instead.
* SQL alert tasks support only Databricks SQL alerts. Legacy alerts are not supported.