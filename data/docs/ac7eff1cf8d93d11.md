Genie Migrate converts SQL from dialects such as T-SQL, Snowflake, Redshift, Oracle, BigQuery, and Teradata into Databricks SQL queries or Databricks notebooks. It also converts extract, transform, and load (ETL) workloads from Informatica PowerCenter (Beta) into Databricks notebooks. You convert files in a migration project, and you choose the output format, called the target framework, when you create the project. See [Supported source dialects and target frameworks](#supported-sources).

For requirements, see [Requirements for Genie Migrate](/aws/en/migration/genie-migrate/#requirements).

## How Genie Migrate converts code

When you run a conversion, Genie Code deploys subagents that convert files concurrently. Each subagent analyzes the source dialect and generates the equivalent code for the project's target framework (Databricks SQL or a Databricks notebook).

Each subagent then checks the converted code:

* **Syntax**: Checks that the converted code runs on Databricks without errors.
* **Semantic intent**: Checks that the converted code keeps the business logic of the source, such as the same joins and `WHERE` clauses.

When a check fails, the subagent revises the code and checks it again. Genie Code also applies your custom skills when it converts files. See [Improve conversions with custom skills](#custom-skills). Converted files are written directly to the workspace folder that you specify for the project.

You can also convert a single file or folder without a project by using the `/migrate` command in a Genie Code conversation.

## Supported source dialects and target frameworks

Genie Migrate converts the following SQL dialects:

* T-SQL
* Snowflake SQL
* Redshift SQL
* Oracle
* BigQuery
* Teradata

When you create a migration project for a SQL dialect, choose one of the following target frameworks:

* **DBSQL**: ANSI-compliant Databricks SQL queries.
* **Notebooks** (Beta): Databricks notebooks that use the DataFrame API, with `spark.sql` for logic that is clearer in SQL.
* **Spark Declarative Pipelines** (Beta): [Lakeflow pipelines](/aws/en/ldp/), for T-SQL projects only, including scripts from SQL Server and Azure Synapse dedicated SQL pools. When the **Migration Projects Experimental Features** preview is on, this target is selected by default for T-SQL projects.

Genie Migrate also supports Informatica PowerCenter as an ETL source.

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To use it, a workspace admin must turn on **Migration Projects Experimental Features** from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

Informatica Intelligent Data Management Cloud (IDMC) and Informatica Intelligent Cloud Services (IICS) aren't supported. Genie Migrate converts the objects in an Informatica export, such as workflows and mappings, into Databricks notebooks, so Informatica projects always use the Notebooks target framework.

To prepare Informatica workflows for conversion, export them from PowerCenter Repository Manager in the PowerMart XML format. Export at the workflow level and include dependent objects, such as mappings, sessions, mapplets, and worklets. Don't include credentials in the export.

## Convert files in a migration project

Before you convert, create a migration project and add your source files. See [Create and analyze a migration project](/aws/en/migration/genie-migrate/projects).

### Step 1: Run the conversion

In Informatica projects, you select and convert the workflows, mappings, and other objects that analysis creates, not the uploaded `.xml` exports.

To convert specific files, select them and click **Convert selected**. To convert all files in the project, clear the selection and click **Convert all**. To convert one group at a time, hover over the group's row and click **Convert this group**. See [Plan the migration in groups](/aws/en/migration/genie-migrate/projects#groups). Genie Code opens a conversation, invokes the migration skill, and deploys subagents to convert the files concurrently. Each converted file appears as a linked file in the project. Each file shows one of the following statuses:

* **Gray**: The file hasn't been converted yet (**Not started**, **Queued**, or **Stopped**). A spinner shows while the file converts.
* **Unfilled green**: The file converted with no issues (**Converted**).
* **Filled green**: You reviewed and accepted the converted file (**Reviewed**).
* **Yellow**: The file converted, but it has action items that you need to review.
* **Red**: The conversion failed (**Error**).

In projects that target Lakeflow pipelines, each group becomes one pipeline that you own, and a file converts only after it's in a group with a catalog and schema. Before you convert a group, click **Select catalog and schema** on its row to choose where its pipeline publishes tables and views. The destination applies when the group's pipeline is first created. If a group's pipeline is deleted, the next conversion of the group creates a new pipeline, as long as the group still has a catalog and schema. Otherwise, the conversion fails and asks you to set them. Each run converts files from up to 10 groups.

Each run converts up to 500 files. If you queue more than 500 files, the first 500 unconverted files convert in the current run. After the run finishes, start the conversion again to convert the next 500.

### Step 2: Review conversion results

For Databricks SQL projects, click a converted file to open an inline diff in the SQL editor, which shows each section of source code above the proposed Databricks SQL that replaces it. Accept all suggested changes, or review and accept individual edits. For Notebooks projects, click a converted file to open the generated Databricks notebook. For scripts that fail to convert, edit the code in the editor or ask Genie Code to re-validate or retry specific sections. After you are satisfied, run the converted SQL or notebook to confirm that it runs on Databricks. If the same error appears in several files, capture the fix in a custom skill and rerun those files. See [Improve conversions with custom skills](#custom-skills).

For projects that target Lakeflow pipelines, click **Open pipeline** on a converted group, review the `-- TODO: manual review required` comments in its SQL files, and then run the pipeline. Genie Migrate validates each converted group with a dry run of its pipeline, so nothing runs and no data is written until you run the pipeline.

Each group's pipeline is named after the project and group, for example `Retail warehouse migration / Sales (Lakebridge 2761…/a0b2…)`. Its converted files are in a folder named after the group inside the project's destination folder, under `transformations/`. Renaming the group later doesn't move the folder.

For Informatica projects, compare each generated notebook with the corresponding PowerCenter mapping. Check source and target tables, joins, filters and router groups, lookups, Update Strategy logic, and parameters. Before you use a converted pipeline in production, run it on non-production data and compare results such as row counts and key aggregates with the output of the PowerCenter workflow.

## Improve conversions with custom skills

Custom skills let you encode business rules that Genie Code applies automatically during every conversion. Use them to handle proprietary data types, enforce preferred target patterns, or capture corrections that you make repeatedly. A migration skill is a Genie Code skill, so you can create and manage it the same way as any other skill. See [Extend Genie Code with agent skills](/aws/en/genie-code/skills).

You don't need to define all your skills before your first conversion. Most of the rules a skill should capture only become clear after you review the first results. A typical workflow is:

1. Convert a representative set of files.
2. Review the files with action items or errors, and look for errors that repeat across files, such as the same unsupported data type, function, or naming pattern.
3. Create a skill that captures the fix for each recurring error.
4. Select only the affected files and click **Convert selected**. Genie Code applies the new skill to those files.

Repeat this cycle as you convert more of your code. Genie Code applies each skill to later conversions in the workspace, so one fix covers other files with the same pattern.

You can create a skill from the Genie Code settings or from a Genie Code conversation. Use the settings path for complex skills that include detailed instructions, examples, or supporting files. Use the chat path for quick, single-rule skills.

* Genie Code settings
* Genie Code chat

Create the skill as a file so you can author detailed instructions and version it in a Git folder:

1. In the Genie Code panel, click  **Settings**, then click  **Open skills folder**.
2. Create a folder for your skill under the workspace skills path, `Workspace/.assistant/skills/`. For example, `Workspace/.assistant/skills/sql-migration/`.
3. In the skill folder, create a `SKILL.md` file with the required frontmatter and your conversion rules. For example:

   ```
   ---

   name: sql-migration

   description: Conversion rules to apply when migrating legacy SQL to ANSI SQL.

   ---

   Always convert the custom type MYDATE to TIMESTAMP_NTZ.
   ```

Genie Code picks up the skill the next time you run a conversion.

Describe the conversion rule that you want to encode, then ask Genie Code to save it:

prompt

```
Always convert our custom type MYDATE to TIMESTAMP_NTZ. Save this as a custom migration skill.
```

Genie Code creates and registers the skill and applies it on future conversions in the workspace.

To view active skills:

prompt

```
Show me my migration skills
```

To remove a skill:

prompt

```
Delete the migration skill for [description]
```

Workspace skills are stored at the workspace level and shared across all users in the workspace.

## Test and validate converted code

The following tips help you review and gain confidence in the converted output:

* **Batch conversion**: Convert a small set of two to five files in one session to verify that multi-file conversion works end to end.
* **Syntax validation**: After conversion, run the output in a Databricks SQL editor or notebook to confirm that it runs without errors.
* **Edge cases**: Include a script with dialect-specific constructs, such as T-SQL window functions, Snowflake `QUALIFY`, or Redshift `LISTAGG`, to see how the converter handles non-trivial patterns.
* **Semantic correctness**: Run the original and converted queries against equivalent test data and compare the results. Confirm that the output is semantically correct, not only syntactically valid.

## Additional resources

* [Genie Code](/aws/en/genie-code/)