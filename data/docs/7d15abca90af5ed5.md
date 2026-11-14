Beta

This feature is in [Beta](/aws/en/release-notes/release-types).

To participate in the Beta, contact your Databricks account team.

In Unity Catalog, each pipeline flow is a securable object. Flow owners and users with `MANAGE` on a flow can grant other users privileges to read, refresh, reset, or manage individual flows.

## Overview

A [flow](/aws/en/ldp/concepts/flows) is a query that loads and processes data incrementally, either as a batch or as a stream, into a target. In Unity Catalog, each flow is a securable object that lives in a schema, alongside the tables it writes to. A flow uses the three-level name `catalog.schema.flow_name`.

A flow in Unity Catalog has the following characteristics:

* **Pipeline:** A flow belongs to the Lakeflow pipeline that defines it and is updated by that pipeline.
* **Target:** A flow writes to a single target streaming table or materialized view. A target table can receive data from more than one flow.
* **Flow type:** A flow records how it processes data, such as append, Auto CDC, or replace where. See [Types of flows](/aws/en/ldp/concepts/flows#flow-types).

Because flows are securable objects, you can grant privileges on an individual flow. For example, you can let a user refresh a flow or reset its checkpoint without granting broader access to the pipeline or the target table.

## How it works

Flows follow the same [permission model](/aws/en/data-governance/unity-catalog/access-control/permissions-concepts) as other objects in a schema:

* **Usage privileges:** To access a flow, a user must have `USE CATALOG` on the parent catalog and `USE SCHEMA` on the parent schema, in addition to a privilege on the flow. See [Usage privileges](/aws/en/data-governance/unity-catalog/access-control/permissions-concepts#usage-privileges).
* **Inheritance:** Flow privileges granted on a catalog or schema apply to all current and future flows in that catalog or schema. See [Privilege inheritance](/aws/en/data-governance/unity-catalog/access-control/permissions-concepts#inheritance).
* **Ownership:** The owner of a flow has all privileges on it. The pipeline manages the flow's ownership.

### Flow privileges

The following privileges apply to flows:

| Privilege | Granted on | Allows the user to |
| --- | --- | --- |
| `ALL PRIVILEGES` | Flow, schema, or catalog | Perform all capabilities on the flow: `READ FLOW`, `REFRESH FLOW`, `WRITE FLOW`, and `APPLY TAG`. Does not include `MANAGE` or `READ METADATA`. See [ALL PRIVILEGES](/aws/en/data-governance/unity-catalog/access-control/privileges-reference#all-privileges). |
| `CREATE FLOW` | Catalog or schema | Create a flow in the schema. The user needs `USE CATALOG`, `USE SCHEMA`, and the applicable creation privilege: `CREATE TABLE` when the flow is created implicitly with a new target table, or `CREATE FLOW` when the flow is defined explicitly. Adding a flow to an existing target also requires `MODIFY` on the target table. |
| `READ FLOW` | Flow, schema, or catalog | Describe the flow and read its definition and state. |
| `REFRESH FLOW` | Flow, schema, or catalog | Refresh the flow. |
| `WRITE FLOW` | Flow, schema, or catalog | Reset or rewind the flow's streaming checkpoint. |
| `APPLY TAG` | Flow, schema, or catalog | Add, edit, and remove tags on the flow. |
| `MANAGE` | Flow, schema, or catalog | View and manage privileges on the flow, rename it, and drop it. |
| `READ METADATA` | Flow, schema, or catalog | View all owner-visible metadata for the flow, including privilege grants, without the ability to modify it. A child of `MANAGE`. See [READ METADATA](/aws/en/data-governance/unity-catalog/access-control/privileges-reference#read-metadata). |

←✕

| Privilege | Granted on | Allows the user to |
| --- | --- | --- |
| `ALL PRIVILEGES` | Flow, schema, or catalog | Perform all capabilities on the flow: `READ FLOW`, `REFRESH FLOW`, `WRITE FLOW`, and `APPLY TAG`. Does not include `MANAGE` or `READ METADATA`. See [ALL PRIVILEGES](/aws/en/data-governance/unity-catalog/access-control/privileges-reference#all-privileges). |
| `CREATE FLOW` | Catalog or schema | Create a flow in the schema. The user needs `USE CATALOG`, `USE SCHEMA`, and the applicable creation privilege: `CREATE TABLE` when the flow is created implicitly with a new target table, or `CREATE FLOW` when the flow is defined explicitly. Adding a flow to an existing target also requires `MODIFY` on the target table. |
| `READ FLOW` | Flow, schema, or catalog | Describe the flow and read its definition and state. |
| `REFRESH FLOW` | Flow, schema, or catalog | Refresh the flow. |
| `WRITE FLOW` | Flow, schema, or catalog | Reset or rewind the flow's streaming checkpoint. |
| `APPLY TAG` | Flow, schema, or catalog | Add, edit, and remove tags on the flow. |
| `MANAGE` | Flow, schema, or catalog | View and manage privileges on the flow, rename it, and drop it. |
| `READ METADATA` | Flow, schema, or catalog | View all owner-visible metadata for the flow, including privilege grants, without the ability to modify it. A child of `MANAGE`. See [READ METADATA](/aws/en/data-governance/unity-catalog/access-control/privileges-reference#read-metadata). |

See [Unity Catalog privileges reference](/aws/en/data-governance/unity-catalog/access-control/privileges-reference) for all Unity Catalog privileges.

## Grant privileges on a flow

Use `GRANT` with the `FLOW` securable type. To grant privileges on a flow, you must be the flow owner or have `MANAGE` on the flow, in addition to `USE CATALOG` and `USE SCHEMA` on its parents.

To let a group refresh a flow, run the following:

SQL

```
GRANT USE CATALOG ON CATALOG main TO `data-engineers`;

GRANT USE SCHEMA ON SCHEMA main.sales TO `data-engineers`;

GRANT REFRESH FLOW ON FLOW main.sales.orders_flow TO `data-engineers`;
```

## Additional resources

* [Load and process data incrementally with Lakeflow pipeline flows](/aws/en/ldp/concepts/flows)
* [Use flows in Lakeflow pipelines](/aws/en/ldp/flow-examples)
* [Unity Catalog securable objects reference](/aws/en/data-governance/unity-catalog/securable-objects)
* [Unity Catalog permissions model concepts](/aws/en/data-governance/unity-catalog/access-control/permissions-concepts)