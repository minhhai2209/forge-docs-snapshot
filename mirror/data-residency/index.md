# Data residency

To help partners more easily meet customer data residency needs, we have enabled data residency
support for apps that use
[persistent Forge hosted storage](/platform/forge/runtime-reference/storage-api/#persistent)
, as well as allowing realm pinning for apps for apps that use [Forge Remote](/platform/forge/remote/).

For apps that use persistent Forge hosted storage, Forge will take care of the hosting, pinning, and migration of hosted data between supported
locations, so partners can focus on building a high quality app for their customers.

This solution is designed to work harmoniously with Atlassian app data residency and consequently is
based on similar concepts and terminology.

For more information about how the Atlassian cloud addresses the data residency needs of organizations, see [Manage data residency](https://support.atlassian.com/security-and-access-policies/docs/manage-data-residency-for-products/)

## How it works

Jira and Confluence users on the Atlassian cloud
[can *move* their data to any supported location](https://support.atlassian.com/security-and-access-policies/docs/move-data-to-another-location/).
When this occurs, the Atlassian cloud infrastructure will migrate the customer's Atlassian app data
to that location.

In line with this, we have enabled data residency support for apps that choose to use persistent Forge hosted storage. Since Forge uses a similar cloud infrastructure for its hosted storage, partners that
choose to store their app’s data on persistent Forge hosted storage will enable Forge to move that data to an admin’s chosen location.

This means that the data from both Atlassian app and all Forge apps using persistent Forge hosted storage will be hosted in the admin's chosen location. As a result:

* If an admin installs an Forge app using persistent Forge hosted storage on an Atlassian app that's pinned to a location, the app will automatically be located there too.
* If an admin migrates the data of a pinned Atlassian app to a different location, then all installed,
  Forge apps using persistent Forge hosted storage will also be migrated there as well.

In addition, Forge supports remote data residency. This allows you to pin remote endpoints to specific geographic regions, ensuring compliance with data residency requirements for data processed or stored outside of persistent Forge hosted storage. By defining region-specific `baseUrl` values, you can align your apps with customer data residency needs.

Apps that are [eligible](#eligibility) will be shown with a `PINNED` status to the admin.

Forge will aim to execute its invocations from the same location as the host Atlassian app. See [Multi-region compute](#multi-region-compute) for more details.

## Eligibility

A Forge app is eligible for `PINNED` status under any of the following conditions:

1. **All in-scope End-User Data is stored exclusively in persistent Forge hosted storage:** If your app uses only persistent Forge hosted storage for all in-scope End-User Data, it qualifies for `PINNED` status without additional configuration.
2. **The app stores in-scope End-User Data remotely but uses Forge Remote data residency with region-specific URLs:** Apps can maintain eligibility for `PINNED` status if they store in-scope End-User Data in a remote backend configured with region-pinned URLs. This requires setting up the manifest file with region-specific `baseUrl` values and marking them with `inScopeEUD: true` to meet data residency requirements. For information on how to do this, see [​Remotes](/platform/forge/manifest-reference/remotes/#data-residency).
3. **The app uses a remote backend but does not store in-scope End-User Data there:** f your app interacts with remote backends solely for operations that do not involve storing in-scope End-User Data, it can be eligible for `PINNED` status. To ensure compliance, you must configure your manifest file appropriately. For information on how to do this, see [​Remotes](/platform/forge/manifest-reference/remotes/#data-residency).

By default, Forge assumes an app stores in-scope End-User Data remotely if its manifest file includes:

In addition, when an admin initiates moving their Jira or Confluence instance to a location, they'll see which apps can move at the same time. These may include Forge apps that are eligible for `PINNED` status which may move at the same time as the Atlassian app.

![Eligible apps moving with the Atlassian app](https://dac-static.atlassian.com/platform/forge/images/dare-apps-list.png?_v=1.5800.1849)

## In-scope End-User Data

Forge developers will be responsible for defining, documenting, and communicating with their
customers what data is in-scope and out-of-scope for data residency for their Forge app (see Atlassian’s
[in-scope data](https://support.atlassian.com/security-and-access-policies/docs/understand-data-residency/)
as an example). Admins use this list of information to understand an app’s suitability and compliance with relevant data residency regulations.

You’ll need to publish what data your app considers in-scope and out-of-scope for data residency in your own documentation.

## Marketplace listing

You can leverage the Atlassian Marketplace to advertise the app’s support for data residency (specifically, its eligibility for `PINNED` status).

You can do this through your app’s Atlassian Marketplace listing. Specifically, when providing your app’s Privacy and Security information, respond accordingly to the following questions:

| Questions | Correct option |
| --- | --- |
| Does your app support data residency options? | Yes. App supports data residency   *(You must fill out the details based on your app)* |
| Does your app support migration of in-scope End User Data between your data residency supported locations? | Yes.   *(If your app is not using Forge Remote for storing in-scope End User Data)* |

Upon updating this information, it will be available on your app’s **Privacy and Security** tab. For
more information, see
[Privacy and Security tab in your Marketplace listing](/platform/marketplace/security-privacy-tab/).

## PINNED Atlassian app location

When an admin moves their Jira or Confluence data to a location, the status of the Atlassian app
will then appear as `PINNED` in the admin’s **Data residency** interface:

![Atlassian app pinned to Europe](https://dac-static.atlassian.com/platform/forge/images/dare-pinned-product.png?_v=1.5800.1849)

The `PINNED` Atlassian app status lets admins verify that their Atlassian app's in-scope data is
hosted on the chosen location. You can learn more about how admins pin their Atlassian app data in ​
[Move product data to another location](https://support.atlassian.com/security-and-access-policies/docs/move-data-to-another-location/).

In-scope Atlassian app data refers to all data stored by an Atlassian app that can be pinned. See
[Understand data residency](https://support.atlassian.com/security-and-access-policies/docs/understand-data-residency/#In-scope-product-data) for more information.

## PINNED app location

After an admin verifies that their Atlassian app data is pinned to a location, they also need to verify
that all in-scope end-user data for an app is also pinned. Apps pinned to the same location as the Atlassian app will be
displayed as `PINNED` in the admin's **Data residency** interface:

![App pinned to same location as Atlassian app](https://dac-static.atlassian.com/platform/forge/images/dare-pinned-app.png?_v=1.5800.1849)

The `PINNED` app status provides admins with the verification that an app's data is hosted in the
same location as the Atlassian app.

When an admin installs an eligible Forge app on an Atlassian app that is already `PINNED`, the app will
automatically be displayed as `PINNED` as well.

## Supported locations

Admins can pin their Atlassian app data and hosted Forge app data to a number of supported locations, namely:

| Location | AWS regions |
| --- | --- |
| Global | In-scope data is hosted within realms determined by Atlassian: data may be moved between realms as needed. |
| Australia | In-scope data is hosted within the Australia (Sydney) region. |
| Canada | In-scope data is hosted within the Canada (Central) region. |
| EU | In-scope data is hosted within the Europe (Frankfurt) and Europe (Dublin) regions. |
| Germany | In-scope data is hosted within the Europe (Frankfurt) region. |
| India | In-scope data is hosted within the Asia Pacific (Mumbai) regions.  **Note**: India is not assigned as the default data residency location, even for organizations based in India. You can manually set data residency to India through the Atlassian Administration interface. |
| Japan | In-scope data is hosted within the Asia Pacific (Tokyo) region. |
| Singapore | In-scope data is hosted within the Asia Pacific (Singapore) region. |
| South Korea | In-scope data is hosted within the Asia Pacific (Seoul) region. |
| Switzerland | In-scope data is hosted within the Europe (Zurich) region. |
| United Kingdom | In-scope data is hosted within the Europe (London) region. |
| USA | In-scope data is hosted within the US East (North Virginia) and US West (Oregon) regions. |

Data residency for persistent Forge hosted storage will automatically include any
*new* location that the Atlassian cloud infrastructure supports.

## Multi-region compute

Forge will aim to execute its invocations from the same location as the host Atlassian app. This helps Forge optimize for an app's reliability and performance (as well as facilitate security and fraud prevention).

To support some Atlassian cloud capabilities and maintain overall reliability, Forge may sometimes execute an app's invocation from a location other than the location where the host Atlassian app is.

## Observability

Tracking, logging, and auditing is an integral part of supporting data residency.
The Developer Console provides [audit log features](/platform/forge/manage-your-apps/#audit-logs) that will allow you to do this;
these features provide records for related events (such as when an admin pins their Atlassian app and Forge app to a location).
