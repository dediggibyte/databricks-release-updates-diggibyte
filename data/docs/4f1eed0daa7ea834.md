The Databricks web terminal provides a convenient and highly interactive way to run shell commands in a command-line interface (CLI), including [Databricks CLI commands](/aws/en/dev-tools/cli/), to take actions on Databricks objects programmatically. It's especially useful for advanced use cases, such as batch operations on multiple files, which existing user interfaces (UIs) might not fully support.

Unlike using [SSH](/aws/en/archive/compute/configure#ssh-access), many users can use the web terminal on one compute and it does not require setting up keys.

The web terminal is available on classic compute, serverless CPU compute, and serverless GPU compute (AI Runtime). Support for serverless GPU compute (AI Runtime) is in [Public Preview](/aws/en/release-notes/release-types).

You can use the web terminal to do the following:

* Make quick file edits using Vim or Emacs.
* Monitor resource usage with commands like `htop` (cluster usage) or `nvidia-smi` (GPU usage).
* Run non-Spark Python scripts.
* Execute file operations with shell commands such as `mv` and `mkdir`.
* Install and manage libraries on compute.
* Use the Databricks CLI to automate various aspects of Databricks.

## Requirements

warning

Databricks proxies the web terminal service from port 7681 on the compute's Spark driver. This web proxy is intended for use only with the web terminal. If the port is occupied when the compute starts or there is some sort of conflict, the web terminal might not work as expected. If other web services are launched on port 7681, compute users might be exposed to potential security exploits. Databricks is not responsible for any issues that result from the installation of unsupported software on a compute.

* Web terminal is disabled by default for all workspace users. To enable it, see [Enable the web terminal](/aws/en/admin/clusters/web-terminal).
* [CAN ATTACH TO](/aws/en/compute/clusters-manage#cluster-level-permissions) permission on a compute.
* To use the web terminal with standard access mode (formerly shared access mode), the compute must be on Databricks Runtime 15.1 or above.

* The web terminal on serverless GPU compute (AI Runtime) requires environment version 5 or above.

## Launch the web terminal

You can launch the web terminal from the compute details page or from a notebook.

### From a notebook

To launch the web terminal from a notebook:

1. Connect the notebook to compute.
2. At the bottom of the notebook's right sidebar, click the terminal icon  to launch the web terminal.
3. Alternatively, click the attached compute drop-down, hover over the attached compute, then click **Web Terminal**.

The web terminal opens in a panel at the bottom of the screen. The buttons at the upper-right of the panel allow you to:

* Open a new terminal session in a new tab.
* Reload a terminal session.
* Close the bottom panel. To reopen the panel, click  at the bottom of the right sidebar.

### From the compute details page

To launch the web terminal from the compute details page:

1. On the workspace's sidebar, click **Compute**.
2. On the **All-purpose compute** tab, click the name of the compute.
3. Click **Start** to start the compute.
4. On the **Apps** tab, click **Web Terminal**.

A new tab opens with the web terminal UI and the Bash prompt.

## Use web terminal

In the web terminal, you can run commands from root inside the container of the compute driver node.

Each user can have up to 100 active web terminal sessions (tabs) open. Idle web terminal sessions may time out and the web terminal web application will reconnect, resulting in a new shell process. If you want to keep your Bash session, Databricks recommends using [tmux](https://www.man7.org/linux/man-pages/man1/tmux.1.html).

### Run Databricks CLI commands

You can also use the web terminal to run Databricks CLI commands. The available CLI is always the latest version, and authentication is based on the current user.

note

Configuration profile commands are not supported when running CLI commands in the web terminal. This is because the web terminal uses environment variables to authenticate to the CLI, which precedes configuration profiles in the [authentication order of evaluation](/aws/en/dev-tools/cli/authentication#auth-eval).

The compute must meet the following requirements:

* Databricks Runtime 15.0 or above

* The workspace must not be enabled for PrivateLink

Launch the web terminal and run the following command to output information about the current user:

Bash

```
   databricks current-user me
```

Bundle commands are also available, which allows you to create and manage your [Declarative Automation Bundles](/aws/en/dev-tools/bundles/) directly from the web terminal within the Databricks workspace. For example, to create, deploy, and run a simple bundle using the default template:

1. From the web terminal root, navigate to your workspace home and run `bundle init`:

   Bash

   ```
   cd /Workspace/Users/someone@example.com  
   databricks bundle init
   ```
2. Accept the default template prompts, then change to the bundle directory and deploy it:

   Bash

   ```
   cd my_project  
   databricks bundle deploy
   ```

   You can view the deployed `my_project` bundle in the Databricks workspace UI.
3. Finally, run the default job in the bundle:

   Bash

   ```
   databricks bundle run my_project_job
   ```

   Navigate to **Job Runs** to see the running job.

## Configure your web terminal

You can set persistent configurations for your web terminal using .bashrc configuration files.

Databricks automatically sources files named .bashrc from your workspace file system's home folder. Settings from these files are automatically activated each time you start a new terminal session.

If you want to source any other files (such as .zshrc) for your web terminal experience, source them from your .bashrc file to persist the configuration.

Save all configuration files in your workspace folder where you can configure them using a text editor.

## Limitations

* Databricks does not support running Spark jobs from the web terminal.
* Databricks web terminal is not available in the following compute types:
  + Jobs compute
  + Compute launched with the `DISABLE_WEB_TERMINAL=true` environment variable set.
  + [Standard compute](/aws/en/compute/standard-overview) on Databricks Runtime version below 15.1.
  + [Standard compute](/aws/en/compute/standard-overview) with ARM instance types on Databricks Runtime below 16.4.
  + Serverless compute using serverless environment version 1.
  + Compute launched with the Spark configuration `spark.databricks.pyspark.enableProcessIsolation` set to `true`.

* On serverless GPU compute (AI Runtime), the web terminal is available only in the regions where serverless GPU compute is supported: `us-west-2`, `us-east-1`, and `us-east-2`.

* There is a hard limit of 12 hours since the initial page load, after which any connection, even if active, will be terminated. You can refresh the web terminal to reconnect. Databricks recommends using [tmux](https://www.man7.org/linux/man-pages/man1/tmux.1.html) to preserve your shell session.
* ARM compute resources on Databricks Runtime below 16.4 cannot use web terminals to access workspace files, including files in Git folders.
* Enabling [Docker Container Services](/aws/en/compute/custom-containers) disables web terminal.