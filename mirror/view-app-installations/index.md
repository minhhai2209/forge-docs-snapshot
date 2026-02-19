# View app installations

You can view the sites onto which your app is installed. This helps you see the following details
about your app:

* the total number of current installations of your app
* a breakdown of **Atlassian apps**, **versions**, **licenses**, **editions**, and **environments** that your app is installed on
* whether admins have enabled data egress for the [purpose of analytics](/platform/forge/manifest-reference/permissions/#external-permissions)

## View app installations

To view app installations:

1. Access the [developer console](/console/myapps).
2. In the left menu, select **Installations**.

The screen shows a list of all the sites and Atlassian apps that your app is currently connected to.

![A list of sites the app is installed onto](https://dac-static.atlassian.com/platform/forge/images/installation-screen.svg?_v=1.5800.1863)

You can sort the sites by **version** or **installation date** in ascending or descending order
by clicking on the corresponding column header.

## Search for installations

You can search for a specific installation of the app by entering the **site** in the search box.

You can also use filters to further refine the list of sites. You can filter by **version**,
**environment**, **Atlassian app**, **license**, or **edition**.

## Check access to analytics

For each site that your app is installed on, you can check whether or not admins have enabled
the sending of data to domains that you've declared for the
[purpose of analytics](/platform/forge/manifest-reference/permissions/#external-permissions).

While egress permissions can be categorized as analytics,
[app admins](https://support.atlassian.com/organization-administration/docs/installing-and-managing-app-access/#Manage-access-to-analytics-and-logs-for-all-apps)
can still choose to disable access to analytics. You must ensure that your app can efficiently
handle the scenario when analytics access is disabled. Otherwise, this may lead to poor user experience,
in the form of failing app invocations or elements not rendering properly in the UI, and more.

## View app logs

You can view app logs associated with a specific site. This is handy for troubleshooting issues
occurring on that site.

Click the **Logs** link for the site you want to view. This takes you to the Logs screen, where
the logs are already filtered by the corresponding **environment**, **time range**, **site**, **license**, and **edition**.

You can do further log operations on this screen. See [View app logs](/platform/forge/view-app-logs/)
for more details.
