Beta

Lakewatch is in [Beta](/aws/en/release-notes/release-types). Workspace admins can control access to this feature from the **Previews** page. See  [Manage workspace-level previews](/aws/en/admin/workspace-settings/manage-previews#workspace).

The first time you open Lakewatch, a guided **Welcome to Lakewatch** flow sets it up in Unity Catalog. It creates a Lakewatch [environment](/aws/en/lakewatch/admin/access-control/access-control-model#environments-and-folders), backed by a catalog, and two [folders](/aws/en/lakewatch/admin/access-control/access-control-model#environments-and-folders), backed by schemas, that hold your datasources and detection rules. Then it grants access so your team can start using Lakewatch. To tighten access later, see [Set up Lakewatch access control](/aws/en/lakewatch/admin/access-control/set-up-access-control).

To open Lakewatch, click the  app switcher in the top navigation bar of your workspace and select **Lakewatch**. Lakewatch isn't listed in the workspace sidebar. If **Lakewatch** isn't in the app switcher, a workspace admin must turn on the Lakewatch preview from the **Previews** page. See  [Manage workspace-level previews](/aws/en/admin/workspace-settings/manage-previews#workspace).

## Requirements

* Your workspace must meet the Lakewatch [prerequisites](/aws/en/lakewatch/admin/prerequisites), including Unity Catalog and serverless compute.
* A SQL warehouse selected under **Compute** in the **Environment, workspace and compute** menu in the top navigation bar. Setup won't continue until a warehouse is selected, and it uses that warehouse to initialize the catalog. Setup doesn't create a warehouse. See [SQL warehouse](/aws/en/lakewatch/admin/prerequisites#serverless-sql-warehouse). Detection rules also require a warehouse that meets a minimum Databricks SQL version. See [Detection warehouse prerequisites](/aws/en/lakewatch/admin/detection-warehouse#prerequisites).
* You must have one of the following:
  + `CREATE CATALOG` on the metastore, to create a new catalog. The Recommended configuration creates a new catalog.
  + `MANAGE` and `CREATE SCHEMA` on an existing catalog, to register it as the environment. Available only with Custom configuration.
* Permission to update the catalog's workspace bindings, if you change them during setup.

## When you see the setup screen

You see the **Welcome to Lakewatch** screen when you open Lakewatch and none of the catalogs you can access is registered as a Lakewatch environment. A Lakewatch environment is required, so you can't skip setup. After someone completes setup, you go straight to Lakewatch.

If you don't have `CREATE CATALOG` on the metastore but can access a catalog that isn't already a Lakewatch environment, the setup screen shows **Use an existing catalog** after you select **Get started with Lakewatch**. You can still complete setup on an existing catalog. See [Set up Lakewatch without CREATE CATALOG](#no-create-catalog). If you can't access any such catalog, the setup screen shows **Ask an administrator to set up Lakewatch** and **Additional permissions are needed** instead. In workspaces that were [enabled for Unity Catalog automatically](/aws/en/data-governance/unity-catalog/manage-privileges/admin-privileges#workspace-admins-auto), workspace administrators have this privilege by default. Otherwise, ask a metastore administrator or a user with `CREATE CATALOG` to complete setup.

## Complete setup

Select **Get started with Lakewatch** to open the **Configuration** section. **Recommended configuration** is selected by default. Choose a configuration before you select **Create**.

important

The Recommended configuration grants all account users Lakewatch admin on the new environment. To choose the catalog, folders, and who gets access before Lakewatch creates anything, select **Custom configuration** first.

1. Select **Get started with Lakewatch**.
2. Under **Configuration**, select a configuration:
   * **Recommended configuration**: Creates a new `lakewatch` catalog and lets everyone who can use the workspace administer Lakewatch. Use it to evaluate Lakewatch, or when everyone in the workspace should have full access.
   * **Custom configuration**: Lets you choose the catalog, folder names, and access before setup. Use it for production, to register an existing catalog, to limit who can administer Lakewatch, or if you don't have `CREATE CATALOG`.
3. Select **Create**. Lakewatch creates the catalog and schemas as needed, registers them as your environment and folders, applies the grants, and opens the Lakewatch overview page. If a step fails, select **Create** again to retry. Lakewatch keeps your choices.

You can change access after setup. See [Manage the environment after setup](#manage-the-environment-after-setup).

### Recommended configuration

The Recommended configuration sets up Lakewatch in one step. It does the following:

* Creates a new catalog named `lakewatch`. If a catalog with that name already exists, enter a different name.
* Creates two folders: `datasources` for datasources, and `detection` for detection rules and alerts.
* Grants all account users Lakewatch admin on the environment and every Lakewatch permission on both folders. Because the catalog is accessible only from this workspace, this effectively means everyone who can use the workspace can administer the environment and collaborate in it.
* Grants all account users `USE CATALOG` and `USE SCHEMA` on the catalog, so that secrets can be created in the `__lakewatch` schema. Custom configuration applies the same grants.
* Makes the catalog accessible only from the current workspace.

If you can't create a catalog, the Recommended configuration is unavailable. See [Set up Lakewatch without CREATE CATALOG](#no-create-catalog).

### Custom configuration

Use Custom configuration to set the initial names and access. It starts with the same settings as the Recommended configuration. To change a section, select the pencil icon next to it, make your changes, and select **Done**:

* **Environment**: Create a new catalog, or select an existing one. Lakewatch doesn't reuse an existing catalog unless you select it explicitly.
* **Workspace**: For an existing catalog, select whether to leave its workspace bindings unchanged (the default) or make the catalog accessible only from this workspace. Making it accessible only from this workspace removes its bindings to other workspaces. A new catalog is accessible only from this workspace.
* **Datasource folder** and **Detection & Alerts folder**: Rename each folder and set its permissions. Keep datasources and detection rules in separate folders. A single folder for both makes their read and edit permissions inseparable.
* **Admins**: Select who gets **Lakewatch admin** on the environment. Setup requires at least one administrator grant.

For each principal, select one or more permission groups, such as **Datasource manager** or **Alert triage**. Principals can be account users, account groups, or service principals. For what each permission group grants, see [Permission groups](/aws/en/lakewatch/admin/access-control/role-capability-matrix#permission-groups). To set up least-privilege access for a security team, follow [Set up Lakewatch access control](/aws/en/lakewatch/admin/access-control/set-up-access-control).

### Set up Lakewatch without CREATE CATALOG

If you don't have `CREATE CATALOG` on the metastore, the setup screen shows **Use an existing catalog**, and the Recommended configuration is unavailable. Set up Lakewatch on an existing catalog instead:

1. Select **Get started with Lakewatch**, and then select **Custom configuration**.
2. Next to **Environment**, select the pencil icon.
3. Select **Use an existing catalog**. Under **Existing catalog**, select a catalog where you have `MANAGE` and `CREATE SCHEMA`. The catalog can't already be a Lakewatch environment.
4. Select **Done**, review the other sections, and then select **Create**.

If your workspace was [enabled for Unity Catalog automatically](/aws/en/data-governance/unity-catalog/manage-privileges/#workspace-catalog), workspace admins own the workspace catalog, so a workspace admin can select it. If Lakewatch shows **You cannot configure this catalog**, you don't have `MANAGE` and `CREATE SCHEMA` on it. Choose another catalog, or ask the catalog owner to grant those privileges.

## Manage the environment after setup

To manage the environment, go to **Settings > Environment** and do any of the following:

* See the backing catalog and the workspace the environment is available from.
* Add and delete folders, and edit folder permissions.
* Add or revoke Lakewatch administrators.

Changing environment settings or administrators requires `MANAGE` on the catalog.

An environment is available only from the workspaces its catalog is bound to. If you open it from another workspace, Lakewatch shows **Environment unavailable**.

To add another environment, for example to separate development and production, select **Create environment**. The flow matches first-time setup and has the same requirements: `CREATE CATALOG` on the metastore, or `MANAGE` and `CREATE SCHEMA` on an existing catalog. Lakewatch admin doesn't include `CREATE CATALOG`, so a Lakewatch admin can't necessarily create an environment.

You can't change the catalog that backs an environment. A new catalog uses the default storage location. To use a catalog whose managed storage location is in a cloud storage bucket you own, create another environment, select **Custom configuration**, and select **Use an existing catalog**.

You can't delete an environment from Lakewatch. To remove one, [drop its backing catalog](/aws/en/sql/language-manual/sql-ref-syntax-ddl-drop-catalog) in Unity Catalog. Lakewatch then no longer lists the environment. Dropping a catalog permanently deletes its schemas and their contents, including the environment's folders.

### Add a folder

Select **Add folder** under **Folders**, then choose a **Schema** option:

* **Create a new schema**: Lakewatch creates a schema in the catalog and registers it as the folder. Requires `MANAGE` and `CREATE SCHEMA` on the catalog.
* **Use an existing schema**: Registers a schema that already exists in the catalog, for example one created outside Lakewatch. Requires `MANAGE` on the catalog, but not `CREATE SCHEMA`. The list shows only schemas you can access that aren't already folders.

### Delete a folder

Select **Delete** in the folder's row. The **Delete folder *name*?** dialog lists every item in the folder, both Lakewatch resources such as datasources and detection rules, and Unity Catalog items such as tables and volumes. You can't delete the folder until you delete each Lakewatch resource it lists. Deleting the folder permanently deletes its backing schema and every Unity Catalog item listed. You can't undo this. To delete a folder, you need permission to delete its backing schema in Unity Catalog.

## Additional resources

* [Configure Lakewatch settings](/aws/en/lakewatch/admin/workspace-config) for the environment.
* [Set up a detection warehouse](/aws/en/lakewatch/admin/detection-warehouse) to run detection rules.
* For least-privilege, team-based access, [set up access control](/aws/en/lakewatch/admin/access-control/set-up-access-control).
* Walk through the full workflow in the [end-to-end walkthrough](/aws/en/lakewatch/quickstart-guide).