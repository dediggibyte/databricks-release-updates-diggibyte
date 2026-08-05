This page explains core concepts of the Unity Catalog permissions model, including the object model, privileges, ownership, and inheritance.

For a general reference of all Unity Catalog privileges, see [Unity Catalog privileges reference](/aws/en/data-governance/unity-catalog/access-control/privileges-reference). For instructions on granting and revoking privileges, see [Show, grant, and revoke privileges](/aws/en/data-governance/unity-catalog/manage-privileges/#grant).

## Securable objects

In Unity Catalog, data and metadata live in a top-level container called a metastore. Within this metastore, data is represented as objects in a three-level namespace: `catalog`.`schema`.`table`. This hierarchical structure also provides the foundation for access control in Unity Catalog.

Every object in this hierarchy is a **securable object**. Access control in Unity Catalog works by granting privileges, such as `SELECT`, `MODIFY`, or `USE SCHEMA`, on these securable objects. This model provides fine-grained control over who can access and manage data across your organization.

For a complete list of securable objects and the privileges that apply to each, see [Unity Catalog privileges reference](/aws/en/data-governance/unity-catalog/access-control/privileges-reference).

### Container objects

Some securable objects in Unity Catalog are **container objects**, meaning they contain child objects within the hierarchy. Container objects have a special role in the permissions model because privileges granted on them can affect their children through inheritance.

The following are container objects in Unity Catalog:

* Catalogs: The top level of the three-level namespace. Catalogs contain schemas as direct children.
* Schemas: The middle level of the three-level namespace. Schemas contain tables, views, volumes, and functions as direct children.

Container objects have several important characteristics:

| Characteristic | Description |
| --- | --- |
| Privilege inheritance | When you grant a privilege on a container object, that privilege automatically applies to all current and future child objects. For example, granting `SELECT` on a catalog allows users to read all tables in that catalog (with appropriate usage privileges). See [Privilege inheritance](#inheritance). |
| Usage privileges | Access to child objects requires the appropriate `USE CATALOG` or `USE SCHEMA` privilege on the parent container objects. See [Usage privileges](#usage-privileges). |
| Ability to manage child objects | When you own a container object, you automatically get the ability to manage all child objects, even if you don't own those children directly. See [Ownership](#ownership). |
| Creation privileges | Container objects support privileges that allow users to create child objects within them, such as `CREATE SCHEMA` on catalogs and `CREATE TABLE` on schemas. |

←✕

| Characteristic | Description |
| --- | --- |
| Privilege inheritance | When you grant a privilege on a container object, that privilege automatically applies to all current and future child objects. For example, granting `SELECT` on a catalog allows users to read all tables in that catalog (with appropriate usage privileges). See [Privilege inheritance](#inheritance). |
| Usage privileges | Access to child objects requires the appropriate `USE CATALOG` or `USE SCHEMA` privilege on the parent container objects. See [Usage privileges](#usage-privileges). |
| Ability to manage child objects | When you own a container object, you automatically get the ability to manage all child objects, even if you don't own those children directly. See [Ownership](#ownership). |
| Creation privileges | Container objects support privileges that allow users to create child objects within them, such as `CREATE SCHEMA` on catalogs and `CREATE TABLE` on schemas. |

Non-container objects, like tables, views, volumes, and functions, don't contain child objects.

## Privileges

Privileges determine what actions a user or group can perform on a securable object. Common privileges include:

* `SELECT`: Read data from tables or views
* `MODIFY`: Write data to tables or views
* `USE CATALOG`: Access a catalog (requires additional privileges to work with child objects)
* `USE SCHEMA`: Access a schema (requires additional privileges to work with child objects)
* `CREATE TABLE`: Create tables within a schema

A user or group must be explicitly granted a privilege to perform an action.

The following sections describe important special privileges in Databricks. For a complete reference of all privileges, see [Unity Catalog privileges reference](/aws/en/data-governance/unity-catalog/access-control/privileges-reference).

### Usage privileges

`USE CATALOG` and `USE SCHEMA` are usage privileges. Generally, usage privileges are a prerequisite to interact with an object and its child objects in the hierarchy.

To work with any object in a catalog, you need the `USE CATALOG` privilege on the catalog, and to work with any object in a schema, you need the `USE SCHEMA` privilege on the schema. Managing an object with the `MANAGE` privilege is an exception, with reduced usage privilege requirements. See [Usage privilege requirements for `MANAGE`](#manage-usage-requirements).

For example, to perform most operations on tables, views, volumes, or functions, you need:

1. `USE CATALOG` on the parent catalog
2. `USE SCHEMA` on the parent schema
3. The specific privilege for the operation (such as `SELECT`, `MODIFY`, or `EXECUTE`)

All three are required. Having only the `SELECT` privilege on a table is not sufficient to read it if you lack `USE CATALOG` or `USE SCHEMA` on its parent objects.

Usage privileges provide an important access control mechanism for higher-level administrators. For example, even if a table owner wants to share their table with other users, those users cannot access the table without `USE CATALOG` and `USE SCHEMA` privileges on the parent objects. Because only catalog and schema owners or users with the `MANAGE` privilege can grant these usage privileges, this prevents table owners from granting access outside approved boundaries.

#### Usage privilege requirements for `MANAGE`

The `MANAGE` privilege has reduced usage privilege requirements. To exercise `MANAGE`, you don't need a usage privilege at the level where `MANAGE` is granted: `MANAGE` on a catalog doesn't require `USE CATALOG` on that catalog, and `MANAGE` on a schema doesn't require `USE SCHEMA` on that schema. You need the usage privilege only on the container levels strictly *above* the level where you hold `MANAGE`, not at or below that level. On each of those higher levels, you can satisfy the requirement with `USE CATALOG` or `USE SCHEMA`, or with ownership or `MANAGE`. Because `MANAGE` on a container is inherited by all of its child objects, holding `MANAGE` at a higher level means you need no usage privileges below it. For example:

* `MANAGE` on a catalog requires no usage privileges. You can manage the catalog and any schema, table, or other object within it without `USE CATALOG` or `USE SCHEMA`.
* `MANAGE` on a schema requires `USE CATALOG` on the parent catalog (or ownership or `MANAGE` on that catalog), but not `USE SCHEMA` on the schema.
* `MANAGE` on a non-container object, such as a table, view, volume, or function, requires `USE CATALOG` on the parent catalog and `USE SCHEMA` on the parent schema (or ownership or `MANAGE` on either parent).

This reduction applies only to the metadata capabilities that `MANAGE` provides. Data-access privileges such as `SELECT` and `MODIFY` still require `USE CATALOG` and `USE SCHEMA`, even for users with `MANAGE`. For more information about what `MANAGE` allows, see [The `MANAGE` privilege](#manage-privilege).

The following table shows common operations and their required privileges:

| Operation | Required privileges |
| --- | --- |
| Read data from a table or view | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `SELECT` on table or view |
| Write data to a table | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `MODIFY` on table |
| Create a schema in a catalog | `USE CATALOG` on catalog, `CREATE SCHEMA` on catalog |
| Create a table in a schema | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `CREATE TABLE` on schema (or catalog if granted at catalog-level) |
| Execute a function | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `EXECUTE` on function |
| Read files from a volume | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `READ VOLUME` on volume |
| Manage a catalog (grant privileges, transfer ownership, drop) | `MANAGE` on catalog (no usage privileges required) |
| Manage a schema (grant privileges, transfer ownership, drop) | `USE CATALOG` on catalog, `MANAGE` on schema |
| Manage a table, view, volume, or function (grant privileges, transfer ownership, drop) | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `MANAGE` on the object |

←✕

| Operation | Required privileges |
| --- | --- |
| Read data from a table or view | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `SELECT` on table or view |
| Write data to a table | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `MODIFY` on table |
| Create a schema in a catalog | `USE CATALOG` on catalog, `CREATE SCHEMA` on catalog |
| Create a table in a schema | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `CREATE TABLE` on schema (or catalog if granted at catalog-level) |
| Execute a function | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `EXECUTE` on function |
| Read files from a volume | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `READ VOLUME` on volume |
| Manage a catalog (grant privileges, transfer ownership, drop) | `MANAGE` on catalog (no usage privileges required) |
| Manage a schema (grant privileges, transfer ownership, drop) | `USE CATALOG` on catalog, `MANAGE` on schema |
| Manage a table, view, volume, or function (grant privileges, transfer ownership, drop) | `USE CATALOG` on catalog, `USE SCHEMA` on schema, `MANAGE` on the object |

### `ALL PRIVILEGES` behavior

`ALL PRIVILEGES` *implies* all applicable privileges for a specific object type, without Databricks explicitly granting each individual privilege. For example:

* `ALL PRIVILEGES` on a table implies the ability to perform `SELECT`, `MODIFY`, and `APPLY TAG`.
* `ALL PRIVILEGES` on a volume implies the ability to perform `READ VOLUME`, `WRITE VOLUME`, and `APPLY TAG`.
* `ALL PRIVILEGES` on a schema implies all schema-level privileges.
* `ALL PRIVILEGES` on a catalog implies all catalog-level privileges.

`ALL PRIVILEGES` does not include the `EXTERNAL USE SCHEMA`, `EXTERNAL USE LOCATION`, or `MANAGE` privileges.

For more details on how `ALL PRIVILEGES` is evaluated and revoked, see [ALL PRIVILEGES](/aws/en/data-governance/unity-catalog/access-control/privileges-reference#all-privileges).

### The `MANAGE` privilege

The `MANAGE` privilege allows users to manage privileges on, transfer ownership of, and delete an object without being the owner. Having `MANAGE` is similar to ownership, but there are some important differences. See [Ownership versus the `MANAGE` privilege](#ownership-vs-manage).

To exercise `MANAGE`, users need the appropriate usage privileges on the parent containers above the object where `MANAGE` is granted, but not on that object itself. For example, `MANAGE` on a catalog requires no usage privileges at all. For full details, see [Usage privilege requirements for `MANAGE`](#manage-usage-requirements).

If `MANAGE` is granted on a container object, the user also gets `MANAGE` on all child objects.

For full details, see [MANAGE](/aws/en/data-governance/unity-catalog/access-control/privileges-reference#manage).

### The `BROWSE` privilege

`BROWSE` allows users to discover objects and view their metadata without granting access to the underlying data. Users with `BROWSE` can see that an object exists, view its name, description, and tags, and request access to it without needing `USE CATALOG` or `USE SCHEMA`.

`BROWSE` is granted at the catalog level and applies to all objects within that catalog. Databricks recommends granting `BROWSE` on catalogs to the `All account users` group to make data discoverable throughout your organization.

For full details, see [BROWSE](/aws/en/data-governance/unity-catalog/access-control/privileges-reference#browse).

## Ownership

Every securable object in Unity Catalog has an owner. The owner can be a user, service principal, or group. The principal that creates an object becomes its initial owner.

Ownership has a special denotation in Unity Catalog. Object owners can automatically perform all capabilities on the object they own. However, Databricks doesn't explicitly grant the `ALL PRIVILEGES` privilege to the owner. This means you won't see `ALL PRIVILEGES` returned when listing permissions using the Databricks API or with a [`SHOW GRANTS` command](/aws/en/sql/language-manual/security-show-grant).

Ownership doesn't inherit downward in Unity Catalog. However, object owners do automatically have the ability to manage all child objects. For example, if you own a catalog, you don't automatically own the child schemas within the catalog, but you can manage all child schemas. Similar to owners having all capabilities on their object without explicitly having `ALL PRIVILEGES`, Databricks also doesn't explicitly grant the `MANAGE` privilege in this case.

Object owners can perform other important operations on the object, including granting and revoking permissions, transferring ownership, and dropping the object.

note

To avoid accidental data exfiltration, schema owners do not have the `EXTERNAL USE SCHEMA` privilege by default and external location owners do not have the `EXTERNAL USE LOCATION` privilege by default. See [Enable external data access to Unity Catalog](/aws/en/external-access/admin).

To summarize, the owner of an object can do the following:

| Capability | Description |
| --- | --