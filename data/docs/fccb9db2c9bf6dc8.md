note

This page covers requirements, quotas, and limitations for row filter and column mask policies. For GRANT policies (Beta), see [ABAC GRANT policies for models (Beta)](/aws/en/data-governance/unity-catalog/abac/grant-policies).

This page lists requirements, policy quotas, and current limitations for ABAC row filter and column mask policies in Unity Catalog.

## Compute requirements

To use ABAC policies, you must use one of the following compute configurations:

* [Serverless compute](/aws/en/compute/serverless/)
* [Standard compute](/aws/en/compute/standard-overview) on Databricks Runtime 16.4 or above
* [Dedicated compute](/aws/en/compute/dedicated-overview) on Databricks Runtime 16.4 or above with [fine-grained access control filtering enabled](/aws/en/compute/single-user-fgac)

For guidance on running workloads that require older runtimes, see [Access from older runtimes](#access-from-older-runtimes).

## Governed tags requirement

ABAC policies use governed tags, not ungoverned tags. Governed tags are defined at the account level with access controls that determine who can create, assign, and manage them. For full details, see [Governed tags](/aws/en/admin/governed-tags/).

note

After assigning or modifying a tag, it can take a few minutes for the change to take effect.

## Policy quotas

| Resource | Limit |
| --- | --- |
| Policies per metastore | 10,000 |
| Policies per catalog or schema | 100 |
| Policies per table | 50 |
| Principals per policy (applies to both `TO` and `EXCEPT` clauses) | 20 |
| Column conditions per `MATCH COLUMNS` clause | 3 |

←✕

| Resource | Limit |
| --- | --- |
| Policies per metastore | 10,000 |
| Policies per catalog or schema | 100 |
| Policies per table | 50 |
| Principals per policy (applies to both `TO` and `EXCEPT` clauses) | 20 |
| Column conditions per `MATCH COLUMNS` clause | 3 |

For more details, including governed tags quotas, see [Service limits](/aws/en/resources/limits).

## ABAC limitations

### Access from older runtimes

Standard and dedicated compute on Databricks Runtime versions earlier than 16.4 can't access ABAC-secured tables. If you need certain workloads to continue running on an older runtime, scope the ABAC policy to a specific group instead of applying it broadly. Add only the users or principals you want the policy to apply to that group, and exclude the principal that runs the older-runtime workload using the `EXCEPT` clause. Users outside the group retain full access to the underlying tables. This allows that workload to continue accessing the tables while you transition to a supported runtime.

### ABAC policies on views

You can't apply ABAC policies directly to views. However, when a user queries a view that references tables with ABAC policies, those policies are respected when accessing data through the view.

ABAC row filters and column masks on the underlying tables are evaluated using the **session user's identity**, meaning the person running the query. The user sees only the rows and column values they are authorized to access, as defined by the ABAC policies on the base tables. Base table access checks and access checks to dependencies use the view owner's identity, so users can query views without direct privileges on the underlying tables.

note

The same session user identity model applies when tables with ABAC policies are accessed through functions.

The session user identity model was introduced alongside the ABAC GA release. Previously, policies were evaluated using the view owner's or function definer's identity. For more information, see the [April 2026 release notes](/aws/en/release-notes/product/2026/april#attribute-based-access-control-abac-is-now-generally-available).

### ABAC policies on materialized views and streaming tables

When a pipeline refreshes a materialized view or streaming table, it evaluates policies using the pipeline owner's or run-as identity. If that identity is subject to an ABAC policy, the materialized view or streaming table permanently contains masked or filtered data. To avoid this, add the pipeline owner or run-as identity to the `EXCEPT` clause of ABAC policies associated with all the tables being read during the pipeline refresh. Use the `TO` clause to specify which users and groups receive masked or filtered data.

### OpenSharing tables with ABAC policies or views that reference them

Tables with ABAC policies or views that reference tables with ABAC policies can only be shared through OpenSharing if the share owner is exempt from the policy (listed in the `EXCEPT` clause). The policy doesn't govern the recipient's access. Recipients can apply their own ABAC policies to shared tables to enforce access control on their side.

* For share providers, see [Add tables and schemas secured by ABAC policies to a share](/aws/en/opensharing/create-share#abac).
* For share recipients, see [Read ABAC-secured data and apply ABAC policies](/aws/en/opensharing/read-data-databricks#abac).

For details on how to use OpenSharing with ABAC, see [OpenSharing and ABAC](/aws/en/data-governance/unity-catalog/abac/opensharing).

### Time travel and cloning on tables with ABAC policies

ABAC policies can't be evaluated against historical table snapshots, so time travel queries fail on tables with active row filters or column masks. Deep and shallow clones also aren't supported on tables with ABAC policies.

To enable these operations, create a service principal or group and add it to the policy's `EXCEPT` clause. The policy isn't evaluated for exempted principals, so these operations can run.

important

Exempted principals see unfiltered, unmasked data. Only exempt trusted identities such as service principals used for ETL or pipeline workloads.

For example, the following policy masks PII columns for all users except the `etl_service_principal`, which can run time travel queries and clone operations:

SQL

```
CREATE POLICY mask_pii  
ON CATALOG prod  
COLUMN MASK prod.governance.mask_value  
TO `account users`  
EXCEPT `etl_service_principal`  
FOR TABLES  
MATCH COLUMNS  
  has_tag_value('pii', 'ssn') AS ssn  
ON COLUMN ssn;
```

### AI Search indexes and ABAC policies

ABAC policies on a source table don't apply to AI Search indexes created from that table. The index syncs all rows from the source table and doesn't enforce row filter or column mask policies when serving queries.

For tables with column masks, you can exclude masked columns from the index using the [columns to sync](/aws/en/ai-search/create-ai-search) setting.

### Multiple policies on the same table or column for the same user

Only one distinct row filter can resolve at runtime for a given table and a given user, and only one distinct column mask can resolve for a given column and a given user. You can define multiple policies, but when a user queries the table, only one policy's conditions must match. If multiple distinct row filters or column masks apply to the same user and table or column, Databricks blocks access and returns an error. Multiple policies are allowed if they resolve to the same row filter or column mask UDF with the same arguments.

For details, see [Rules for multiple filters and masks](/aws/en/data-governance/unity-catalog/abac/policy-evaluation#multiple-filters).

### ABAC on dedicated compute

For limitations of ABAC on dedicated compute, see [Limitations](/aws/en/compute/single-user-fgac#limitations).

### Limitations common to ABAC and table-level row filters and column masks

For general limitations of row filters and column masks that apply to both ABAC and [table-level row filters and column masks](/aws/en/data-governance/unity-catalog/filters-and-masks/), see [Limitations](/aws/en/data-governance/unity-catalog/filters-and-masks/#limits).