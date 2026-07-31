# Forge changelog

**What's changing**  
Forge now supports offline impersonation for Jira Service Management (JSM) portal-only users. This follows our June 12, 2026 release of online impersonation support.

You can now use `asUser(accountId)` to make asynchronous or background API calls on behalf of portal-only users (also known as customer accounts). For apps using Forge remotes, offline impersonation is supported via the `offlineUserAuthToken` mutation.

This allows your apps to perform background actions, such as processing data or updating requests, in the context of the portal-only user, while maintaining the appropriate permission checks.

Note that portal-only users can only make `asUser()` calls to Jira/JSM APIs using corresponding scopes declared in the manifest file.

**What you need to do**  
To use offline impersonation for portal-only users in your app:

For more information on how Forge handles access for unlicensed users, see our [documentation](https://developer.atlassian.com/platform/forge/access-to-forge-apps-for-unlicensed-users/ "https://developer.atlassian.com/platform/forge/access-to-forge-apps-for-unlicensed-users/").
