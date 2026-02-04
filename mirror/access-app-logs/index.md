# Access app logs

To help you troubleshoot faster, app log sharing is now enabled automatically during
installation. This means that when a user installs your app on their site, you will now
automatically get access to the app logs for that site.

Once you’ve [shared your Forge app](/platform/forge/distribute-your-apps/#start-sharing-your-app) or
[listed it on the Atlassian Marketplace](platform/forge/distribute-your-apps/#listing-forge-apps-on-the-atlassian-marketplace),
users may experience issues using it on their Atlassian site. To help you
[fix the issue](/platform/forge/debugging/), you can access the logs for your app
installed on their site. Log access is automatically granted when a user installs your
app. You can [view these logs](/platform/forge/view-app-logs-and-installations/) in the [developer console](/console/myapps/).

However, a user may disable log access to their site, which means their logs will no
longer appear in the developer console. If your user is experiencing a problem with your
app, and you can’t resolve it by analyzing the logs that you currently have access to,
you’ll need to ask the user to re-enable access to the logs, or download the logs and send
them to you.

To find the user’s email address, follow the steps on
[how to contact your customer](/platform/marketplace/sales-and-evaluations-reports/#how-do-i-contact-a-customer-).
You must collect and use data in accordance with the privacy
rights that you've obtained from your user. For more information, see the
[Atlassian Developer Terms](/platform/marketplace/atlassian-developer-terms/)
and [Forge Terms](/platform/forge/developer-terms/).

This is only available for paid Atlassian apps.

## Re-enable log access

If your user is experiencing problems with your app, but has disabled log access for
their site, you might need them to re-enable log access.

Either tell them to follow the same method that they used for
[managing log access](https://support.atlassian.com/organization-administration/docs/managing-an-installed-app/#Manage-access-to-logs), or give them the following instructions:

1. Go to [admin.atlassian.com](https://admin.atlassian.com/).
2. Select the relevant **site**.
3. Select **Apps** in the global navigation.
4. In the **Sites** section of the lefthand navigation, select the **site** you're administering apps for.
5. In the lefthand navigation, select **Connected apps**.
6. Select the action button for the app you want to enable logs for.
7. In the **Details** tab, under **Logs access**, enable the setting.

   Your user sees a screen like this, showing the details of your app and the controls for
   enabling or disabling access to their site's logs.

   ![The admin hub app details page, showing details, and the section to enable logs](https://dac-static.atlassian.com/platform/forge/images/admin-hub-access-prod-logs-section.png?_v=1.5800.1816)

Once your user has enabled access, you'll be able to see their logs and
[monitor your app on their site](/platform/forge/monitor-your-apps) in the
[developer console](/console/myapps/).

## Download logs

If you need your users to download and send their app logs, direct them to the
[Manage an installed app](https://support.atlassian.com/organization-administration/docs/managing-an-installed-app/#Manage-access-to-logs)
documentation. This documentation provides complete instructions on how to download logs from the Connected apps page in Atlassian Administration.
