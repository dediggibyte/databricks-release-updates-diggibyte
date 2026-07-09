On this page

Last updated on **Jun 19, 2026**

This page describes how Lakebase Postgres is compatible with standard Postgres. As a managed Postgres service, there are some differences and limitations.

## Postgres version support[​](#postgres-version-support "Direct link to postgres-version-support")

Lakebase Autoscaling supports Postgres 16, Postgres 17, and Postgres 18. Postgres 17 is the default version. To use Postgres 18, select it when creating a new project.

## Postgres extension support[​](#postgres-extension-support "Direct link to postgres-extension-support")

Lakebase supports numerous Postgres extensions. For the full list, see [Postgres extensions](/aws/en/oltp/projects/extensions).

## Session, memory, and storage[​](#session-memory-and-storage "Direct link to session-memory-and-storage")

### Session context[​](#session-context "Direct link to Session context")

The Lakebase scale-to-zero feature automatically closes idle connections after a period of inactivity.

When connections are closed, anything in the session context, such as temporary tables, prepared statements, advisory locks, and [NOTIFY](https://www.postgresql.org/docs/current/sql-notify.html) and [LISTEN](https://www.postgresql.org/docs/current/sql-listen.html) commands, is lost.

To avoid losing session-level contexts, you can disable scale-to-zero. However, doing so means your compute runs 24/7.

### Memory[​](#memory "Direct link to Memory")

SQL queries and index builds can generate large volumes of data that may not fit in memory. The size of your compute determines the amount of memory available.

### Unlogged tables[​](#unlogged-tables "Direct link to Unlogged tables")

Unlogged tables are tables that do not write to the Postgres write-ahead log (WAL). These tables are stored in compute local storage and are not persisted across compute restarts or when a compute scales to zero. This is unlike standard Postgres, where unlogged tables are only truncated in the event of abnormal process termination. Additionally, unlogged tables are limited by compute local disk space. Lakebase computes allocate 20 GiB of local disk space or 15 GiB times the maximum compute size (whichever is highest) for temporary files used by Postgres.

### Temporary tables[​](#temporary-tables "Direct link to Temporary tables")

Temporary tables exist only for the lifetime of a session (or optionally a transaction). Like unlogged tables, they are stored in compute local storage and limited by local disk space.

## Postgres logs[​](#postgres-logs "Direct link to postgres-logs")

Access to Postgres logs is not supported.

## Statistics collection[​](#statistics-collection "Direct link to statistics-collection")

Statistics collected by the Postgres [cumulative statistics system](https://www.postgresql.org/docs/current/monitoring-stats.html) are not saved when a compute (where Postgres runs) scales to zero. To avoid losing statistics, you can disable the scale-to-zero feature. However, disabling scale to zero also means that your compute will run 24/7.

## Postgres parameter settings[​](#postgres-parameter-settings "Direct link to postgres-parameter-settings")

As a managed Postgres service, many database parameters are set based on the compute size. See all of your database parameter settings using:

PostgreSQL

```
SHOW ALL;
```

You can configure parameters that have a `user` context at the session, database, or role level. You cannot configure parameters at the instance level.

* Show parameters that can be set at the session, database, or role level.

  PostgreSQL

  ```
  SELECT name  
  FROM pg_settings  
  WHERE context = 'user';
  ```
* Set a parameter for the session.

  PostgreSQL

  ```
  SET maintenance_work_mem='1 GB';
  ```
* Set a parameter for all sessions connected to a database.

  PostgreSQL

  ```
  ALTER DATABASE databricks_postgres SET maintenance_work_mem='1 GB';
  ```
* Set a parameter for all sessions from a given user.

  PostgreSQL

  ```
  ALTER USER "john@company.com" SET maintenance_work_mem='1 GB';
  ```

## Database encoding and collations[​](#database-encoding-and-collations "Direct link to database-encoding-and-collations")

### Database encoding[​](#database-encoding "Direct link to Database encoding")

By default, the C.UTF-8 collation is used. C.UTF-8 supports the full range of UTF-8 encoded characters.

The UTF8 encoding (Unicode, 8-bit variable-width encoding) is also supported.

To view the encoding and collation for your database, run the following query:

PostgreSQL

```
SELECT  
    pg_database.datname AS database_name,  
    pg_encoding_to_char(pg_database.encoding) AS encoding,  
    pg_database.datcollate AS collation,  
    pg_database.datctype AS ctype  
FROM  
    pg_database  
WHERE  
    pg_database.datname = 'your_database_name';
```

note

In Postgres, you can't change a database's encoding or collation after it has been created.

### Collations[​](#collations "Direct link to collations")

A collation is an SQL schema object that maps an SQL name to locales provided by libraries installed in the operating system.

By default, Lakebase uses the `C.UTF-8` collation. Another provider supported by Lakebase is `icu`, which uses the external [ICU](https://icu.unicode.org/) library.

Lakebase provides a full series of [predefined icu locales](https://www.postgresql.org/docs/current/collation.html#COLLATION-MANAGING-PREDEFINED-ICU) in case you require locale-specific sorting or case conversions.

* View all predefined locales:

PostgreSQL

```
SELECT * FROM pg_collation;
```

* Create a database with a predefined `icu` locale:

PostgreSQL

```
CREATE DATABASE my_arabic_db  
LOCALE_PROVIDER icu  
icu_locale 'ar-x-icu'  
template template0;
```

* Specify a locale for individual columns:

PostgreSQL

```
CREATE TABLE my_ru_table (  
    id serial PRIMARY KEY,  
    russian_text_column text COLLATE "ru-x-icu",  
    description text  
);
```

## Functionality limitations[​](#functionality-limitations "Direct link to functionality-limitations")

### Roles and permissions[​](#roles-and-permissions "Direct link to roles-and-permissions")

* You can't access the host operating system.
* You can't connect using Postgres `superuser`.
  + Any functionality that requires `superuser` privileges or direct local file system access is not allowed.
  + The `databricks_superuser` takes the place of the Postgres `superuser` role. For information about the privileges associated with this role, see [Manage roles](/aws/en/oltp/projects/manage-roles).

### Replication[​](#replication "Direct link to replication")

Replicating data to or from a Lakebase database using native Postgres logical replication is not yet available.

### Tablespaces[​](#tablespaces "Direct link to tablespaces")

Lakebase doesn't support Postgres [tablespaces](https://www.postgresql.org/docs/current/manage-ag-tablespaces.html). Attempting to create a tablespace with the `CREATE TABLESPACE` command results in an error. This is because of Lakebase's managed cloud architecture, which doesn't permit direct file system access for custom storage locations.

If you have existing applications or scripts that use tablespaces for organizing database objects across different storage devices, you must remove or modify these references when migrating to Lakebase.