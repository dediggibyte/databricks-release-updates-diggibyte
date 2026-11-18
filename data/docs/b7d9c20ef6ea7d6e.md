Migrate your workloads from classic compute to serverless compute. Serverless compute handles provisioning, scaling, runtime upgrades, and optimization automatically.

Most classic workloads can migrate with minimal or no code changes. For example, workloads that use [`df.cache()` and `df.persist()`](/aws/en/compute/serverless/dataframe-cache) mostly migrate without code changes. This page focuses on those workloads. Certain workloads that depend on R or Scala notebooks require classic compute and can't migrate to serverless. For a full list of current limitations, see [Serverless compute limitations](/aws/en/compute/serverless/limitations).

## Migrate with Genie Migrate for Serverless

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). Workspace administrators can enable it from the **Previews** page by opting into the **Compute Agent** preview. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

Genie Migrate for Serverless is an agent that migrates a single notebook or job to serverless compute. The agent reviews the workload's environment, libraries, Spark configurations, tags, and code, then proposes each change as an individual suggestion for you to accept or reject. Accepted changes are applied in place and can be rolled back.

Use Genie Code to migrate a notebook or job interactively, or use the Databricks CLI to migrate jobs in the background, including many jobs from a script. See [Migrate jobs with the Databricks CLI](#agent-migrate-cli).

### What the agent reviews and changes

| Area | What the agent does |
| --- | --- |
| Environment and libraries | Translates library installs into a serverless environment specification, including `%pip` installs, cluster init scripts, cluster libraries on jobs, and references to a private package index. |
| Environment variables | Translates cluster environment variables to their serverless equivalents, preserving workspace secret references and omitting platform-managed values. |
| Data and storage access | Rewrites serverless-incompatible paths, such as local disk, `dbfs:/`, and mount paths, to Unity Catalog volumes. The agent applies unambiguous rewrites automatically and asks you to choose a volume when the target is ambiguous. |
| Spark configurations | Classifies each Spark configuration, comments out configurations that are safe to drop, and flags and removes configurations that serverless does not support. Covers both cluster-attached and in-notebook configurations. |
| Workload code | Rewrites code that serverless does not support into compatible equivalents, such as RDD operations rewritten to DataFrame operations, and adjusts code for ANSI-mode SQL behavior on serverless. |
| Tags | Translates custom cluster tags, such as a cost-center tag, to their serverless equivalents. |
| Performance mode | Suggests a performance mode based on the cluster's configuration. See [Choose a performance mode](#choose-a-performance-mode). |

←✕

| Area | What the agent does |
| --- | --- |
| Environment and libraries | Translates library installs into a serverless environment specification, including `%pip` installs, cluster init scripts, cluster libraries on jobs, and references to a private package index. |
| Environment variables | Translates cluster environment variables to their serverless equivalents, preserving workspace secret references and omitting platform-managed values. |
| Data and storage access | Rewrites serverless-incompatible paths, such as local disk, `dbfs:/`, and mount paths, to Unity Catalog volumes. The agent applies unambiguous rewrites automatically and asks you to choose a volume when the target is ambiguous. |
| Spark configurations | Classifies each Spark configuration, comments out configurations that are safe to drop, and flags and removes configurations that serverless does not support. Covers both cluster-attached and in-notebook configurations. |
| Workload code | Rewrites code that serverless does not support into compatible equivalents, such as RDD operations rewritten to DataFrame operations, and adjusts code for ANSI-mode SQL behavior on serverless. |
| Tags | Translates custom cluster tags, such as a cost-center tag, to their serverless equivalents. |
| Performance mode | Suggests a performance mode based on the cluster's configuration. See [Choose a performance mode](#choose-a-performance-mode). |

### Requirements

* Workspace admin access is recommended to ensure a complete migration. This is because the agent also inspects workspace-level global init scripts beyond the target workload. You might be able to migrate if you have `CAN MANAGE` permission on the workload, but without admin permissions, it can result in missing libraries, environment settings, or tags.
* Confirm you have access to the agent. Type `/compute` in Genie Code. `/compute` should appear in the autocomplete menu. If it doesn't appear, a workspace admin must enable the preview in your workspace.

### Migrate a notebook

1. Open the notebook you want to migrate.
2. Open Genie Code and run `/compute migrate to serverless` from the `/` command palette.
3. Review the agent's findings. The agent scans the notebook's environment, libraries, and code, and proposes a change for each item that needs one, such as moving a library install into an environment specification or rewriting a code cell to run on serverless.
4. Accept or reject each proposed change.
5. Apply the changes you accepted. They are written to the notebook in place.
6. Attach the notebook to serverless and run it to confirm it behaves as you expect. See [Verify a migrated workload](#agent-verifying).

### Migrate a job

1. Open the job you want to migrate.
2. Open Genie Code and run `/compute migrate to serverless` from the `/` command palette.
3. The agent clones your job and attempts to migrate the cloned job to serverless.
4. Review the agent's findings. For a multi-task job, the agent enumerates every task and its per-task cluster configuration, and proposes changes for each while preserving the job's schedule.
5. Accept or reject each proposed change across the migration surface: environment and libraries, Spark configurations, and any workload code that must change.
6. Apply the changes you accepted. The job's compute is switched to serverless.
7. Run the job on serverless and confirm the results. See [Verify a migrated workload](#agent-verifying).
8. Optionally, as a final step, the agent promotes the migrated clone. It copies the clone's configuration and notebooks back onto your original job in place (keeping the same job ID, schedule, and permissions), then deletes the clone. If you skip promotion, your original job keeps its schedule and keeps running on classic compute. The clone has no schedule or triggers, so it runs only when you start it.

### Migrate jobs with the Databricks CLI

Use the `compute-migrations` command group in the Databricks CLI to run Genie Migrate for Serverless on a job in the background, without an open Genie Code session. You can start migrations for many jobs from a script and review each one when it is ready.

The Databricks CLI path has the following requirements:

* A workspace admin has enabled the **Compute Agent** preview. Without it, every `compute-migrations` command fails with `PERMISSION_DENIED`.
* Databricks CLI version 1.24.0 or above. See [Install or update the Databricks CLI](/aws/en/dev-tools/cli/install).
* `CAN MANAGE` permission on each job you migrate.

The agent backs up the job, then builds a serverless working copy. The working copy is a new job named `[Serverless Migration - <timestamp>] <job name>` that runs copies of the job's notebooks and files. It has no schedule or triggers, so it runs only when you start it or when Databricks runs it for validation. Your original job is not changed until you approve the migration.

warning

A validation run is not isolated. The working copy runs against the same tables, volumes, checkpoints, and external systems as the original job. If the job writes to production tables, sends notifications, calls external APIs, or advances streaming checkpoints, the validation run does too. Set `run_validation` only for jobs where one extra run is safe. You can't change this setting after you create the migration.

Don't edit the original job or the working copy while a migration is in progress. Approving the migration replaces the original job's settings and files with the working copy's.

1. Start a migration for the job:

   Bash

   ```
   databricks compute-migrations create -o json --request-id "<uuid>" --json '{

   "asset_type": "JOB",

   "asset_uri": "jobs/<job-id>",

   "auto_approve": false,

   "run_validation": false

   }'
   ```

   The response includes the migration ID. Use a new `request-id` for each job, and reuse it if you retry after a timeout so that you don't create a duplicate migration. You can't change `auto_approve` or `run_validation` after you create the migration.
2. Check the state of the migration with `databricks compute-migrations get <migration-id> -o json`. Planning and building the working copy usually take several minutes. To check many migrations, use `list`, then confirm each one with `get` before you act on it.
3. When the migration reaches `TRANSLATION_READY`, review the working copy. `migration_report.primary_asset.id` is the working copy's job ID. Compare its settings and code with the original job, then run `approve-migration-translation` or `reject-migration-translation` with the `--etag` from your latest `get`.
4. If you set `run_validation`, Databricks runs the working copy one time and records the result in `validation_report`. The migration moves to `MIGRATION_REVIEW` whether the run succeeds or fails, so check `validation_report.passed` before you approve.
5. When the migration reaches `MIGRATION_REVIEW`, review the working copy and the validation result, then run `approve-migration-execution` or `reject-migration-execution` with the `--etag` from your latest `get`. Approving applies the working copy's settings and files to the original job, keeping its job ID, schedule, and permissions.
6. When the migration reaches `MIGRATION_COMPLETE`, the original job has been changed. Verify it right away. See [Verify a migrated workload](#agent-verifying).
7. After you verify the original job, delete the working copy job. `migration_report.secondary_assets` lists notebooks the working copy runs. Delete them only after you confirm that the original job doesn't reference them.

Each reject command requires a rejection reason, which you pass after the migration ID. For example:

Bash

```
databricks compute-migrations reject-migration-translation <migration-id> "Keep the existing output table names." --etag <etag>
```

Give a specific reason. The agent revises the working copy and returns it for review. If you reject a migration repeatedly, it fails.

The following table lists the `compute-migrations` commands:

| Command | Description |
| --- | --- |
| `create` | Starts a migration for a job. Fails with `ALREADY_EXISTS` if the job has a migration in progress or one that already succeeded. |
| `get`, `list` | Returns the state, reports, and `etag` of one migration or all migrations. |
| `approve-migration-translation`, `reject-migration-translation` | Approves or rejects the working copy in the `TRANSLATION_READY` state. Setting `auto_approve` at creation skips this review. |
| `approve-migration-execution`, `reject-migration-execution` | Approves or rejects the migration in the `MIGRATION_REVIEW` state. Approving changes the original job. |
| `cancel-migration` | Stops a migration. Cancellation does not undo changes already applied to the original job or the side effects of a validation run. |
| `delete` | Removes the migration record. Does not roll back changes or remove the working copy or backup. A migration that failed or was canceled already releases the job, so you don't need to delete it before you start a new migration. |

←✕

| Command | Description |
| --- | --- |
| `create` | Starts a migration for a job. Fails with `ALREADY_EXISTS` if the job has a migration in progress or one that already succeeded. |
| `get`, `list` | Returns the state, reports, and `etag` of one migration or all migrations. |
| `approve-migration-translation`, `reject-migration-translation` | Approves or rejects the working copy in the `TRANSLATION_READY` state. Setting `auto_approve` at creation skips this review. |
| `approve-migration-execution`, `reject-migration-execution` | Approves or rejects the migration in the `MIGRATION_REVIEW` state. Approving changes the original job. |
| `cancel-migration` | Stops a migration. Cancellation does not undo changes already applied to the original job or the side effects of a validation run. |
| `delete` | Removes the migration record. Does not roll back changes or remove the working copy or backup. A migration that failed or was canceled already releases the job, so you don't need to delete it before you start a new migration. |

Pass `--etag` from your latest `get` with each approve, reject, or cancel command. If the migration changed since you read it, the command fails with `ABORTED` instead of acting on a state you have not reviewed. If the agent can't migrate the job, the migration moves to `NOT_SUPPORTED` or `FAILED`, and `state_history` explains why.

### Verify a migrated workload

The agent proposes and applies changes, but does not verify your workload's output. A validation run with the Databricks CLI checks only that the run succeeds. Always run a migrated workload on serverless and confirm the results before you rely on it, especially for workloads that write to production tables. If the agent proposes a change that looks wrong, reject it and send us feedback so we can improve the agent. See [Submit product feedback](/aws/en/resources/ideas).

tip

While you validate a migrated workload, run it in performance