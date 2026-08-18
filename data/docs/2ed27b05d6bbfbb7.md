Environment variables provide deployment-specific configuration to application code in serverless Lakeflow Jobs tasks. Define named environment variable entries on a job, then select an entry for each task that needs it. During Beta, you configure environment variables through the Jobs API.

Beta

This feature is in [Beta](/aws/en/release-notes/release-types). To use it, a workspace admin must turn on **Environment variables in Lakeflow Jobs** from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).

This page describes environment variables for serverless jobs. Serverless compute doesn't support init scripts. If your workload runs on classic compute, see [Set and use environment variables with init scripts](/aws/en/init-scripts/environment-variables).

## How environment variables work

Environment variable entries are defined at the job level. Each entry has a unique key, contains inline variables, and works with all serverless task types. An entry key can contain only letters, numbers, hyphens, and underscores. Each inline variable name must start with a letter or underscore and can contain only letters, numbers, and underscores.

Each task selects a single environment variable entry with `environment_variables_key` and receives only that entry's variables. Entries are never combined, and one entry can't inherit from another. A task that omits `environment_variables_key` receives no environment variables.

Environment variables are available only to application code that runs in the task process. They aren't available to Spark execution logic.

## Requirements

* A workspace admin has turned on **Environment variables in Lakeflow Jobs** from the **Previews** page. See [Manage Databricks previews](/aws/en/admin/workspace-settings/manage-previews).
* Tasks that run on serverless environment version 5 or later.

## Limitations

User-defined functions (UDFs) can't read environment variables, because UDFs run in Spark execution logic rather than the task process.

The following limits apply:

| Configuration | Limit |
| --- | --- |
| Environment variable entries per job | 10 |
| Entry key | 1–100 characters; must match `^[\w\-_]+$` |
| Inline variables per entry | 100 |
| Inline variable name | 1–256 characters; must match `^[A-Za-z_][A-Za-z0-9_]*$` |
| Inline variable value | 512 characters |

←✕

| Configuration | Limit |
| --- | --- |
| Environment variable entries per job | 10 |
| Entry key | 1–100 characters; must match `^[\w\-_]+$` |
| Inline variables per entry | 100 |
| Inline variable name | 1–256 characters; must match `^[A-Za-z_][A-Za-z0-9_]*$` |
| Inline variable value | 512 characters |

## Configure environment variables with the Jobs API

Use the `environment_variables` field in a [`POST /api/2.2/jobs/create`](https://docs.databricks.com/api/workspace/jobs/create) request to define environment variable entries. Set `environment_variables_key` on each task that uses an entry.

The following example defines separate environment variable entries for a notebook task and a JAR task. Each task selects its entry with `environment_variables_key`, and any serverless task type can use an entry the same way:

JSON

```
{  
  "name": "serverless-environment-variables-example",  
  "tasks": [  
    {  
      "task_key": "process_orders",  
      "notebook_task": {  
        "notebook_path": "/Workspace/Shared/process-orders"  
      },  
      "environment_key": "default",  
      "environment_variables_key": "production"  
    },  
    {  
      "task_key": "summarize",  
      "spark_jar_task": {  
        "main_class_name": "com.company.main"  
      },  
      "environment_key": "summary_env",  
      "environment_variables_key": "summary_vars"  
    }  
  ],  
  "environments": [  
    {  
      "environment_key": "default",  
      "spec": {  
        "environment_version": "5",  
        "dependencies": []  
      }  
    },  
    {  
      "environment_key": "summary_env",  
      "spec": {  
        "environment_version": "5",  
        "java_dependencies": ["/Volumes/company/default/prod/summarize.jar"]  
      }  
    }  
  ],  
  "environment_variables": [  
    {  
      "environment_variables_key": "production",  
      "variables": {  
        "APP_ENV": "production",  
        "REGION": "us-west-2"  
      }  
    },  
    {  
      "environment_variables_key": "summary_vars",  
      "variables": {  
        "APP_ENV": "production",  
        "LOG_LEVEL": "INFO",  
        "LOG_FILE": "service.log"  
      }  
    }  
  ]  
}
```

You can also configure environment variable entries with the [Update a job](https://docs.databricks.com/api/workspace/jobs/update), [Overwrite all settings for a job](https://docs.databricks.com/api/workspace/jobs/reset), and [Submit a one-time run](https://docs.databricks.com/api/workspace/jobs/submit) operations.

## Read environment variables in application code

Application code reads configured variables from the process environment.

* Python
* Scala

Python

```
import os  
  
app_environment = os.environ["APP_ENV"]  
region = os.environ["REGION"]
```

Scala

```
val appEnvironment = sys.env("APP_ENV")  
val region = sys.env("REGION")
```

## Additional resources

* [Run your Lakeflow Jobs with serverless compute for workflows](/aws/en/jobs/run-serverless-jobs)
* [Configure the serverless environment](/aws/en/compute/serverless/dependencies)