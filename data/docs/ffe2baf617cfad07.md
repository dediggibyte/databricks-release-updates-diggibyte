Register an [external model provider](/aws/en/ai-gateway/model-provider-services) as a model provider service, grant access to it, configure Unity Gateway features, and delete it.

## Requirements

* `CREATE SERVICE` on the schema where you create the model provider service, plus `USE CATALOG` and `USE SCHEMA` on its catalog and schema.
* The credentials for the external provider you want to register (for example, an OpenAI API key or an AWS access key pair).
* To authenticate Amazon Bedrock with a service credential instead of an access key pair, you must have an existing service credential and `ACCESS` on it. See [Authenticate Amazon Bedrock with a service credential](#bedrock-service-credential).

To back a provider credential with a customer-owned Unity Catalog secret instead of storing the value inline, you must have an existing Unity Catalog secret and `READ SECRET` on it. See [Back a provider credential with a Unity Catalog secret](#uc-secret-auth).

## Create a model provider service

Model provider services and [model services](/aws/en/ai-gateway/model-services) share a single name namespace within a Unity Catalog schema. You can't use a name for a model provider service if a model service in the schema already uses it, and vice versa.

Create a model provider service in the Unity Gateway UI or Catalog Explorer. To create one programmatically, use the REST API, the Databricks SDKs, the Databricks CLI, Terraform, or Declarative Automation Bundles (DABs).

* UI
* REST API
* CLI
* Terraform
* DABs (Beta)
* Python SDK
* Go SDK
* Java SDK
* JS SDK

1. Do one of the following:
   * In the workspace sidebar, click **AI Gateway**, then open the **Providers** tab and click **Provider**.
   * In Catalog Explorer, go to the schema where you want to create the model provider service, click **Create** > **Service**, then select **Model provider service** in the **Create a service** dialog.
2. Enter a name for the model provider service, and select the catalog and schema to create it in. If you start from Catalog Explorer, Catalog Explorer prefills the catalog and schema.
3. Select the provider type, and enter the provider's connection details and credentials.
4. Click **Create**. Databricks encrypts and stores the credentials. The UI does not display them after this point.

Send a `POST` to [/api/2.1/unity-catalog/model-provider-services](https://docs.databricks.com/api/ai-gateway/v1/create-model-provider-service), passing `parent` and `model_provider_service_id` as query parameters. Set `provider_type` and exactly one matching provider block; `targets` allowlists the reachable upstream models, and secrets are supplied inline as plaintext:

Bash

```
databricks api post \  
  "/api/2.1/unity-catalog/model-provider-services?parent=schemas/main.default&model_provider_service_id=my_provider" \  
  --json '{  
  "comment": "Routes to a custom OpenAI-compatible provider",  
  "config": {  
    "provider_type": "EXTERNAL_MODEL_PROVIDER_TYPE_CUSTOM",  
    "targets": [  
      { "model": "gpt-4o", "native_api_types": ["openai/v1/chat/completions"] }  
    ],  
    "custom": {  
      "direct": {  
        "base_url": "https://api.example.com/v1",  
        "api_key": { "plaintext": "dummy-api-key" }  
      }  
    }  
  }  
}'
```

Pass the parent schema and a leaf name, and supply the config with `--json`. Set `provider_type` and exactly one matching provider block; `targets` allowlists the reachable upstream models, and secrets are supplied inline as plaintext. To install the CLI, see [Install or update the Databricks CLI](/aws/en/dev-tools/cli/install).

Bash

```
databricks ai-gateway create-model-provider-service schemas/main.default my_provider --json '{  
  "comment": "Routes to a custom OpenAI-compatible provider",  
  "config": {  
    "provider_type": "EXTERNAL_MODEL_PROVIDER_TYPE_CUSTOM",  
    "targets": [  
      { "model": "gpt-4o", "native_api_types": ["openai/v1/chat/completions"] }  
    ],  
    "custom": {  
      "direct": {  
        "base_url": "https://api.example.com/v1",  
        "api_key": { "plaintext": "dummy-api-key" }  
      }  
    }  
  }  
}'
```

Create and manage a model provider service with the [Databricks Terraform provider](/aws/en/dev-tools/terraform/) and the [databricks\_ai\_gateway\_model\_provider\_service](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/ai_gateway_model_provider_service) resource. Keep real keys out of source control by passing the API key through a `sensitive = true` variable (set it with `-var` or a `TF_VAR_provider_api_key` environment variable):

Hcl

```
variable "provider_api_key" {  
  type      = string  
  sensitive = true  
}  
  
resource "databricks_ai_gateway_model_provider_service" "example" {  
  parent                    = "schemas/main.default"  
  model_provider_service_id = "my_provider"  
  comment                   = "Routes to a custom OpenAI-compatible provider"  
  
  config = {  
    provider_type = "EXTERNAL_MODEL_PROVIDER_TYPE_CUSTOM"  
  
    targets = [{  
      model            = "gpt-4o"  
      native_api_types = ["openai/v1/chat/completions"]  
    }]  
  
    custom = {  
      direct = {  
        base_url = "https://api.example.com/v1"  
        api_key  = { plaintext = var.provider_api_key }  
      }  
    }  
  }  
}
```

Define the model provider service in a [bundle](/aws/en/dev-tools/bundles/) and deploy it with `databricks bundle deploy`. Keep real keys out of source control by passing the API key through a bundle variable (set it with `--var` or a `BUNDLE_VAR_provider_api_key` environment variable):

YAML

```
variables:  
  provider_api_key:  
    description: Provider API key.  
  
resources:  
  model_provider_services:  
    my_provider:  
      parent: schemas/main.default  
      model_provider_service_id: my_provider  
      comment: Routes to a custom OpenAI-compatible provider  
      config:  
        provider_type: EXTERNAL_MODEL_PROVIDER_TYPE_CUSTOM  
        targets:  
          - model: gpt-4o  
            native_api_types: [openai/v1/chat/completions]  
        custom:  
          direct:  
            base_url: https://api.example.com/v1  
            api_key:  
              plaintext: ${var.provider_api_key}
```

Create and manage a model provider service with the [Databricks SDK for Python](/aws/en/dev-tools/sdk-python):

Python

```
from databricks.sdk.service import catalog as c  
  
model_provider_service = w.ai_gateway.create_model_provider_service(  
    parent="schemas/main.default",  
    model_provider_service_id="my_provider",  
    model_provider_service=c.ModelProviderService(  
        comment="Routes to a custom OpenAI-compatible provider",  
        config=c.ModelProviderServiceConfig(  
            provider_type=(  
                c.ModelProviderServiceConfigExternalModelProviderType  
                .EXTERNAL_MODEL_PROVIDER_TYPE_CUSTOM  
            ),  
            targets=[  
                c.ModelProviderServiceConfigModelTargetConfig(  
                    model="gpt-4o",  
                    native_api_types=["openai/v1/chat/completions"],  
                )  
            ],  
            custom=c.ModelProviderServiceConfigCustomProviderConfig(  
                direct=c.ModelProviderServiceConfigCustomProviderDirectConfig(  
                    base_url="https://api.example.com/v1",  
                    api_key=c.ModelProviderServiceConfigProviderSecret(  
                        plaintext="dummy-api-key"  
                    ),  
                )  
            ),  
        ),  
    ),  
)
```

Create and manage a model provider service with the [Databricks SDK for Go](/aws/en/dev-tools/sdk-go):

Go

```
modelProviderService, err := w.AiGateway.CreateModelProviderService(ctx,  
	catalog.CreateModelProviderServiceRequest{  
		Parent:                 "schemas/main.default",  
		ModelProviderServiceId: "my_provider",  
		ModelProviderService: catalog.ModelProviderService{  
			Comment: "Routes to a custom OpenAI-compatible provider",  
			Config: &catalog.ModelProviderServiceConfig{  
				ProviderType: catalog.ModelProviderServiceConfigExternalModelProviderTypeExternalModelProviderTypeCustom,  
				Targets: []catalog.ModelProviderServiceConfigModelTargetConfig{{  
					Model:          "gpt-4o",  
					NativeApiTypes: []string{"openai/v1/chat/completions"},  
				}},  
				Custom: &catalog.ModelProviderServiceConfigCustomProviderConfig{  
					Direct: &catalog.ModelProviderServiceConfigCustomProviderDirectConfig{  
						BaseUrl: "https://api.example.com/v1",  
						ApiKey: &catalog.ModelProviderServiceConfigProviderSecret{  
							Plaintext: "dummy-api-key",  
						},  
					},  
				},  
			},  
		},  
	})
```

Create and manage a model provider service with the [Databricks SDK for Java](/aws/en/dev-tools/sdk-java):

Java

```
ModelProviderServiceConfig config =  
    new ModelProviderServiceConfig()  
        .setProviderType(  
            ModelProviderServiceConfigExternalModelProviderType  
                .EXTERNAL_MODEL_PROVIDER_TYPE_CUSTOM)  
        .setTargets(  
            Collections.singletonList(  
                new ModelProviderServiceConfigModelTargetConfig()  
                    .setModel("gpt-4o")  
                    .setNativeApiTypes(  
                        Collections.singletonList("openai/v1/chat/completions"))))  
        .setCustom(  
            new ModelProviderServiceConfigCustomProviderConfig()  
                .setDirect(  
                    new ModelProviderServiceConfigCustomProviderDirectConfig()  
                        .setBaseUrl("https://api.example.com/v1")  
                        .setApiKey(  
                            new ModelProviderServiceConfigProviderSecret()  
                                .setPlaintext("dummy-api-key"))));  
  
ModelProviderService modelProviderService =  
    w.aiGateway()  
        .createModelProviderService(  
            new CreateModelProviderServiceRequest()  
                .setParent("schemas/main.default")  
                .setModelProviderServiceId("my_provider")  
                .setModelProviderService(  
                    new ModelProviderService()  
                        .setComment("Routes to a custom OpenAI-compatible provider")  
                        .setConfig(config)));
```

Create and manage a model provider service with the [Databricks AI Gateway SDK for JavaScript](https://www.npmjs.com/package/@databricks/sdk-aigateway):

TypeScript

```
import { ModelProviderServiceConfig_ExternalModelProviderType as ProviderType } from '@databricks/sdk-aigateway/v1';  
  
const created = await client.createModelProviderService({  
  parent: 'schemas/main.default',  
  modelProviderServiceId: 'my_provider',  
  modelProviderService: {  
    comment: 'Routes to a custom OpenAI-compatible provider',  
    config: {  
      providerType: ProviderType.EXTERNAL_MODEL_PROVIDER_TYPE_CUSTOM,  
      targets: [{ model: 'gpt-4o', nativeApiTypes: ['openai/v1/chat/completions'] }],  
      provider: {  
        $case: 'custom',  
        custom: {  
          providerMode: {  
            $case: 'direct',  
            direct: {  
              baseUrl: 'https://api.example.com/v1',  
              authMode: {  
                $case: 'apiKey',  
                apiKey: {  
                  value: { $case: 'plaintext', plaintext: 'dummy-api-key' },  
                },  
              },  
            },  
          },  
        },  
      },  
    },  
  },  
});
```

For the full list of providers and their authentication methods, see [Govern external model providers (model provider services)](/aws/en/ai-gateway/model-provider-services).

## Authenticate Amazon Bedrock with a service credential

You can authenticate an Amazon Bedrock provider with a [service credential](/aws/en/connect/unity-catalog/cloud-services/service-credentials) instead of storing an AWS access key pair. A service credential holds an identity and access management (IAM) role that Unity Catalog governs, so no long-lived AWS key is copied into the model provider service: Databricks obtains short-lived credentials from the role to authenticate each request.

Create the model provider service as described in [Create a model provider service](#create-mps). Select **Amazon Bedrock** as the provider type, then set **Auth method** to **Service credential** and select the credential instead of entering an access key pair.

Confirm the following requirements:

* The owner of the model provider service has `ACCESS` on the service credential. Because Databricks re-checks the owner's access when serving requests, the owner must keep it for as long as the provider is in use. Revoking it stops queries for everyone, even callers who hold `EXECUTE` on the provider. To grant the owner access to the credential:

  SQL

  ```
  GRANT ACCESS ON SERVICE CREDENTIAL <service-credential-name> TO `<model-provider-service-owner>`;
  ```
* The credential's purpose is **service**, not storage.
* The credential is available in the workspaces requests come from. Its workspace bindings still apply, so a request from a workspace the credential isn't bound to fails there, even though the model provider service itself is reachable from any workspace that shares the metastore.
* The service credential IAM role can invoke the Bedrock models you plan to query. To create one, see [Create service credentials](/aws/en/connect/unity-catalog/cloud-services/service-credentials).

Callers who query the provider need the same grants as for any other provider. They don't need any privilege on the service credential, which is what keeps the credential itself out of their reach.

The model provider service tracks a credential by its internal identifier, so you can rename a credential without query failure.

If you delete a credential, queries fail and there is no warning that a model provider service references it. Confirm that there ar