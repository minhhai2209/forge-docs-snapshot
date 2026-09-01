# Atlassian Government Cloud for Forge developers

The Atlassian Government Cloud (AGC) is a dedicated cloud environment designed to meet the security, compliance, and operational needs of United States government agencies and their contractors. AGC is FedRAMP Moderate authorized and operates with enhanced controls, continuous monitoring, and a completely separate perimeter from Atlassian's commercial cloud.

Marketplace apps are a critical part of the AGC experience. To reach AGC customers, you must explicitly enable your app for AGC — it is not available there by default.

## Who can access AGC

AGC is available only to US government agencies and contractors or vendors working with the US government. Each AGC product also has a minimum user count:

* Jira: 201 users
* Confluence: 201 users
* Jira Service Management: 26 users

## AGC requirements

* **Explicit opt-in required:** Your app is not automatically available to AGC customers. You must go through the AGC enablement process.
* **App type requirements:** Apps must be registered as Forge or Connect-on-Forge apps. Connect apps that have not adopted Forge are not eligible.
* **Developer license required:** You must receive a developer license from the AGC provisioning team before you can build and test against AGC.
* **FedRAMP authorization not required:** Your app does not need to be FedRAMP Moderate authorized to operate in AGC. However, individual AGC customers may require you to authorize your app as an external service as part of their own risk management process.
* **App installation in production:** At present, only Atlassian support teams can install apps for AGC customers in production. Apps are not self-installable by AGC customers. See [Manage Marketplace apps for Atlassian Government apps](https://support.atlassian.com/organization-administration/docs/manage-marketplace-apps-for-atlassian-government-apps/) for details.

## AGC limitations for Forge features

The following Forge features are not supported for AGC apps:

Everything else in Forge is supported on AGC unless stated otherwise in the specific feature's documentation.

## Full AGC developer documentation

For complete guidance on building, testing, and publishing apps for AGC — including app compatibility requirements, OAuth 2.0 on AGC, and the publishing process — see the [Atlassian Government Cloud developer portal](/platform/framework/agc/).
