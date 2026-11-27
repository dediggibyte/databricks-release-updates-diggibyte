Workspace-level Genie One is available to the members of a single workspace. Account-level Genie One is available to all users in your Databricks account, across all of its workspaces. Use workspace-level Genie One to give business users a focused experience in a specific workspace. Use account-level Genie One when your users work with assets in more than one workspace, or when some users don't belong to any workspace.

## Workspace-level Genie One

Workspace-level Genie One is scoped to a single workspace and available only to its members. Account-only users don't have access.

Workspace members need at least one workspace entitlement, such as Consumer access, Databricks SQL access, or Workspace access. Any of them lets members use Genie One chat and open the dashboards, Genie Agents, and Databricks Apps that are shared with them. For more about Consumer access, see [What is consumer access?](/aws/en/ai-bi/consumers/).

Workspace admins and users with higher entitlements also qualify. You can assign entitlements by syncing them from your identity provider, by granting them to users and groups in the workspace admin settings, or by using the API. For background, links to the steps for each method, and a comparison of what each entitlement allows, see  [Access entitlements](/aws/en/security/auth/entitlements#access-entitlements).

To open workspace-level Genie One, see [Access workspace-level Genie One](/aws/en/genie-one/access-genie-one#access-workspace-level).

## Account-level Genie One

Account-level Genie One is a unified view across all workspaces in your Databricks account. Users can only access assets explicitly shared with them. To view data from a specific workspace, users need at least one workspace entitlement for that workspace, such as Consumer access, Databricks SQL access, or Workspace access.

Users in a registered identity provider who aren't assigned to a workspace can use a [limited account-only experience](/aws/en/genie-one/account-only-user-access).

To open account-level Genie One, see [Access account-level Genie One](/aws/en/genie-one/access-genie-one#access-account-level).

### Use cross-workspace chat

Workspace members can use account-level Genie One to ask questions about and take action on assets across workspaces. A single response can use assets from multiple eligible workspaces. Users need at least one workspace entitlement for each workspace they query, such as Consumer access, Databricks SQL access, or Workspace access. Genie One uses only assets and data that the user has permission to access.

To choose the compute for account-level chat:

1. In account-level Genie One chat, click the  kebab menu next to the ask bar.
2. Click **Manage compute**.
3. In the **Compute** drop-down, select **Auto** to let Genie One select an available SQL warehouse, or select a SQL warehouse under an eligible workspace. The choice applies to the current session only, and each new visit starts on **Auto**.

The compute selector lists only SQL warehouses that you can access, grouped by workspace. Eligible workspaces must meet all of the following requirements: you belong to the workspace, Genie One is enabled, and the workspace is in the same region and connected to the same Unity Catalog metastore as the [system workspace](#system-workspace). Queries run as you on the selected SQL warehouse, and usage is billed to that warehouse's workspace.

The following limitations apply:

* Cross-metastore and cross-region queries aren't supported.
* Catalogs that are [bound to a workspace](/aws/en/data-governance/unity-catalog/access-control/workspace-catalog-binding) cannot be accessed in cross-workspace chat.
* If the workspace that runs the query turns off results downloads, you can't save or download the results.
* The [Genie One Model Context Protocol (MCP) server](/aws/en/agents/mcp-tools/genie-mcp) does not support cross-workspace chat.
* Workspaces that use the [compliance security profile](#compliance-profile-exclusion) are excluded.

## Control access to account-level Genie One

Account admins can control access to account-level Genie One in the account console. This setting applies to all users in the account and does not apply to workspace-level Genie One.

1. In the [account console](https://accounts.cloud.databricks.com), click  **Settings**.
2. Click the **Feature enablement** tab.
3. Turn **Genie** on or off.

## Account-level Genie One data handling and processing

Account-level Genie One is an account-wide discovery and search surface for dashboards, Genie Agents, Databricks Apps, and other assets that you have permission to access. When you open an asset, it opens in the originating workspace.

### System workspace for account-level Genie One

To support account-level features, Databricks automatically provisions a managed workspace named `databricks-system-workspace` in your account. Account-level Genie One runs on this workspace.

The system workspace appears in the [`system.access.workspaces_latest`](/aws/en/admin/system-tables/workspaces) system table.

Like account-level Genie One, the system workspace does not aggregate or process data from [workspaces that use the compliance security profile](#compliance-profile-exclusion).

To remove the system workspace from your account, contact Databricks support.

### Network connectivity

Account-level Genie One supports front-end Private Link (Beta). Users in your VPCs or on-premises networks can reach account-level Genie One over a private connection instead of the public internet. For setup, see [Configure inbound Private Link for account-level resources](/aws/en/security/network/front-end/front-end-private-connect-account).

### What data is processed and where

When you use account-level Genie One, Databricks-generated metadata (such as asset identifiers, usage signals, and audit events) might be processed in the US. Customer data and metadata (such as tables, dashboards, charts, and similar objects) is stored in the same region as your workspace but processed according to your [Geo settings](/aws/en/resources/databricks-geos#cross-geo-processing):

* If you've disabled cross-Geo processing, processing happens in the same Geo as the workspace.
* If not, processing can happen across multiple Geos.

If your data residency or compliance policies do not permit metadata to be sent to US-based services, turn off account-level Genie One using the control described in [Control access to account-level Genie One](#enable). Turning off the feature stops account-level Genie One from sending additional metadata to US-based services.

### Workspaces using the compliance security profile are excluded

Account-level Genie One does not aggregate data from workspaces with the compliance security profile enabled.