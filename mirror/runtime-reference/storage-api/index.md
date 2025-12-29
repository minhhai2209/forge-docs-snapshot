# Storage overview

Forge provides hosted storage capabilities that let you persistently store data in your app installation. Each installation of your app is subject to the quotas and limits of Forge's hosted storage capabilities. See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and [Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for more details.

## Hosted storage capabilities

Use this for long-term storage until you need to delete or overwrite the data. Forge provides the following persistent storage capabilities:

* [Key-value store](/platform/forge/runtime-reference/storage-api-basic/): lets you store data in key-value pairs.
* [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/): lets you store data based on [custom data structures](/platform/forge/runtime-reference/custom-entities/) specific to your app's needs and query patterns.
* [Forge SQL](/platform/forge/storage-reference/sql/): lets you provision dedicated SQL database instances for each customer installation. You can then use these instances to store interrelated and complex datasets as required by your app.
* [Object Store (EAP)](/platform/forge/storage-reference/object-store/): lets you store and manage large items such as substantial data objects or media files. This feature is currently available as part of Forge's Early Access Program (EAP).

These capabilities [encrypt](https://www.atlassian.com/trust/security/security-practices#key-management) and store data on disk, optimising them for durability and persistence at the expense of performance.

## Data recovery for apps with hosted storage

Forge hosted storage retains data for 28 days after uninstallation. However, when a customer reinstalls an app that uses Forge hosted storage, data
from the previous installation is not automatically restored.

To recover this data for a customer, app developers must:

* Get customer consent to restore data.
* Submit a recovery request within 21 days of uninstallation. This is to ensure the request is processed before the 28-day retention ends.

To submit a recovery request:

1. Raise a bug ticket on [Developer and Marketplace Support](https://ecosystem.atlassian.net/servicedesk/customer/portal/34/group/3534/create/4180).
2. Write **Re-link data to reinstalled app** in the summary.
3. Add the following customer details to the **Description**:
   * **Site ID**: of the site where the app is currently installed
   * **Installation ID**: the current app installation where the existing data should be re-linked

We will then re-link the data from their *previous* installation (also identified by Installation ID) to the current installation.

If the customer uninstalled and reinstalled their app multiple times, you may need to specify which installation's data we should re-link.
In this case, you can ask the customer to identify this installation by the date it was uninstalled.

See [Data lifecycle for Forge-hosted storage](/platform/forge/storage-reference/hosted-storage-data-lifecycle/) for related details.
