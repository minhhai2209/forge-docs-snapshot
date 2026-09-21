# View app installations

You can view the sites onto which your app is installed. This helps you see the following details
about your app:

* the total number of current installations of your app
* a breakdown of **Atlassian apps**, **versions**, **licenses**, **editions**, and **environments** that your app is installed on
* whether admins have enabled logs, custom metrics, and data egress for the [purpose of analytics](/platform/forge/manifest-reference/permissions/#external-permissions)

## View app installations

To view app installations:

1. Access the [developer console](/console/myapps).
2. In the left menu, select **Installations**.

The screen shows a list of all the sites and Atlassian apps that your app is currently connected to.

![The Installations page showing filters, a table of app installations, and pagination controls](https://dac-static.atlassian.com/platform/forge/images/installation-screen.png?_v=1.5800.2336)

You can sort the sites by **site name**, **version**, or **installation date** in ascending or descending order
by selecting the corresponding column header.

## Customize the table

You can configure the table to show the information most relevant to you. Show or hide columns,
move them left or right, and pin a column to the left. You can restore the default table configuration
by resetting your selection.

## Search for specific installations

You can use filters to refine the list of sites. You can filter by:

* **Site**, **environment**, **Atlassian app**, **version**, **license**, **edition**, and **status**.
* **Installed on**, including a custom date range.
* Whether **logs access**, **analytics access**, and **custom metrics access** are enabled or disabled.

The page shows the number of installations that match your filters above the table. You can choose to
show 10, 20, 30, 40, or 50 installations per page.

## Check access to analytics

For each site that your app is installed on, you can check whether or not admins have enabled
the sending of data to domains that you've declared for the
[purpose of analytics](/platform/forge/manifest-reference/permissions/#external-permissions).

While egress permissions can be categorized as analytics,
[app admins](https://support.atlassian.com/organization-administration/docs/installing-and-managing-app-access/#Manage-access-to-analytics-and-logs-for-all-apps)
can still choose to disable access to analytics. You must ensure that your app can efficiently
handle the scenario when analytics access is disabled. Otherwise, this may lead to poor user experience,
in the form of failing app invocations or elements not rendering properly in the UI, and more.

## Check access to custom metrics

For each site that your app is installed on, you can check whether or not admins have enabled custom metrics ingestion. See [custom metrics](/platform/forge/monitor-custom-metrics) for more details.

## Copy a site ARI

From the **Actions** menu for an installation, select **Copy site ARI** to copy the installation context
ARI. You can use this value as the `installationContext` when you [export app logs](/platform/forge/export-app-logs/).

## View installation permissions

From the **Actions** menu for an installation, select **View permissions**. The Installation permissions
page shows the app version, the requested scopes and egress permissions, and the status of each permission.

## View app logs

You can view app logs associated with a specific site. This is handy for troubleshooting issues
occurring on that site.

From the **Actions** menu for the site you want to investigate, select **View logs**. This takes you to
the Logs screen, where the logs are already filtered by the corresponding **environment**, **time range**,
**site**, **license**, and **edition**.

You can do further log operations on this screen. See [View app logs](/platform/forge/view-app-logs/)
for more details.

## Download installation details

Select **Download installations** to generate a CSV file containing all installation details for your app.
After a file has been generated, select **Download** to retrieve the previously generated file immediately.
The file shows the date and time through which its data is current.

To generate a new file with the latest installation data, select the **More download options** menu and then
**Download Latest**. Generating a new file can take 15 to 20 minutes. Select **Refresh** while the file is
being generated to check whether it is ready to download.
