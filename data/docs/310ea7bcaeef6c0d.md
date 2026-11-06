Beta

This feature is in [Beta](/aws/en/release-notes/release-types).

Cost and pricing for features in Beta are subject to change.

The Databricks SSH ([Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell)) tunnel connects Visual Studio Code, Cursor, or your terminal to the Databricks workspace and Databricks serverless compute, AI Runtime, or classic compute. Use it to edit workspace files and run or debug Python scripts and notebooks, with your Python environment and code execution on the remote compute. Connect directly to serverless compute, or set up a reusable SSH connection to a dedicated classic cluster.

note

The SSH tunnel is for IDE-driven and interactive development, including [running Claude Code and Codex](#coding-agents). To run agent loops or untrusted code in a lightweight, isolated environment, see [Databricks Sandbox](/aws/en/compute/serverless/sandbox). For a comparison of the two, see [IDE connected with SSH](/aws/en/dev-tools/ide-tools#tunnel-vs-sandbox).

## Requirements

Start the SSH connection from your local machine. The tunnel cannot be launched from another remote environment or a Docker container.

To connect to serverless or classic compute, you must have:

* Databricks CLI version 1.5.0 or above installed on your local machine and authentication configured. Check your installed version with `databricks --version`. See [Install or update the Databricks CLI](/aws/en/dev-tools/cli/install).
* Either of the following:
  + Visual Studio Code version 1.110.0 (Universal) or above and the [Remote - SSH extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) (1.0.46+) installed.
  + Cursor version 2.6.11 (Universal) or above.

To connect to serverless compute, port forwarding to serverless compute must be enabled. See [Manage port forwarding to serverless compute](/aws/en/admin/workspace-settings/port-forwarding-serverless).

To connect to serverless GPU compute, the AI Runtime feature must be enabled. See [AI Runtime](/aws/en/machine-learning/ai-runtime/).

### Additional requirements for classic compute

To connect to classic (dedicated, single-user) compute:

* The compute must be running Databricks Runtime 17.0 or above. See [Dedicated compute overview](/aws/en/compute/dedicated-overview).
* Unity Catalog must be enabled.
* If a compute policy exists, it must not prohibit jobs execution.
* When using [Databricks Container Services for dedicated compute](/aws/en/compute/custom-containers), your Docker image must have `openssh-server` installed.

## Choose an SSH connection

Use the connection method for your compute type:

| Compute | Connection method | Setup requirement |
| --- | --- | --- |
| Serverless compute | `databricks ssh connect` | No separate SSH setup step.  Add `--ide vscode` or `--ide cursor` to launch an IDE. |
| AI Runtime | `databricks ssh connect --accelerator <accelerator>` | No separate SSH setup step.  Add `--ide vscode` or `--ide cursor` to launch an IDE.  For supported accelerators, see [`--accelerator`](/aws/en/dev-tools/cli/reference/ssh-commands#connect). |
| Classic dedicated, single-user compute | Run `databricks ssh setup --name <connection-name>` in your terminal.  Then start the SSH session from the IDE or run `ssh <connection-name>`. | Select a dedicated, single-user cluster that meets the classic compute requirements.  Shared clusters are not supported. |

←✕

| Compute | Connection method | Setup requirement |
| --- | --- | --- |
| Serverless compute | `databricks ssh connect` | No separate SSH setup step.  Add `--ide vscode` or `--ide cursor` to launch an IDE. |
| AI Runtime | `databricks ssh connect --accelerator <accelerator>` | No separate SSH setup step.  Add `--ide vscode` or `--ide cursor` to launch an IDE.  For supported accelerators, see [`--accelerator`](/aws/en/dev-tools/cli/reference/ssh-commands#connect). |
| Classic dedicated, single-user compute | Run `databricks ssh setup --name <connection-name>` in your terminal.  Then start the SSH session from the IDE or run `ssh <connection-name>`. | Select a dedicated, single-user cluster that meets the classic compute requirements.  Shared clusters are not supported. |

For a comparison with Databricks Connect and other development options, see [Connect from your IDE](/aws/en/dev-tools/ide-tools).

## Connect to serverless compute

Upon meeting the requirements above, run [databricks ssh connect](/aws/en/dev-tools/cli/reference/ssh-commands#connect) from your terminal or IDE.

The `--ide` value selects the editor to launch, regardless of which editor or terminal you run the command from.

* Visual Studio Code
* Cursor
* Terminal

Bash

```
databricks ssh connect --ide vscode
```

The CLI opens a Visual Studio Code window connected to the remote compute.

Bash

```
databricks ssh connect --ide cursor
```

The CLI opens a Cursor window connected to the remote compute.

Bash

```
databricks ssh connect
```

The CLI starts an interactive SSH session.

For command options, including named connections and authentication profiles, see [databricks ssh connect](/aws/en/dev-tools/cli/reference/ssh-commands#connect).

After connecting, [open your workspace project](#open) and [select the Python environment](#run-code). If the connection fails, see [Troubleshoot SSH tunnel connections](#troubleshooting).

### Connect to serverless GPU compute with AI Runtime

With AI Runtime enabled, add `--accelerator` to use GPU compute:

Bash

```
databricks ssh connect --accelerator GPU_1xA10
```

`databricks ssh connect` gives you an interactive session on a single node. For long-running training jobs or multi-node distributed training, submit the workload with `databricks air` instead. See [Use the Databricks CLI with AI Runtime](/aws/en/machine-learning/ai-runtime/connecting/cli/).

## Connect to classic compute

For a reusable connection to a classic dedicated cluster, set up an SSH host name, then select that host in your IDE or connect from a terminal.

### Set up the SSH connection

note

Setting up the SSH connection is only required if you are connecting to classic compute.

Run [databricks ssh setup](/aws/en/dev-tools/cli/reference/ssh-commands#setup) on your local machine. Replace `<connection-name>` with a name for this connection, such as `my-connection`:

Bash

```
databricks ssh setup --name <connection-name>
```

The CLI prompts you to select a cluster and adds a host entry to your SSH configuration. You can also select a cluster directly. Replace `<cluster-id>` with the ID of your dedicated cluster:

Bash

```
databricks ssh setup --name <connection-name> --cluster <cluster-id>
```

To configure how long the SSH tunnel waits after the last client disconnects, add `--shutdown-delay` to the setup command. The default is 10 minutes. For example, to set a 30-minute delay for connections through this SSH host entry:

Bash

```
databricks ssh setup --name <connection-name> --cluster <cluster-id> --shutdown-delay 30m
```

note

For IntelliJ users, Databricks recommends adding `--auto-start-cluster=false` to the setup command and starting the cluster manually before connecting. This is because JetBrains IDEs start all configured clusters on launch, which can result in unexpected compute charges.

### Connect using Visual Studio Code or Cursor

1. For Visual Studio Code, install the [Remote SSH extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh). Cursor includes a remote SSH extension by default.
2. In the IDE main menu, click **View** > **Command Palette**. Select **Remote-SSH: Settings**. Alternatively, select **Preferences: Open User Settings (JSON)** to modify `settings.json` directly.
3. Under **Remote.SSH: Default Extensions** (or `remote.SSH.defaultExtensions` in `settings.json`), add `ms-Python.Python` and `ms-toolsai.jupyter`.

   If you are modifying `settings.json`:

   JSON

   ```
   "remote.SSH.defaultExtensions": [

   "ms-Python.Python",

   "ms-toolsai.jupyter"

   ]
   ```

   note

   Optionally, increase the value of **Remote.SSH: Connect Timeout** (or `remote.SSH.connectTimeout` in `settings.json`) to further reduce the chance of timeout errors. The default timeout is 360.
4. In the Command Palette, select **Remote-SSH: Connect to Host**.
5. From the drop-down menu, select the connection you set up in the first step. The IDE proceeds to connect in a new window.

### Connect using IntelliJ IDEs

1. Follow the [Remote server tutorial](https://www.jetbrains.com/help/idea/remote-development-starting-page.html) to get set up.
2. On the new connection screen, enter:
   * **Username**: `root`
   * **Host**: `<connection-name>`

### Connect to classic compute from a terminal

Use the connection name you configured with `databricks ssh setup`:

Bash

```
ssh <connection-name>
```

For a direct connection without a reusable SSH host entry, you can also use the CLI. Replace `<cluster-id>` with your dedicated cluster ID:

Bash

```
databricks ssh connect --cluster <cluster-id>
```

See [databricks ssh connect](/aws/en/dev-tools/cli/reference/ssh-commands#connect).

## Open workspace projects through SSH

By default, the `databricks ssh connect` command opens to an ephemeral directory. To access workspace files, navigate to your workspace directory from the IDE or terminal:

* In Visual Studio Code or Cursor, from the Command Palette (**Cmd/Ctrl+Shift+P**) select **Open Folder** and navigate to `/Workspace/Users/<your-username>`.
* From a terminal window, change your directory: `cd /Workspace/Users/<your-username>`.

note

Files in `/Workspace`, `/Volumes`, and `/dbfs` persist across cluster restarts. Files in `/home`, `/root`, and other local paths are ephemeral and lost on restart.

## Run Python and notebooks in the SSH session

Select the Python environment provided by your SSH session before running code. For classic compute, this environment includes the built-in Databricks Runtime libraries and [compute-scoped libraries](/aws/en/libraries/cluster-libraries).

1. Open the Command Palette (**Cmd/Ctrl+Shift+P**) and select **Python: Select Interpreter**.
2. Select the `pythonEnv-xxx` virtual environment from the list. If you set up Python dependencies using the `--base-environment` flag, select the longer virtual environment name from the list of options. If the virtual environment does not appear:

   1. Run `echo $DATABRICKS_VIRTUAL_ENV` from a terminal within the IDE.

      Example output: `/local_disk0/.ephemeral_nfs/envs/pythonEnv-xxx/bin/python`
   2. Paste the full output as the interpreter path in the **Python: Select Interpreter** prompt.
3. Open a new terminal and the virtual environment should automatically activate.
4. To run a Jupyter notebook, make sure that the virtual environment is selected as the kernel. Click **Select Kernel** in the upper right of the notebook.

Run and debug Python files and `.ipynb` notebooks using the standard Python and Jupyter extensions.

To use Spark in a Python file on serverless compute, initialize a session explicitly:

Python

```
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().profile("DEFAULT").getOrCreate()
```

## Manage dependencies for SSH sessions

Choose dependency management for your compute type:

* For serverless compute, use a [workspace base environment](#workspace-base-environments) with a supported serverless environment version.
* For classic compute, use [cluster libraries](#cluster-libraries) for dependencies that persist across restarts.
* For dependencies scoped to a project session, use a [setup notebook](#setup-notebook).

For non-Python packages, see [Non-Python dependencies](#init-scripts).

### Workspace base environments (recommended for serverless and AI Runtime)

note

This feature requires the **Serverless workspace base environment support in Jobs** preview to be enabled. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

Use a [workspace base environment](/aws/en/admin/workspace-settings/base-environment) with serverless environment version 4 or below to pre-configure Python dependencies. The SSH tunnel does not support `--base-environment` with serverless environment version 5 or above. Create a base environment using the [workspace UI](/aws/en/admin/workspace-settings/base-environment#create-base-env) or the Databricks CLI [databricks environments create-workspace-base-environment](/aws/en/dev-tools/cli/reference/environments-commands) command.

Specify the environment using the `--base-environment` option when connecting:

Bash

```
databricks ssh connect --base-environment my-workspace-env
```

The `--base-environment` option accepts a display name, a workspace YAML path, or a resource ID. You cannot combine it with `--cluster`. See [databricks ssh connect](/aws/en/dev-tools/cli/reference/ssh-commands#connect).

### Cluster libraries (recommended for classic compute)

Install dependencies using the workspace UI under **Compute > Libraries**. These persist across cluster restarts and are available in `pythonEnv-xxx`. See [Cluster libraries](/aws/en/libraries/cluster-libraries).

### Non-Python dependencies

To persist non-Python dependencies, use an init script that installs the packages when the compute starts. Optionally, store the packages in a Unity Catalog volume and reference them from the init script. See [What are init scripts?](/aws/en/init-scripts/).

### Project-specific notebook setup

For project-scoped dependencies, run a notebook containing `%pip install` commands at the start of each session:

Python

```
# Install from pyproject.toml

%pip install .

# Install from a requirements file

%pip install -r requirements.txt

# Install a wheel from Volumes or Workspace

%pip install /Volumes/catalog/schema/volume/your_library.whl
```

`%pip` commands include Databricks-specific guardrails and propagate dependencies to Spark executor nodes. This enables user-defined 