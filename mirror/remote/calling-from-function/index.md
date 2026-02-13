# Calling a remote backend from a Forge function

You can call your remote backend from your Forge functions. The diagram below illustrates the data flow.

![Forge Remote diagram describing the flow of data and auth between Forge and remote application](https://dac-static.atlassian.com/platform/forge/images/remote/remote-calling-backend-from-frontend.png?_v=1.5800.1849)

Note: If you are calling your remote backend from a frontend function in a Forge app, see [Calling a remote backend from a Forge frontend](/platform/forge/remote/calling-from-frontend) instead.

## Getting started

To call your remote backend from a function you need to define a [remote](/platform/forge/manifest-reference/remotes) in your `manifest.yml`.

### Example manifest

Here's an example of how to set up your manifest:

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
modules:
  trigger:
    - key: update-issue
      function: main
      events:
        - avi:jira:updated:issue
  function:
    - key: main
      handler: index.run
remotes:
  - key: remote-app-node
    baseUrl: https://forge-remote-refapp-nodejs.services.atlassian.com
    operations:
      - compute
    auth:
      appSystemToken:
        enabled: true
```

## Calling your remote from a function

To call your remote from a function, you can use the [invokeRemote](/platform/forge/runtime-reference/invoke-remote-api/) method from the `@forge/api` package. This function allows you to make HTTP requests to your remote backend.

For example, a `GET` request to a remote endpoint could look like this:

```
```
1
2
```



```
import { invokeRemote } from "@forge/api";

const res = await invokeRemote('remote-app-node', {
  path: `/tasks/?team=Forge`,
  method: 'GET'
});

if (!res.ok) {
  throw new Error(`invokeRemote failed: ${res.status}`);
}

const json = await res.json();
console.log(`Tasks: ${JSON.stringify(json)}`);
```
```

## Verifying requests

You will need to verify the requests received by your remote came from Atlassian and are intended for your app. For more information on how to do this, see [Verifying remote requests](/platform/forge/remote/essentials/#verifying-remote-requests).

## Next steps

Now that you've verified the requests and have received your access tokens, you can:
