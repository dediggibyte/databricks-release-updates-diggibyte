Beta

This feature is in [Beta](/aws/en/release-notes/release-types). Account admins can manage access to this feature from the account console **Previews** page. See  [Manage account-level previews](/aws/en/admin/workspace-settings/manage-previews#account).

Databricks can pull in metadata from external knowledge sources, such as BI tools, so your teams can use the semantic models, measures, and calculated columns that they already report on without re-creating them in Databricks. Genie can use the measure definitions from your BI tools when it answers questions.

Genie Ontology combines modeled context, which you define and govern with Unity Catalog semantics, with inferred context that Genie extracts from your assets. Metadata that Databricks pulls in from external knowledge sources adds to the inferred context, so you don't have to re-create those semantics. Genie turns the measures, calculated columns, and relationships in these definitions into [Ontology Snippets](/aws/en/genie/genie-ontology).

## Turn external knowledge on or off

An account admin turns on the **External knowledge** preview from the account console. Turning off the preview stops serving Ontology Snippets in all workspaces in the account. See  [Manage account-level previews](/aws/en/admin/workspace-settings/manage-previews#account).

## Supported external knowledge sources

* [Power BI](/aws/en/genie/genie-ontology/external-knowledge-sources/power-bi): Pull in metadata from Power BI semantic models through a Unity Catalog connection. The connection must be used by a Power BI task in a job.

## Additional resources

* [Genie Ontology](/aws/en/genie/genie-ontology)