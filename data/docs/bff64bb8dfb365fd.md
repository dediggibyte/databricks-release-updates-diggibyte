On this page

Last updated on **Jul 1, 2026**

Beta

The AI Runtime CLI is in [Beta](/aws/en/release-notes/release-types).

The `air` command-line interface submits and manages distributed training workloads on [AI Runtime](/aws/en/machine-learning/ai-runtime/), the on-demand serverless GPU compute platform. The CLI uses YAML-based job configuration, integrates with MLflow, and supports workspace-based and git-based code workflows.

## When to use the CLI[​](#when-to-use-the-cli "Direct link to When to use the CLI")

Use the AI Runtime CLI when you want to:

* Submit GPU training workloads from your laptop and code editor without opening a notebook.
* Define training jobs declaratively in YAML so they can be checked into source control.
* Run long-running training jobs or multi-node distributed training — workloads that need to outlive an interactive session or span more than one node.

For the in-notebook Python API (`@distributed` and `@ray_launch`), see [Multi-GPU workload](/aws/en/machine-learning/ai-runtime/distributed-training) instead.

To work interactively on a single GPU node over SSH — from your terminal or IDE, rather than submitting a workload — use `databricks ssh connect`. See [Connect to Databricks using an SSH tunnel](/aws/en/dev-tools/ssh-tunnel).

## In this section[​](#in-this-section "Direct link to In this section")

* [Install the AI Runtime CLI](/aws/en/machine-learning/ai-runtime/cli/installation)
* [AI Runtime CLI quickstart](/aws/en/machine-learning/ai-runtime/cli/quickstart)
* [AI Runtime CLI command reference](/aws/en/machine-learning/ai-runtime/cli/command-reference)
* [Workload YAML reference](/aws/en/machine-learning/ai-runtime/cli/yaml-config)
* [Track runs with MLflow and the Jobs run page](/aws/en/machine-learning/ai-runtime/cli/track-runs)
* [Use custom Docker images](/aws/en/machine-learning/ai-runtime/cli/docker-images)
* [AI Runtime CLI examples](/aws/en/machine-learning/ai-runtime/cli/examples/)