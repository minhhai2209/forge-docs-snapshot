# Data lifecycle for Forge-hosted storage

This document outlines the Forge-hosted [Persistent](/platform/forge/runtime-reference/storage-api/#persistent) storage data lifecycle for apps. It focuses on data managed through Forge-hosted storage and explains how data is provisioned, retained, and deleted at different stages of the app lifecycle. Understanding these stages helps you effectively plan your app's behavior and ensures it meets data handling requirements.

This guide only discusses Forge-hosted Persistent storage and doesn't include remote or other types of storage. While this guide details how Atlassian manages Forge-hosted data, you may find these practices useful for managing remote storage as well to ensure consistency and effective data handling.

## Data storage during App lifecycle stages

Each stage affects how data is managed and stored by Atlassian. Below is an overview of each stage and how it affects data.

| Stage | Data status |
| --- | --- |
| Creation / Deployment | When a developer creates or deploys an app, no storage is set up at these stages. The system defines the app and makes it ready for use, but it does not create or store any data until a customer installs it on a site. |
| Installation | When a customer installs the app, the system provisions storage in the site's Atlassian app partition to manage the app's data for that specific site. |
| Upgrade | If new features require storage, the system provisions additional storage in the site’s Atlassian app partition during an app upgrade to meet new storage needs without affecting existing site data. |
| Uninstallation | When a customer uninstalls the app, they will either retain access for 60 days following the end of the billing or trial period, or remove the app immediately, forfeiting any remaining time. |
| Deletion | To delete an app, customers or Atlassian support must first uninstall all installations. The system then deletes data, following the same uninstallation retention period as described above. |

## Data retention and deletion events

How data is stored or deleted depends on what happens to the app. Forge follows Atlassian's internal Standard Data Retention and Disposal policy. You can find more information in the [Atlassian SOC 2 report](https://www.atlassian.com/trust/compliance/resources/soc2). Below are the key actions that affect data retention or deletion:

### App uninstallation

When an app is uninstalled, the data is first 'soft deleted' and then retained for the rest of the retention period as outlined in the Atlassian SOC 2 report.

### App reinstallation

If an app is reinstalled, it is treated as a new installation. However, if a request is made within 21 days of uninstallation, the new installation can be relinked to the old data. For more details on the process, refer to [Data recovery for apps with hosted storage](/platform/forge/runtime-reference/storage-api/#data-recovery-for-apps-with-hosted-storage).

### App deletion

Before an [app is deleted](/platform/forge/manage-your-apps/#delete-forge-apps), all installations must be removed first. Partners need to ask customers or contact Atlassian support to uninstall the app so the data can be deleted. Given these are normal uninstallations, they will fall under the same retention period as described above.

## Licensing changes and Atlassian app impacts

Changes in app licenses or Atlassian app cancellations can also affect how data is managed. Below is how different licensing events impact data.

### App licensing changes

* **Active license:**
  * After a paid app is canceled, the customer can uninstall the app.
  * When an Atlassian app with installed apps is canceled, the system will also cancel the app subscriptions.
  * The system keeps the app data according to Atlassian's data retention policy after the customer uninstalls it.
* **License suspension or deactivation:** If an app's license is suspended or deactivated, the app becomes inactive, but the system keeps all the stored data without changes. The data remains unchanged while the app is inactive. A license suspension usually happens when a customer misses a payment, such as after the grace period for payment recovery. Once the payment is resolved, the license is reactivated, and the app regains access to the existing data.

### Atlassian app deletion

For more information on what happens when a subscription is canceled, see [Cancel a subscription](https://support.atlassian.com/subscriptions-and-billing/docs/cancel-a-subscription/).

* **Jira & Confluence:** The system schedules data for deletion after the Atlassian app is deleted, following Atlassian's data retention policy.
* **Compass:** The system schedules data for deletion after the Atlassian app is deleted, following Atlassian's data retention policy.
* **Bitbucket:** The system deletes the data after the Atlassian app is deleted, according to Atlassian's data retention policy.

### Site suspension, deactivation, and deletion

The system handles site suspension, deactivation, and deletion based on Atlassian's data retention policies. This affects all apps installed on the site.

* When a site is deleted, it undergoes a soft delete during which the site and app data remain recoverable. However, once the site is permanently removed after the soft delete period, all associated app data is also deleted immediately.
