This page describes packaged clean rooms, a provider-consumer collaboration model for Databricks clean rooms.

In a packaged clean room, one collaborator is the *provider* and one is the *consumer*:

* The **provider** authors the notebooks and JARs and contributes data assets. The provider's code and data assets are hidden from the consumer.
* The **consumer** contributes their own data assets, triggers runs, and can view the run output. The consumer cannot view the provider's notebook or JAR code or the provider's data assets.

Neither collaborator can see the other's data assets. Either the provider or the consumer can create the clean room; whoever creates it designates which collaborator is the package provider. See [Create clean rooms](/aws/en/clean-rooms/create-clean-room) and [Work with Databricks clean rooms as an invited collaborator](/aws/en/clean-rooms/clean-room-collaborator).

This differs from an approval-based clean room, where all collaborators have equal privileges and can review every notebook before it runs. See [How does Clean Rooms ensure a no-trust environment?](/aws/en/clean-rooms/#no-trust). A packaged clean room is useful when a provider wants to offer a packaged analysis—similar to a private library—that a consumer can run against their own data without inspecting the provider's code.

## How packaged clean rooms differ from approval-based clean rooms

The following table compares the capabilities of each collaborator in a packaged clean room with those in an approval-based clean room:

| Capability | Approval-based | Packaged (consumer) | Packaged (provider) |
| --- | --- | --- | --- |
| View notebooks and JARs | All code visible | Names only, no code | Own notebooks and JARs |
| Add notebooks and JARs | Yes | No | Yes |
| View data assets | All visible | Own assets only | Own assets only |
| Add data assets | Yes | Yes | Yes |
| View run output | Yes | Yes | No |
| Access output tables | Runner only | Consumer (runner) only | No |
| Access shared output tables | Yes | Yes | Yes |
| Trigger runs | Yes | Yes | No |
| Auto-approval rules | Yes | No | No |

←✕

| Capability | Approval-based | Packaged (consumer) | Packaged (provider) |
| --- | --- | --- | --- |
| View notebooks and JARs | All code visible | Names only, no code | Own notebooks and JARs |
| Add notebooks and JARs | Yes | No | Yes |
| View data assets | All visible | Own assets only | Own assets only |
| Add data assets | Yes | Yes | Yes |
| View run output | Yes | Yes | No |
| Access output tables | Runner only | Consumer (runner) only | No |
| Access shared output tables | Yes | Yes | Yes |
| Trigger runs | Yes | Yes | No |
| Auto-approval rules | Yes | No | No |

## Security and trust model

Because the consumer cannot inspect the provider's notebook or JAR code, the consumer must trust that the provider's code behaves as described, similar to using a private library.

The clean room's egress network policy controls whether the provider's code can reach the internet or specific external endpoints. If egress is open, or if it allows endpoints that the consumer is not comfortable with, the provider's code could potentially send the consumer's data outside the clean room.

Before you contribute sensitive data to a packaged clean room, review its egress network policy. See [What is serverless egress control?](/aws/en/security/network/serverless-network-security/network-policies).

## Before you begin

* Packaged mode is set when the clean room is created and cannot be changed afterward.

## Create a packaged clean room

Either the provider or the consumer can create a packaged clean room. The steps are the same as for an approval-based clean room, except that you select the packaged clean room type and designate the package provider.

1. In your Databricks workspace, click  **Catalog**.
2. In the upper-right side, click **Share** > **Clean Rooms**.
3. Click **Create Clean Room**.
4. Under **Clean room type**, select **Packaged Clean Room**.
5. Enter a **Clean Room name** and select the **Region** for the central clean room.
6. Under **Collaborator details**, enter the **Clean Room sharing identifier** for the other collaborator, then click **Add collaborator**.
7. For **Designated Clean Room package provider**, select **You** or **Invited collaborator** to choose which collaborator is the package provider. The package provider's assets are hidden from the other collaborator.
8. Click **Create clean room**.

Packaged mode is set when the clean room is created and cannot be changed afterward.

## Provider tasks

As the provider, you supply the notebooks, JARs, and data, and you can monitor the runs that the consumer triggers.

* **Add notebooks, JARs, and data assets**: Add your assets the same way you would in an approval-based clean room. See [Step 3. Add data assets and notebooks to the clean room](/aws/en/clean-rooms/create-clean-room#add-assets). Your assets are visible only to you, and you cannot see the consumer's data assets.
* **Monitor run history**: The consumer triggers runs that use your notebooks and JARs. You can see the consumer's runs in the run history, but you cannot view the run output. See [Monitor clean room notebook runs](/aws/en/clean-rooms/manage-clean-room#view-runs).

## Consumer tasks

As the consumer, you contribute your own data, trigger runs against the provider's code, and view the results.

* **Open the packaged clean room**: You see the names of the provider's notebooks and JARs, but not their source code.
* **Add your data assets**: Click **Add Input Data** to add your tables, volumes, or models to the clean room. Your data is visible only to you, and the provider cannot see it.
* **Trigger a run**: The provider's code runs in the clean room's secure environment with access to the data assets that both collaborators contributed.
* **View the run output**: You can view the output of the run. To make results available to others, the provider's code can also write to a shared output schema that all collaborators can read. See [Create and work with output tables in Databricks Clean Rooms](/aws/en/clean-rooms/output-tables).

## Limitations

* Packaged mode is set at clean room creation and cannot be disabled afterward.
* Auto-approval rules are disabled for all collaborators, including the provider.