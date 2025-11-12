# Manage your apps

You can securely manage all your Forge apps, [Cloud Fortified Connect apps](/platform/marketplace/cloud-fortified-apps-program/)
and [OAuth 2.0 (3LO) integrations](/cloud/jira/platform/oauth-2-3lo-apps/)
in one place using the Atlassian [developer console](/console/myapps/).

## View your apps

The developer console lets you view information about your apps and integrations,
including their scopes and environments.

To access the console:

1. From any page on [developer.atlassian.com](https://developer.atlassian.com/), select your profile icon
   in the top-right corner.
2. From the dropdown, select **Developer console**.

Your apps and integrations are listed with the following details:

* **App name**: the name of your app, which can be changed in **Settings**
* **Distribution status**: whether or not you've [enabled sharing for your app](/platform/forge/distribute-your-apps/)
* **Updated on**: the time and date you created your app or updated its settings
* **Type**: the platform or framework used to build your app. To learn more about your options
  for building an app, see the [Cloud development platform overview](/developer-guide/cloud-development-platform-overview/).

For Jira apps, the app name **isn't** the name displayed to users in the Jira issue.
To change the name that appears in the Jira issue, you need to update the title in the
manifest.

Your apps and integrations are listed in the order that they were last updated.
You can search for an app using the search bar above the app table.

## View Forge app details

Select a Forge app on the **My apps** screen to get more information about it, including app ID,
environments, and permissions.

The **Overview** page displays the following panels:

* **App details**
  * **App ID**: The identifier for the selected Forge app.
  * **App environments**: The three available [environments](/platform/forge/environments-and-versions/)
    for the app. The **Environments** page of the developer console lists the available environments
    of each app and their corresponding IDs.
  * **Currently deployed to**: Which of the three environments the app is currently deployed to.
  * **Compatible with**: The Atlassian apps the Forge app is supports, as declared in the manifest.
* **Monitoring**
  * **Number of installations**: How many sites the app is currently installed on.
  * **Log summary**: How many sites are currently sharing their logs with you.
* **Contributors**
  * **Your role**: Your role as a contributor for the selected Forge app. See
    [Roles and permissions](/platform/forge/contributors/#roles-and-permissions) for more details.
  * **App owner**: The owner of the app you're contributing to.
  * **Total contributors**: The total number of contributors for the app.
* **Permissions**
  * **API scopes**: the API scopes currently included in the Forge app’s manifest file. See
    [View Forge app permissions](#view-forge-app-permissions) below for more information.
* **Distribution**

## View Forge app permissions

You can view the level of access your Forge app has to an Atlassian user’s account by
selecting **Permissions** in the left menu, or selecting the **Permissions** panel.

The **Permissions** page lists the APIs included in your Forge app, where you have added at
least one scope from that API to your app's manifest file. For the APIs and scopes to display on the
**Permissions** page, you'll need to deploy your app to the *production* environment.
See [Environments and versions](/platform/forge/environments-and-versions) for more details.

To see the individual scopes for an API, select **View**.

To learn more about Forge app permissions, see
[Security](/platform/forge/security/#simple-and-secure-authentication).
For more information about individual scopes, see
[Permissions](/platform/forge/manifest-reference/permissions/).

## Create and edit Forge apps

Any new Forge apps you create using the CLI appear in the console, and any
changes you make to existing Forge apps using the CLI are reflected in the
console.

## Delete Forge apps

The process of deleting Forge apps varies, depending on whether you've
[listed your app](/platform/marketplace/listing-forge-apps/) on the Atlassian Marketplace or you've
[distributed your app](/platform/forge/distribute-your-apps/) via the developer console.

### Delete a Forge app listing on the Marketplace

By listing a Forge app on the Atlassian Marketplace, the app effectively becomes one of the following:

* a **paid via Atlassian** app, if you listed it as a paid app
* a **free** app, if you listed it as a free app

To delete a **paid via Atlassian** Forge app, see the
[Paid via Atlassian cloud apps only](/platform/marketplace/knowledge-base/retiring-your-app/#paid-via-atlassian-cloud-apps-only)
documentation. To delete a **free** Forge app, see the
[Free apps](/platform/marketplace/knowledge-base/retiring-your-app/#free-apps) documentation.

For both *paid via Atlassian* and *free* apps, there are end-of-life (EOL) terms to consider when
deleting the app from the Marketplace. The EOL terms only apply to apps with active customers.
See [Manual retiring of apps](/platform/marketplace/knowledge-base/retiring-your-app/#manual-retiring-of-apps)
for more details.

### Delete a Forge app distributed via the developer console

You can delete the app via the console if the app is not installed on a site.

1. Access the [developer console](/console/myapps/).
2. Select the app that you want to delete.
3. Go to **Settings** in the left menu, and select **Delete app**.

If the app is currently installed on a site, do one of the following:

* Uninstall the app from all the sites it's installed on, then delete the app from the console.
* Submit a ticket at [Developer and Marketplace support](https://developer.atlassian.com/support), and the Atlassian team will uninstall and delete the app for you.

If you created Forge apps using Atlassian accounts based on aliases of the same email, then the
list of apps for each account is treated independently. This means you need to uninstall the
apps from each account individually.

For example, if you have an Atlassian account associated with *[simon@example.com](mailto:simon@example.com)*, you can create
separate Atlassian accounts based on aliases of the account, such as *[si.mon@example.com](mailto:si.mon@example.com)* and
*[simon+app@example.com](mailto:simon+app@example.com)*. If you signed up for Forge and created apps on all of these accounts, you
need to uninstall the apps for each individual account.

## Download audit logs

App admins can download audit logs for apps that use
[Forge-hosted storage](/platform/forge/storage/#forge-hosted-storage). Audit logs contain details
of audit events related to changes made in the storage location of app data.

Unlike app logs, which record events related to the app's operation and performance, audit logs are
used for security and compliance purposes. They serve as supporting evidence for audits,
demonstrating that the movement of app data was conducted in accordance with customer requests
through Atlassian's Data Residency controls.

### Availability of audit logs

Audit logs are available for download for a duration of two years. After this period, the logs are
permanently deleted from the database and are no longer included in the downloadable CSV file.

When an app is uninstalled from a tenant, audit logs are available for 30 days. After 30 days, the
related logs are erased from the database and can no longer be downloaded.

When an app is uninstalled from a tenant, audit logs remain available for download for 30 days.
Since you as partner don’t know when an app is uninstalled from a tenant, we recommend downloading
audit logs at a regular cadence to capture logs from uninstalled apps.

### Data migration events captured by audit logs

#### Admin-initiated data migration of site and Atlassian app locations

When a customer site admin moves their Jira or Confluence data to a location, that app's status
will then appear as `PINNED`. For any Forge apps installed on that Atlassian app, all Forge app data within the
hosted storage is also moved to that same `PINNED` location as the host Atlassian app.

Audit logs capture these data migration events, including when a migration has been scheduled,
started, completed, or failed. See [Data Residency](/platform/forge/data-residency/) and
[Move Atlassian app data to a different location](https://support.atlassian.com/security-and-access-policies/docs/move-data-to-another-location/)
for more information.

#### App installation or uninstallation from a tenant

Audit logs capture app installation and uninstallation events within a tenant.

#### Atlassian scheduled Forge backfill operation

On March 28, 2024, Atlassian triggered a migration event for data residency for all Forge apps using
hosted storage. For any apps deployed before this date, audit logs will include two entries for
those events, `Forge backfill started` and `Forge backfill completed`. See the
[changelog](/platform/forge/changelog/#CHANGE-1556/) for more details.

The following fields show the event metadata captured in audit logs:

| Field | Description | Examples |
| --- | --- | --- |
| App ID | The unique identifier of the Forge app. | `83ba0476-7067-4011-9a80-0a132d9ff63a` |
| App name | The name of the Forge app. | `spam-log` |
| Site ID | The unique identifier of the site. | `87f02c6d-d051-4671-9338-612c4460f2fb` |
| Atlassian app | The name of the Atlassian app associated with the app. | `Confluence` |
| Environment | The environment of the Forge app. | `Production` |
| Installed version | The installed version of the Forge app. | `3.1.0` |
| Event | The status of a migration event or app lifecycle event. | * `Migration scheduled` * `Migration completed` * `App uninstalled` |
| Event date | The date when the event takes place. | `2024-03-12` |
| Location | The current location of the site's data. | `Global` |
| Target location | The intended location for the migration event. This field is marked as `N/A` during lifecycle events, which are app installation and app uninstallation. | `US` |

### Access audit logs from the developer console

Only app admins have permission to download audit logs.

You can download audit logs via the console:

1. Access the [developer console](/console/myapps/).
2. Select the app for which you want to download audit logs.
3. Go to **Settings** in the side navigation panel.
4. In the **Audit logs** section, select **Download**.
5. Select the date range of the audit logs you would like to download. Only audit logs within the
   last two years can be downloaded.
6. Select **Download**. A CSV file containing the audit logs will be downloaded to your device.

If you encounter an error when trying to download audit logs, check that your app is using hosted
storage, or try a different date range. Remember, you can only download audit logs for apps that use
hosted storage within the last two years.

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
