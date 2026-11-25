Beta

This feature is in [Beta](/aws/en/release-notes/release-types).

A one-time migration copies an existing Postgres database into a branch in a Lakebase project. You choose the target project and branch, and Lakebase copies the source database's roles, schema, and data into it.

## When to use a migration

Migrate your database when you want a single, complete copy of it and you can cut over at one point in time.

Use a different method in these cases:

* To keep the target in sync with ongoing changes on the source until you cut over, use [logical replication](/aws/en/oltp/projects/logical-replication).
* To export a database to a file that you store outside Lakebase, use [Postgres pg\_dump & pg\_restore](/aws/en/oltp/projects/pg-dump-restore).

To compare all the ways to move data in and out of Lakebase, see [Move data in and out of Lakebase](/aws/en/oltp/projects/move-data-in-and-out).

## How a migration works

You can create and manage migrations in the Lakebase App, or programmatically with the Python SDK, Java SDK, Databricks CLI, curl, or Go SDK. Where an operation is available more than one way, this page shows the instructions together as tabs. Migrations don't require a separate enablement step.

The programmatic examples require Python SDK 0.163.0, Java SDK 0.177.0, or Databricks CLI 1.26.0 (or above). The migration commands are hidden from the `databricks postgres --help` list, but `databricks postgres <command> --help` shows each command's usage.

A migration runs in these stages:

| Stage | What happens |
| --- | --- |
| [Create](#create-migration) | You name the migration, choose a Unity Catalog connection to the source database, and list the databases to copy. Creating the migration starts the first assessment. |
| [Assess](#review-assessment) | Lakebase runs a set of checks against the source. Each check passes, raises a warning, or blocks the migration. See [Lakebase migration assessment checks](/aws/en/oltp/projects/migration-assessment-checks). |
| [Resolve](#review-assessment) | You fix blockers on the source and re-run the assessment, or acknowledge the warnings. |
| [Start](#start-migration) | You choose the target project and branch, and then start the migration. Lakebase loads the roles and schema, and then copies the data one database at a time. |
| [Finish](#after-migration) | You set role passwords, re-apply ownership and privileges, and point your applications at Lakebase. |

←✕

| Stage | What happens |
| --- | --- |
| [Create](#create-migration) | You name the migration, choose a Unity Catalog connection to the source database, and list the databases to copy. Creating the migration starts the first assessment. |
| [Assess](#review-assessment) | Lakebase runs a set of checks against the source. Each check passes, raises a warning, or blocks the migration. See [Lakebase migration assessment checks](/aws/en/oltp/projects/migration-assessment-checks). |
| [Resolve](#review-assessment) | You fix blockers on the source and re-run the assessment, or acknowledge the warnings. |
| [Start](#start-migration) | You choose the target project and branch, and then start the migration. Lakebase loads the roles and schema, and then copies the data one database at a time. |
| [Finish](#after-migration) | You set role passwords, re-apply ownership and privileges, and point your applications at Lakebase. |

A migration is a one-time copy, not continuous replication. It brings most of your database across automatically and leaves a few things for you to set up on the target:

| Copied automatically | You configure manually |
| --- | --- |
| Roles (names and memberships) | Role passwords |
| Schema, table data, and sequence values | Object ownership and privileges (`GRANT`s) |

←✕

| Copied automatically | You configure manually |
| --- | --- |
| Roles (names and memberships) | Role passwords |
| Schema, table data, and sequence values | Object ownership and privileges (`GRANT`s) |

For the complete list of what is and isn't copied, see [What a migration copies](#what-is-copied).

## Prerequisites

* A workspace in a region where migrations are available. See [Region availability](#availability).
* A Unity Catalog connection of type PostgreSQL to the source database that uses username and password authentication, and the [USE CONNECTION](/aws/en/data-governance/unity-catalog/access-control/privileges-reference#use-connection) privilege on it. In the Lakebase App, you can create the connection while you create the migration. The connection uses TLS with full certificate verification. See [Run federated queries on PostgreSQL](/aws/en/query-federation/postgresql).
* The `CAN MANAGE` permission on the target Lakebase project. See [Manage project permissions](/aws/en/oltp/projects/manage-project-permissions).
* A target project that runs PostgreSQL 17 or above, with a branch that has at least one compute. See [Manage projects](/aws/en/oltp/projects/manage-projects).
* Target database names that don't already exist on the target branch. By default, each target database uses the name of its source database.

For the source requirements that the assessment checks, such as supported PostgreSQL versions and the 500 GB limit on each source database, see [Lakebase migration assessment checks](/aws/en/oltp/projects/migration-assessment-checks).

## Step 1: Create a migration

Creating a migration saves its configuration and starts the first assessment. Each migration copies between 1 and 10 databases from one source.

* UI
* Python SDK
* Java SDK
* CLI
* curl

1. In the Lakebase App, click **Migrations** in the sidebar.
2. Click **Create migration**. If you don't have any migrations yet, click **Create new migration**.
3. On the **Connect to source** step, enter a name for the migration. The name must be 1 to 63 characters, start with a lowercase letter, and contain only lowercase letters, numbers, and hyphens.
4. For the migration type, select **One-time copy**.
5. Connect to the source database:

   * To create a Unity Catalog connection, select **Create new connection**, and then enter the connection name, host, port, user, and password.
   * To use a Unity Catalog connection that already exists, select the option to use an existing connection, and then select the connection. Only PostgreSQL connections are listed.

   The following image shows the **Connect to source** step with **One-time copy** and an existing connection selected.
6. On the **Map databases** step, enter the name of the first database to copy in **Source database name**. To copy more databases, click **Add database** for each one. To give a copy a different name, enter the name in **Lakebase database name**. Leave the field empty to keep the original name.
7. On the **Review** step, confirm the source connection and databases, and then click **Create migration & start assessment**.

`create_migration` takes the migration ID and a `Migration` separately, and returns a long-running operation. Call `.wait()` to block until the first assessment finishes:

Python

```
from databricks.sdk import WorkspaceClient

from databricks.sdk.service.postgres import DatabaseMapping, Migration, MigrationType

w = WorkspaceClient()

migration = w.postgres.create_migration(

migration_id="my-migration",

migration=Migration(

source_connection="my_pg_connection",

database_mappings=[

DatabaseMapping(source_database="app"),

DatabaseMapping(source_database="analytics", target_database="analytics_copy"),

],

migration_type=MigrationType.MIGRATION_TYPE_ONE_TIME_COPY,

),

).wait()

print(f"Migration created: {migration.name}")
```

To create a migration and wait for the first assessment to finish, run the following:

Java

```
import com.databricks.sdk.WorkspaceClient;

import com.databricks.sdk.service.postgres.*;

import java.util.List;

WorkspaceClient w = new WorkspaceClient();

Migration migration = new Migration()

.setSourceConnection("my_pg_connection")

.setMigrationType(MigrationType.MIGRATION_TYPE_ONE_TIME_COPY)

.setDatabaseMappings(List.of(

new DatabaseMapping().setSourceDatabase("app"),

new DatabaseMapping()

.setSourceDatabase("analytics")

.setTargetDatabase("analytics_copy")));

w.postgres().createMigration(

new CreateMigrationRequest()

.setMigrationId("my-migration")

.setMigration(migration)

).waitForCompletion();
```

The migration ID is a positional argument. The source connection, migration type, and database mappings go in the `--json` body. The command waits until the first assessment finishes:

Bash

```
databricks postgres create-migration my-migration \

--json '{

"source_connection": "my_pg_connection",

"migration_type": "MIGRATION_TYPE_ONE_TIME_COPY",

"database_mappings": [

{"source_database": "app"},

{"source_database": "analytics", "target_database": "analytics_copy"}

]

}'
```

Creating a migration is a long-running operation. The operation completes when the first assessment finishes.

1. Send the create request. The `migration_id` goes in the query string. A mapping without a `target_database` keeps the source database name:

   Bash

   ```
   curl -X POST "$WORKSPACE/api/2.0/postgres/migrations?migration_id=my-migration" \

   -H "Authorization: Bearer ${DATABRICKS_TOKEN}" \

   -H "Content-Type: application/json" \

   -d '{

   "source_connection": "my_pg_connection",

   "database_mappings": [

   {"source_database": "app"},

   {"source_database": "analytics", "target_database": "analytics_copy"}

   ],

   "migration_type": "MIGRATION_TYPE_ONE_TIME_COPY"

   }'
   ```

   The response is a long-running operation:

   JSON

   ```
   {

   "name": "migrations/my-migration/operations/create",

   "done": false

   }
   ```
2. Poll the operation until `done` is `true`:

   Bash

   ```
   curl "$WORKSPACE/api/2.0/postgres/migrations/my-migration/operations/create" \

   -H "Authorization: Bearer ${DATABRICKS_TOKEN}" | jq
   ```

## Step 2: Review the assessment

A migration assessment runs a check for each source requirement and returns one of these verdicts for each check: Pass, Warning, Blocker, Unsupported, or Error. Any Blocker, Unsupported, or Error result blocks the migration. For the full list of checks, see [Lakebase migration assessment checks](/aws/en/oltp/projects/migration-assessment-checks).

To review an assessment in the Lakebase App:

1. Click **Migrations** in the sidebar and select the migration.
2. On the **Overview** tab, review the **Assessments** card. It shows the number of blockers, warnings, and passes, and lists the checks with the most severe results first. To see every check, click **See more** or open the **Assessments** tab.

   The following image shows the **Assessments** card for an assessment that found two warnings and no blockers.
3. If the assessment found blockers, fix them on the source database, and then click **Re-run assessment**.
4. If the assessment found only warnings, click **Review warnings**. Select **I have reviewed and acknowledge all warnings.**, and then click **Acknowledge warnings**.

After every check passes, or after you acknowledge the warnings, the migration's status changes to **Ready to start**.

An assessment expires 24 hours after it completes. If the latest assessment expired, re-run it before you start the migration. After the first assessment completes, you can't change the migration's source connection or database mappings. To copy different databases, create a new migration.

To get assessment results, re-run an assessment, or acknowledge warnings programmatically, use the following. Assessments are listed newest first, and each one is named `migrations/{migration_id}/assessments/{n}`, where `n` is the attempt number.

* Python SDK
* Java SDK
* CLI
* curl

To print the result of each check in an assessment, run the following. Each check has a `check_id`, a `verdict`, and, for checks that don't pass, a `reason`:

Python

```
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

assessment = w.postgres.get_assessment(name="migrations/my-migration/assessments/1")

for check in assessment.checks or []:

print(check.check_id, check.verdict, check.reason)

for assessment in w.postgres.list_assessments(parent="migrations/my-migration"):

print(assessment.name)
```

To re-run the assessment and wait for it to finish, run the following:

Python

```
w.postgres.assess_migration(name="migrations/my-migration").wait()
```

To acknowledge the warnings on an assessment, run the following. The call completes immediately:

Python

```
w.postgres.acknowledge_assessment_warnings(name="migrations/my-migration/assessments/1")
```

To print the result of each check in an assessment, run the following:

Java

```
import com.databricks.sdk.WorkspaceClient;

import com.databricks.sdk.service.postgres.*;

WorkspaceClient w = new WorkspaceClient();

Assessment assessment = w.postgres().getAssessment("migrations/my-migration/assessments/1");

if (assessment.getChecks() != null) {

for (AssessmentCheck check : assessment.getChecks()) {

System.out.println(check.getCheckId() + " " + check.getVerdict() + " " + check.getReason());

}

}

for (Assessment a : w.postgres().listAssessments("migrations/my-migration")) {

System.out.println(a.getName());

}
```

To re-run the assessment and wait for it to finish, run the following:

Java

```
w.postgres().assessMigration(

new AssessMigrationRequest().setName("migrations/my-migration")

).waitForCompletion();
```

To acknowledge the warnings on an assessment, run the following. The call completes immediately:

Java

```
w.postgres().acknowledgeAssessmentWarnings(

new AcknowledgeAssessmentWarningsRequest()

.setName("migrations/my-migration/assessments/1"));
```

To list the assessments for a migration, run the following:

Bash

```
databricks postgres list-assessments migrations/my-migration --output json
```

To get one assessment, run the following:

Bash

```
databricks postgres get-assessment migrations/my-migration/assessments/1 --o