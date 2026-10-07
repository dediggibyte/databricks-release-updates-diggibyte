Beta

This feature is in [Beta](/aws/en/release-notes/release-types). It is an early release, and its capabilities, commands, and interfaces change frequently.

Genie Code CLI is a coding agent that runs locally in your terminal and is tuned for data and AI work on Databricks. It works like other terminal coding agents, but comes preconfigured to understand Databricks and to work naturally with your data, pipelines, models, and apps.

Because it runs on your machine, Genie Code CLI can read and edit your local files, run commands, and reach into Databricks on your behalf. It uses the [Databricks CLI](/aws/en/dev-tools/cli/), including the [`databricks genie` commands](/aws/en/dev-tools/cli/reference/genie-commands) such as `databricks genie ask`, to discover data and answer questions about it. During Beta, model access is provided and governed through [Unity Gateway](/aws/en/ai-gateway/), so you do not bring your own model subscription.

## Requirements

* A Databricks workspace in a [Unity Gateway supported region](/aws/en/resources/feature-region-support#model-serving-features-availability).
* Unity Catalog enabled for your workspace. See [Enable a workspace for Unity Catalog](/aws/en/data-governance/unity-catalog/enable-workspaces).
* The [Databricks CLI](/aws/en/dev-tools/cli/) version 1.0.0 or above, installed separately. Genie Code CLI uses it to authenticate and to run the `databricks genie` commands. See [Install or update the Databricks CLI](/aws/en/dev-tools/cli/install).

Genie Code CLI runs under your own identity, so it can only access data and perform operations that your Databricks permissions allow.

## Install and set up

1. Install the [Databricks CLI](/aws/en/dev-tools/cli/) (version 1.0.0 or above) separately, if you have not already. See [Install or update the Databricks CLI](/aws/en/dev-tools/cli/install).
2. Install Genie Code CLI with the command for your operating system.

   * Linux or macOS
   * Windows

   Bash

   ```
   curl -fsSL https://github.com/databricks/genie-code-cli/releases/latest/download/install.sh | bash
   ```

   Run the following in PowerShell:

   PowerShell

   ```
   powershell -ExecutionPolicy Bypass -c "irm https://github.com/databricks/genie-code-cli/releases/latest/download/install.ps1 | iex"
   ```
3. Confirm the installation:

   Bash

   ```
   genie --version
   ```
4. Change into your project directory and start Genie Code CLI:

   Bash

   ```
   cd my-project  
   genie
   ```
5. When prompted, select a Databricks CLI profile, or authenticate if you have not configured one. See [Authentication for the Databricks CLI](/aws/en/dev-tools/cli/authentication).
6. Confirm that you trust the contents of the directory, then start prompting.

## What you can do with it

Genie Code CLI can work directly with local files, discover and query your Unity Catalog data through Genie, and build and deploy Databricks assets from a single conversation in the terminal. For example:

* **Ingest and govern**: "Clean up these monthly sales CSVs, load them into Unity Catalog, and show me revenue by region over time."
* **Explore your data**: "Which of my catalogs has customer churn data, and what were the top drivers last quarter?"
* **Extend a pipeline**: "Add a silver `refunds` table to my orders pipeline and backfill the last 90 days."
* **Train and serve a model**: "Run this training script on Databricks and put the model behind a serving endpoint."
* **Build and ship an app**: "Build a local app prototype for my `customers` table and deploy it as a Databricks App."

## How Genie Code CLI differs from Genie Code in the workspace

Genie Code CLI is a separate experience built for local, terminal-based work. It has its own tools, skills, and instructions, and at this time does not share them with Genie Code in the Databricks workspace. It also does not yet include all of the capabilities available in the workspace UI.

Use Genie Code CLI as a terminal-native companion when you are working locally with files, scripts, and prototypes. Continue to use [Genie Code](/aws/en/genie-code/) in the workspace for the richer, fully featured experience.

## Billing

Genie Code CLI usage is billed the same as using the model directly through [Unity Gateway](/aws/en/ai-gateway/), and appears in your Unity Gateway usage. It is not billed under Genie pricing.

To control spend, workspace admins can set budgets for Unity Gateway. See [Manage budgets for Unity Gateway](/aws/en/ai-gateway/budgets).

## Limitations

* Model selection is managed by Databricks. You cannot choose a specific model. During Beta, Genie Code CLI uses GPT 5.6. The selection may differ from other Genie surfaces, and it can change over time.
* Currently, Genie Code CLI is not billed under Genie usage, and is not impacted by Genie budgets. To control spend, set budgets for Unity Gateway. See [Manage budgets for Unity Gateway](/aws/en/ai-gateway/budgets).