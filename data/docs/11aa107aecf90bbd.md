On this page

Last updated on **Jul 8, 2026**

Workspace files are the files stored and managed in the Databricks workspace file system. Workspace files can be almost any type of file. Common examples include the following:

* Notebooks (`.ipynb`)
* Source notebooks (`.py`, `.sql`, `.r`, and `.scala`)
* SQL queries (`.dbquery.ipynb`)
* Dashboards (`.lvdash.json`)
* Alerts (`.dbalert.json`)
* Python files (`.py`) files used in custom modules
* YAML configuration (`.yaml` or `.yml`)
* Markdown (`.md`) files, such as `README.md`
* Text files (`.txt`) or other small data files (`.csv`)
* Libraries (`.whl`, `.jar`)
* Log files (`.log`)

note

Genie Agents and experiments cannot be workspace files.

For recommendations on working with files, see [Recommendations for files in volumes and workspace files](/aws/en/files/files-recommendations).

Your Databricks workspace file tree can contain folders attached to a Git repository called "Databricks Git folders". Git folders have some additional file type limitations. For a list of file types supported in Git folders (formerly "Repos"), see [Supported asset types in Git folders](/aws/en/repos/supported-artifact-types).

important

Workspace files are enabled everywhere by default in Databricks Runtime version 11.2. For production workloads, use Databricks Runtime 11.3 LTS or above. Contact your workspace administrator if you cannot access this functionality.

## What can you do with workspace files?[​](#what-can-you-do-with-workspace-files "Direct link to What can you do with workspace files?")

Databricks provides functionality similar to local development for many workspace file types, including a built-in file editor. Not all use cases for all file types are supported.

You can create, edit, and manage access to workspace files using familiar patterns from notebook interactions. You can use relative paths for library imports from workspace files, similar to local development. For more details, see:

* [Workspace files basic usage](/aws/en/files/workspace-basics)
* [Programmatically interact with workspace files](/aws/en/files/workspace-interact)
* [Work with Python and R modules](/aws/en/files/workspace-modules)
* [Display images](/aws/en/notebooks/notebook-media#display-images)
* [Manage Databricks notebooks](/aws/en/notebooks/notebooks-manage)
* [File ACLs](/aws/en/security/auth/access-control/#files)
* [Python unit testing in the workspace](/aws/en/files/python-unit-tests)

Init scripts stored in workspace files have special behavior. You can use workspace files to store and reference init scripts in any Databricks Runtime versions. See [Store init scripts in workspace files](/aws/en/files/workspace-init-scripts).

note

In Databricks Runtime 14.0 and above, the the default current working directory (CWD) for code executed locally is the directory containing the notebook or script being run. This is a change in behavior from Databricks Runtime 13.3 LTS and below. See [What is the default current working directory?](/aws/en/files/cwd-dbr-14).

## Limitations[​](#limitations "Direct link to limitations")

* If your workflow uses source code located in a [remote Git repository](/aws/en/jobs/git), you cannot write to the current directory or write using a relative path. Write data to other location options.
* You cannot use `git` commands when you save to workspace files. The creation of `.git` directories is not allowed in workspace files.
* Reading from workspace files using Spark executors (such as `spark.read.format("csv").load("file:/Workspace/Users/<user-folder>/data.csv")`) is not supported on [serverless compute](/aws/en/compute/serverless/).
* Executors cannot write to workspace files.
* Symlinks are only supported for target directories under the `/Workspace` root folder, such as `os.symlink("/Workspace/Users/someone@example.com/Testing", "Testing")`.
* Workspace files can't be accessed from [user-defined functions (UDFs)](/aws/en/udf/) on clusters with [standard access mode](/aws/en/compute/configure#access-modes) on Databricks Runtime 14.2 and below.
* Notebooks are only supported as workspace files on Databricks Runtime 16.2 and above, and on [serverless environment 2](/aws/en/release-notes/serverless/environment-version/two) and above.
* A notebook cannot be imported as a Python module on Databricks Runtime 16.0 and above. Instead, [change the notebook format](/aws/en/workspace/workspace-assets#ws-asset-names), or if you want the code to be imported, refactor the notebook into a Python file.
* Queries, alerts, and dashboards are only supported as workspace files on Databricks Runtime 16.4 and above, and on [serverless environment 2](/aws/en/release-notes/serverless/environment-version/two) and above. In addition, these workspace files can't be renamed.
* Only notebooks and files support viewing and editing using file system commands, such as `%sh ls`.
* Using `dbutils.fs` commands to access workspace files is not supported on serverless compute. Use a `%sh` cell in notebooks or language-specific commands such as `shutil` in Python when running notebooks on serverless compute.

### File size limit[​](#file-size-limit "Direct link to file-size-limit")

* Workspace file size is limited to 500MB. Operations that attempt to download or create files larger than this limit will fail.

### File access permission limit[​](#file-access-permission-limit "Direct link to File access permission limit")

Permission to access files in folders under `/Workspace` expire after 36 hours for interactive compute and after 30 days for jobs. Databricks recommends running long executions as jobs if they need /Workspace file access.

## Enable workspace files[​](#enable-workspace-files "Direct link to enable-workspace-files")

To enable support for non-notebook files in your Databricks workspace, call the [/api/2.0/workspace-conf](https://docs.databricks.com/api/workspace/workspaceconf/setstatus) REST API from a notebook or other environment with access to your Databricks workspace. Workspace files are **enabled** by default.

To enable or re-enable support for non-notebook files in your Databricks workspace, call the `/api/2.0/workspace-conf` and get the value of the `enableWorkspaceFileSystem` key. If it is set to `true`, non-notebook files are already enabled for your workspace.

The following example demonstrates how you can call this API from a notebook to check if workspace files are disabled and if so, re-enable them.

#### Example: Notebook for re-enabling Databricks workspace file support

[Open notebook in new tab](https://docs.databricks.com/aws/en/notebooks/source/files/turn-on-files.html)[Open in Databricks](https://login.databricks.com/signin?destination_url=%2Fopen%3Fp%3DeyJhY3Rpb24iOiJpbXBvcnRub3RlYm9vayIsInBheWxvYWQiOnsidXJsIjoiaHR0cHM6Ly9kb2NzLmRhdGFicmlja3MuY29tL2F3cy9lbi9ub3RlYm9va3Mvc291cmNlL2ZpbGVzL3R1cm4tb24tZmlsZXMuaHRtbCJ9fQ%253D%253D&utm_source=open-in-databricks&utm_medium=docs&utm_campaign=docs%2Ffiles%2Fworkspace&utm_content=https%3A%2F%2Fdocs.databricks.com%2Faws%2Fen%2Fnotebooks%2Fsource%2Ffiles%2Fturn-on-files.html)

Expand notebook