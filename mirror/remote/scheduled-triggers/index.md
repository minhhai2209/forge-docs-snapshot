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
   4. Add the relevant [scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-forge/) your app will need, for example Jira Oauth 2.0, Confluence Oauth 2.0, Storage scopes. If no additional scopes (in addition to read:app-user-token, read:app-system-token) are requested, a valid token will not be created
3. Define a `remotes` item with a key matching the remote name you specified in the endpoint, setting the baseUrl to the site URL prefix to prepend to the routes specified in your app's route.path.

### Example manifest

Below is an example `manifest.yml` containing a module that routes an event to `/frc-trigger` when a Confluence comment is added:

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
modules:  
  scheduledTrigger:
    - key: remote-scheduled-trigger-node
      endpoint: remote-trigger-node
      interval: hour
  endpoint:
      - key: remote-trigger-node
        remote: remote-app-node
        route:
          path: /frc-trigger
        auth:
          appSystemToken:
            enabled: true
permissions:
  scopes:
    - read:app-system-token    
    - read:confluence-content:summary # relevant app scopes must be included when oauth tokens are enabled
remotes:
remotes:
  - key: remote-app-node
    baseUrl: https://forge-remote-refapp-nodejs.services.atlassian.com
```

## Verifying requests

You will need to verify the requests received by your remote came from Atlassian and are intended for your app. For more information on how to do this, see [Verifying remote requests](/platform/forge/remote/essentials/#verifying-remote-requests).

## Next steps

Now that you’ve verified the requests and have received your access tokens, you can:
