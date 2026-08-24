# Configuring scheduled triggers to invoke a remote backend

You can configure [scheduled triggers](/platform/forge/manifest-reference/modules/scheduled-trigger/) to invoke your remote backend repeatedly on a scheduled interval.
Specify remote endpoints in your app’s manifest and Forge will automatically make requests to your remote with a [Forge Invocation Token](/platform/forge/remote/essentials/#the-forge-invocation-token--fit-) and an optional app access token.

## Getting started

To configure scheduled triggers that invoke your remote backend, in your `manifest.yml`:

1. Specify the `endpoint` your app will send remote requests to. This is done using the `endpoint` property of the `scheduledTrigger` module. Using `endpoint` rather than `function` tells Forge that your app will invoke a remote endpoint.
2. Define an `endpoint` item with a `key` matching the `endpoint` name you specified in the previous step.
   1. Set the `remote` property to the key that uniquely identifies the remote system the endpoint will communicate with.
   2. Set the `route.path` to the REST API operation path to be appended to the remote’s baseUrl, to invoke the desired REST API.
   3. If you want Forge to provide a system token, request it in the `auth` property.
   4. Add the relevant [scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-forge/) your app will need, for example Jira OAuth 2.0, Confluence OAuth 2.0, Storage scopes. If no additional scopes (in addition to read:app-user-token, read:app-system-token) are requested, a valid token will not be created
3. Define a `remotes` item with a key matching the remote name you specified in the endpoint, setting the baseUrl to the site URL prefix to prepend to the routes specified in your app's route.path.

### Example manifest

Below is an example `manifest.yml` configuring a scheduled trigger that invokes a remote endpoint at `/frc-trigger` every hour:

```
1modules:  
2  scheduledTrigger:
3    - key: remote-scheduled-trigger-node
4      endpoint: remote-trigger-node
5      interval: hour
6  endpoint:
7      - key: remote-trigger-node
8        remote: remote-app-node
9        route:
10          path: /frc-trigger
11        auth:
12          appSystemToken:
13            enabled: true
14permissions:
15  scopes:
16    - read:app-system-token    
17    - read:confluence-content:summary # relevant app scopes must be included when oauth tokens are enabled
18remotes:
19  - key: remote-app-node
20    baseUrl: https://forge-remote-refapp-nodejs.services.atlassian.com
21
```

## Token expiry and choosing an interval

When you request a system token in the endpoint's `auth` property, each scheduled trigger invocation includes an app system token in the `x-forge-oauth-system` header. This token is guaranteed to be valid for at least 2 hours; see [Token expiry](/platform/forge/remote/calling-product-apis/#token-expiry) for how tokens are cached, rotated, and validated using the `exp` claim.

The 2-hour minimum TTL guarantee only applies when the scheduled trigger **directly invokes a remote endpoint** (using the `endpoint` property in the manifest). If your scheduled trigger invokes a **Forge function** that then calls the remote via [`invokeRemote`](/platform/forge/runtime-reference/invoke-remote-api/), the token delivered to the remote does **not** respect the 2-hour minimum TTL and may have significantly less validity remaining. To ensure the guaranteed TTL, configure the scheduled trigger to invoke the remote endpoint directly rather than routing through a Forge function. See [Calling a remote backend from a Forge function](/platform/forge/remote/calling-from-function/) for more details on how tokens are handled in function-based invocations.

Scheduled triggers run without a user in session, so only the **app system token** is delivered. The app user token (`x-forge-oauth-user`) requires an active user and is **not** sent to scheduled trigger invocations. If your remote needs to act on behalf of a specific user offline, exchange the system token for a user token using [offline user impersonation](/platform/forge/remote/calling-product-apis/#offline-user-impersonation).

Choose an interval shorter than 2 hours so your remote always holds a valid token. The `hour` interval is a good default: the trigger fires several times within each token's guaranteed lifetime, so your remote always holds a token with plenty of remaining validity and gets multiple delivery attempts if an invocation is delayed or fails. Avoid relying on the `day` or `week` intervals as your only mechanism for refreshing tokens, since the token will expire well before the next invocation and your remote will be left without a valid token in between.

## Verifying requests

You will need to verify the requests received by your remote came from Atlassian and are intended for your app. For more information on how to do this, see [Verifying remote requests](/platform/forge/remote/essentials/#verifying-remote-requests).

## Next steps

Now that you’ve verified the requests and have received your access tokens, you can:
