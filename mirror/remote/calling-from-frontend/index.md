# Calling a remote backend from a Forge frontend

You can call your remote backend from your frontend (Custom UI and UI Kit) via a resolver. The diagram below illustrates the data flow.

![Forge Remote diagram describing the flow of data and auth between Forge and remote application](https://dac-static.atlassian.com/platform/forge/images/remote/remote-calling-backend-from-frontend.png?_v=1.5800.1783)

## Getting started

To define a remote endpoint for a Forge module, in your `manifest.yml`:

1. Specify the `endpoint` your app will send remote requests to. For UI modules, this is done using the `resolver.endpoint` property of the module that will be making remote requests.
2. Define an `endpoint` item with a `key` matching the `endpoint` name you specified in the previous step.
   1. Set the `remote` property to the key that uniquely identifies the remote system the endpoint will communicate with.
   2. If you want Forge to provide system or user tokens, request them in the `auth` property.
   3. Add the relevant [scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-forge/) your app will need, for example Jira Oauth 2.0, Confluence Oauth 2.0, Storage scopes. If no additional scopes (in addition to read:app-user-token, read:app-system-token) are requested, a valid token will not be created
3. Define a `remotes` item with a key matching the remote name you specified in the endpoint, setting the baseUrl to the site URL prefix to prepend to the routes specified in your invokeRemote request.

### Example manifest

Here's an example of how to setup your manifest:

```
```
1
2
```



```
modules:
  macro:
    - key: forge-remote-app-node
      resource: main
      resolver:
        endpoint: remote-macro-node
      title: forge-remote-app-node
      description: Invokes a Forge Remote NodeJS Server and renders the result.
  endpoint:
    - key: remote-macro-node
      remote: remote-app-node
      auth:
        appUserToken:
          enabled: true
        appSystemToken:
          enabled: true 
resources:
  - key: main
    path: static/hello-remote-world/build
permissions:
  scopes:
    - read:app-system-token
    - read:app-user-token
    - read:confluence-content.summary # relevant app scopes must be included when oauth tokens are enabled
remotes:
  - key: remote-app-node
    baseUrl: https://forge-remote-refapp-nodejs.services.atlassian.com
```
```

## Verifying requests

You will need to verify the requests received by your remote came from Atlassian and are intended for your app. For more information on how to do this, see [Verifying remote requests](/platform/forge/remote/essentials/#verifying-remote-requests).

## Calling your remote from a Forge frontend

To call your remote from a Forge frontend, you can use the [invokeRemote](/platform/forge/apis-reference/ui-api-bridge/invokeRemote) or the [requestRemote](/platform/forge/apis-reference/ui-api-bridge/requestRemote) API from the `@forge/bridge` package. These APIs allows you to make HTTP requests to your remote backend.

For example, a `GET` request to a remote endpoint could look like this:

```
```
1
2
```



```
import { invokeRemote } from "@forge/bridge";

const res = await invokeRemote({
  path: `/tasks/?team=Forge`,
  method: 'GET'
});

console.log(`Tasks: ${JSON.stringify(res.body[0])}`);
```
```

## Atlassian app modules

To see a complete list of modules you can use to call your remote, including payload and context properties, see the Forge modules for each Atlassian app:

## Next steps

Now that you’ve verified the requests and have received your access tokens, you can:
