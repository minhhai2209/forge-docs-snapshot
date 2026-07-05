# Forge changelog

We've added a new Forge module (`devops:securityInfoProvider`) that lets your app send security information (such as vulnerabilities and security containers) to Jira and associate it with issues. This is now available in **preview**.

**What's new**

The `devops:securityInfoProvider` module surfaces your app's security data directly in the development panel of Jira issues. Apps can write and delete security information using the <https://developer.atlassian.com/cloud/jira/software/rest/> via the `requestJira` function.

To register a provider, declare the module in your `manifest.yml` and configure the required endpoint handlers:

* `fetchWorkspaces`: returns the list of workspaces available to the user
* `fetchContainers`: returns security containers within a workspace
* `searchContainers`: searches containers matching a query

Two optional lifecycle hooks are also available: `onEntityAssociated` and `onEntityDisassociated`, invoked when a container is linked or unlinked from a Jira entity.

**Important behaviour to note**

When a user uninstalls your app, all security data your app sent to Jira is deleted after a grace period.

There is currently a limitation, where your Forge app must define a Connect app key in order to be able to link workspaces. See [https://jira.atlassian.com/browse/ECO-1602](https://jira.atlassian.com/browse/ECO-1602 "https://jira.atlassian.com/browse/ECO-1602")

**Get started**

See the <https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-software-security-info/> for the full manifest schema, example requests/responses, and property details.
