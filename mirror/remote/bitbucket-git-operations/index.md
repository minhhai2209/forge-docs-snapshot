# Bitbucket git operations from a remote

Once your remote backend has received a request from Forge, you can use the app system token or app user token to
perform git operations over HTTPS against Bitbucket repositories.

## Prerequisites

When setting up your app to:

* call a remote (from a Custom UI or UI Kit 2 frontend)
* send Atlassian app and lifecycle events (to a remote)
* configure scheduled triggers to invoke a remote backend

You’ll need one of the following in your `manifest.yml`:

* `endpoint.auth.appSystemToken` set to `true`
* `endpoint.auth.appUserToken` set to `true`

Which one you need depends on whether you want to access Atlassian app APIs as a generic bot user (`appSystemToken`) or the current user's permission (`appUserToken`).

This ensures requests to your remote contain an `x-forge-oauth-system` or `x-forge-oauth-user` header, containing a token
you can use to perform git operations over HTTPS against Bitbucket repositories.

Your app must also request the `read:repository:bitbucket` scope for operations such as `git clone`, and the `write:repository:bitbucket` scope for `git push`.
This can be done by including them in the permissions section of your app's `manifest.yml` file.

### Token Expiry

Both of these tokens are encoded in JWT. The [`exp`](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.4) claim in their payload represents the expiration time.

* We recommend adding a [lifecycle events](/platform/forge/events-reference/life-cycle/#installation)
  trigger for the installation and upgrade events to ensure that your app starts off with a token available.
* If your app needs to ensure the access token is periodically refreshed, consider utilizing a [scheduled trigger](/platform/forge/remote/scheduled-triggers/).
  There is no endpoint for proactively refreshing the access token.
* As there is no lifecycle event sent upon app uninstallation yet ([FRGE-1246](https://ecosystem.atlassian.net/browse/FRGE-1246)),
  authentication failures from git operations may indicate the app is no longer installed on the tenant.
  You can infer the app was uninstalled if it stopped receiving a scheduled trigger.

## Getting started

Once you’ve got your token, you can use it as the basic auth credentials in the URL of the git over HTTPS operation, with `x-token-auth` as a substitute for username.

The git operation will fail if the app does not have the correct scope, or if the app or user does not have the appropriate permission to the repo.

Example:

Git clone using app system token as the credential:

```
```
1
2
```



```
git clone https://x-token-auth:{x-forge-oauth-system token}@bitbucket.org/{workspace}/{repository}.git
```
```

Git push using app user token as the credential:

```
```
1
2
```



```
git push --repo https://x-token-auth:{x-forge-oauth-user token}@bitbucket.org/{workspace}/{repository}.git
```
```

## Next steps

For further help, see how you can:
