This page describes how to use Databricks Data Classification in Unity Catalog to automatically classify and tag sensitive data in your catalog.

For new classifiers, changes to classification behavior, and other updates, see [Data Classification release notes](/aws/en/release-notes/data-classification/).

Data catalogs can have a vast amount of data, often containing known and unknown sensitive data. It is critical for data teams to understand what kind of sensitive data exists in each table so that they can both govern and democratize access to this data.

To address this problem, Databricks Data Classification uses an agent to automatically classify and tag tables in your catalog. This allows you to discover sensitive data and to apply governance controls over the results, using tools such as [Attribute-based access control in Unity Catalog](/aws/en/data-governance/unity-catalog/abac/). For a list of supported tags, see [Supported classification tags](/aws/en/data-governance/unity-catalog/data-classification-tags).

Using this feature, you can:

* **Classify data**: The engine uses an agentic AI system to automatically classify and tag any tables in Unity Catalog.
* **Optimize cost through intelligent scanning**: The system intelligently determines when to scan your data by leveraging Unity Catalog and the Data Intelligence Engine. This means that scanning is incremental and optimized to ensure all new data is classified without manual configuration.
* **Review and protect sensitive data**: The results display assists you in viewing classification results and protecting sensitive data by tagging and creating access control policies for each class.

Account and metastore admins can monitor classification coverage, such as the percentage of tables with sensitive data detections, on the [Data page](/aws/en/admin/governance-hub/data) in Governance Hub.

important

Databricks Data Classification uses [default storage](/aws/en/storage/default-storage) to store classification results. You are not billed for the storage.

Databricks Data Classification uses a large language model (LLM) to assist with classification.

## Requirements

* Your workspace must have [serverless compute](/aws/en/compute/serverless/) available (enabled by default in workspaces with Unity Catalog).
* To enable data classification, you must own the catalog or have the `MANAGE` privilege on it.
* To enable automatic tagging for a catalog, you must have `USE CATALOG` on the catalog, `APPLY TAG` on the catalog, and `ASSIGN` on the tag being applied.
* To view all classification results for a catalog in the UI, you must have one of the following privileges on the catalog:
  + `MANAGE`
  + `READ METADATA`
  + `USE CATALOG`, `USE SCHEMA`, and `SELECT`
* To view classification results for a single schema, you must have `USE CATALOG` on the catalog and one of the following privileges on the schema:
  + `MANAGE`
  + `READ METADATA`
  + `USE SCHEMA` and `SELECT`
* If you have only `USE CATALOG` or `BROWSE` on a catalog, you can view summary results for the catalog and its schemas. You can see detections only for tables accessible to you.
* To see sample values associated with detections, you must have `SELECT` on the [The results system table](#results-system-table).

Schema-level access lets a central admin team delegate review of classification results to schema owners, without granting them access to results for the whole catalog.

note

By default, only account admins have `MANAGE` and `ASSIGN` permissions on data classification system governed tags. Account admins can grant `MANAGE` and `ASSIGN` for individual governed tags to other users, service principals, or groups. See [Manage permissions on governed tags](/aws/en/admin/governed-tags/manage-permissions).

## Use data classification

You can enable data classification for multiple catalogs at once from the results page, or configure individual catalogs with more granular schema-level control.

### Enable multiple catalogs

1. On the Data Classification results page, click **Configure**.
2. Select the catalogs you want to enable, or select all available catalogs in the workspace.
3. Click **Enable**.

Enabling all available catalogs does not automatically enable future catalogs. To classify a new catalog, return to the **Configure** dialog and enable it.

### Enable a single catalog with schema selection

To control which schemas in a catalog are scanned:

1. Navigate to the catalog and click the **Details** tab.
2. Next to **Data Classification**, click the **Enable** button.
3. The **Data Classification** dialog appears. Use the **Schema scope** drop-down menu to choose which schemas to scan:

   * **All selected and future schemas** (default): Automatically scans existing schemas and any new schemas created in the future. Clear the checkbox next to any existing schema you want to exclude from scanning.
   * **Only selected schemas**: Scans only the schemas you select. New schemas are not scanned until you add them to the list.
4. Click **Save**.

This creates a background job that incrementally scans all tables in the catalog or selected schemas.

The classification engine relies on intelligent scanning to determine when to scan a table. New tables and columns in a catalog are typically scanned within 24 hours of being created.

### Manually trigger a full scan

After the initial scan, you can manually trigger a full scan at any time. A full scan re-evaluates every table in the schemas and catalogs where data classification is enabled. It does not scan schemas you excluded or did not select. The scan applies any newly configured classes to your existing and new data, and incurs compute costs similar to the initial scan.

To trigger a full scan for a catalog:

1. Navigate to the catalog and click the **Details** tab.
2. Next to **Data Classification**, click **View results** to open the Data Classification UI.
3. By default, the catalog is selected as the scope. Click **Trigger full scan**.

## How recreated and temporary tables are scanned

Data Classification is optimized for tables that are frequently dropped and recreated, and for tables that exist briefly.

* **Dropped and recreated tables**: When a table is recreated with the same name and columns, for example by `CREATE OR REPLACE TABLE`, `DROP SCHEMA ... CASCADE`, or a pipeline that fully refreshes its tables, Data Classification keeps the previous table's classification results instead of scanning it again. If [view scanning](#classify-views) is enabled, this also applies to views.
* **Temporary and staging tables**: Data Classification recognizes short-lived staging and temporary tables created by common ingestion, transformation, and BI tools, and avoids scanning them before they are dropped.

## Classify views

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To use it, a workspace admin must turn on **Data Classification View Scanning** from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

By default, Data Classification scans tables, streaming tables, and materialized views. When view scanning is enabled, Data Classification also scans the columns of regular Unity Catalog views and classifies sensitive data in them, using the same detectors and classes it applies to tables.

View classification results appear alongside your table results, both in the Data Classification results page and in the [The results system table](#results-system-table).

### Enable view scanning

After a workspace admin turns on the preview, all catalogs with Data Classification enabled in the workspace include views on their next scheduled scan.

note

Enabling view scanning increases Data Classification cost, because views are scanned in addition to your tables. The size of the increase depends on how many views your catalogs contain and how large and complex they are. Databricks recommends enabling view scanning first in a workspace with smaller catalogs to observe the cost impact before enabling it more broadly. See [View Data Classification expenses](#view-data-classification-expenses).

### View scanning limitations

* **Classification tags are not applied to view columns by default.** Unlike tables, views are classified but their columns are not tagged with `class.*`, because a classification tag on a view can conflict with an existing column-mask or row-filter policy and make the view non-queryable. If [ABAC on Views](/aws/en/data-governance/unity-catalog/abac/policies#create-a-policy) (Beta) is enabled, auto-tagging of view columns is supported. In either case, you get the full classification results in the results page and the [The results system table](#results-system-table).
* **Views with unsafe definitions are not scanned.** Views whose definitions use unsafe operations, such as legacy Hive metastore user-defined functions, `reflect()`, and `java_method()`, are not scanned. They are reported with the status `UNSUPPORTED_VIEW_DEFINITION`.
* **Metric views are not scanned.** [Metric views](/aws/en/uc-semantics/metric-views/) are excluded from view scanning and do not appear in view classification results.

## View classification results

To view classification results, click **View results** next to the **Data Classification** setting.

This opens the Data Classification UI for the catalog. To view classification results, a serverless SQL warehouse is required.

You can also view aggregated results across all classified catalogs in the metastore by using the catalog selector at the upper left. Choose **All catalogs** from the drop-down menu.

Use the **Compliance framework** filter to limit the results to classifications associated with a specific compliance framework.

For each classification type, the table shows:

* **Detected columns**: The number of columns where the classification was detected.
* **Auto-tagging**: The tagging status for that classification — **Active** or **Inactive**. In the metastore view, a status of **Partially Active** indicates that tagging is enabled in some but not all catalogs.
* **Compliance framework**: The compliance frameworks associated with the classification. For details about the classifications included in each framework, see [Compliance framework reference](/aws/en/data-governance/unity-catalog/data-classification-tags#compliance-reference).
* **Unmasked user access (last 7d)**: The percentage of users who accessed unmasked data of that classification over the last 7 days. Use this to assess the exposure of sensitive data across your organization.

### Review detections

To review the results for a specific classification type, click **Review** in the rightmost column. A panel appears with two tabs:

* **Detected Columns**: Displays the columns where the classification tag was detected with high confidence, ordered by most recent detection first. Also includes a **Detections over time** chart and a list of detected columns with sample values. Click any bar in the chart to see the specific detections for that date. Sample values appear only if you have the required permissions to view classification results.
* **User Access**: Lists all users who accessed columns with this classification tag, showing their email and username along with whether they have masked or unmasked access. Also shows any [attribute-based access control (ABAC)](/aws/en/data-governance/unity-catalog/abac/) policies assigned to this classification tag. When viewing results for a single catalog, you can create a new ABAC policy directly from the panel.

If any detected columns are incorrect, you can click the **Exclude** icon to the right of the entry. See [Exclude detections](#exclude-detections).

### Enable automatic tagging

If the identified columns match your expectations, you can enable automatic tagging for the classification tag. When automatic tagging is enabled, all existing and future detections of this classification are tagged.

You can configure automatic tagging at two levels:

* **Metastore level**: Enable or disable across all catalogs at once. You must be a metastore admin and have `ASSIGN` on the tag being applied.
* **Catalog level**: Enable or disable for the current catalog only. Catalog-level settings take precedence over the metastore-level setting. You must have `USE CATALOG` and `APPLY TAG` on the catalog, and `ASSIGN` on the tag being applied.

At the catalog level, automatic tagging has three states:

* **Default (inherited)**: The catalog inherits the tagging setting from the metastore level.
* **Active**: Tagging is explicitly enabled for this catalog, regardless of the metastore-level setting.
* **Inactive**: Tagging is explicitly disabled for this catalog, regardless of the metastore-level setting.

When you disable tagging, no future tags are applied, but existing tags are not removed.

note

When you enable automatic tagging, tags are not backfilled immediately. They will be populated in the next scan, which should take effect within 24 hours. Subsequent classifications will be tagged immediately.

### Exclude detections

Beta

Detection exclusions and their use to improve future classification accuracy are in [Beta](/aws/en/release-notes/release-types).

In the review panel, you can exclude individual column detections. Excluding a detection:

* Removes any existing classification tag from that column.
* Prevents future scans from reapplying the tag to that column.
* Provides feedback that improves the accuracy of future classification results.

To exclude a detection, click the **Exclude** icon for the corresponding column in the review panel. To re-include the detection, click the icon again.

### The results system table

Data classification creates a system table named `system.data_classification.results` to store results that by default are accessible only to the account admin. The account admin can share this table. The table is only