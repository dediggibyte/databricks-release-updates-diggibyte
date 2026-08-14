Databricks recipients use their existing OpenSharing setup to access shares from a provider who has enabled OpenSharing SecureConnect.

If your provider has enabled SecureConnect and you have an egress firewall, you must allow outbound connections to Databricks IP addresses to access SecureConnect. Allowlist the IP addresses for the provider's cloud and region, regardless of the cloud you are on.

important

Databricks recipients on classic compute and open recipients must allow outbound connections to Databricks IP addresses in their egress firewall. SecureConnect does not initiate inbound connections to the recipient's network.

Databricks recipients on serverless compute do not need to configure their egress firewall to access SecureConnect. Databricks routes serverless traffic to SecureConnect internally.

For an overview of SecureConnect and provider-side setup, see [Share data behind a firewall with SecureConnect](/aws/en/opensharing/secureconnect-provider).

## Allowlist Databricks IPs in your egress firewall

Select the cloud your provider is on, then add the listed Databricks IP addresses to your egress firewall's outbound allowlist for the provider's region.

* AWS
* Azure
* GCP

For an AWS provider, allowlist the Databricks IP addresses for "Default storage, OpenSharing SecureConnect, Zerobus Ingestion, and Lakebase (Autoscaling Beta)" corresponding to the provider's region.

See [IP addresses and domains for Databricks services and assets](/aws/en/resources/ip-domain-region).

For an Azure provider, allowlist the Databricks IP addresses for "Control Plane IPs, including default storage and webapp" corresponding to the provider's region.

See [IP addresses and domains for Databricks services and assets](/aws/en/resources/ip-domain-region).

For a GCP provider, allowlist the Databricks IP addresses for "Control Plane services, including default storage and webapp" for the provider's region. See [IP addresses and domains for Databricks services and assets](/aws/en/resources/ip-domain-region).

## Billing

Databricks is expanding SecureConnect networking billing to include charges for recipients accessing shared data across regions or clouds. To understand how you might be billed, see [Expanded networking billing for OpenSharing SecureConnect](/aws/en/release-notes/whats-coming#secureconnect-billing).

## Limitations

The following limitations apply to Databricks recipients accessing SecureConnect-enabled shares:

* mTLS is not enabled for recipients using classic compute.
* mTLS is not enabled for OIDC recipients.
* Serverless Databricks recipients using a Databricks-to-Open credential in the same region as the provider are not supported.

* If you use serverless compute to read shares from providers in the same region as you, you can connect to at most five providers that use SecureConnect with private connectivity (a network connectivity configuration, or NCC).