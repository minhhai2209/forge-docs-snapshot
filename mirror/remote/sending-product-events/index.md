# Sending Atlassian app and lifecycle events to a remote

You can configure [Atlassian app events](/platform/forge/events-reference/product_events) and [lifecycle events](/platform/forge/events-reference/life-cycle) to be delivered directly to your remote backend.
Specify remote endpoints in your app’s manifest and Forge will automatically route events along with a [Forge Invocation Token](/platform/forge/remote/essentials/#the-forge-invocation-token--fit-) and an optional app access token.

# Timeouts and asynchronous events

Given the high-volume nature of Forge events, remote invocations will have a timeout of 5 seconds. Your app needs to implement processing logic in an asynchronous fashion (for example, enqueuing events for a worker to process asynchronously). The diagram below illustrates such a solution.

![Forge Remote diagram describing the flow of events and auth between Forge and remote application, with an event queue setup on the remote app](https://dac-static.atlassian.com/platform/forge/images/remote/remote-events-diagram.png?_v=1.5800.1741)

## Getting started

To configure events to be delivered to your remote backend, in your `manifest.yml`:

1. Specify the `endpoint` your app will send remote requests to. This is done using the `endpoint` property of the `trigger` module defined for the event. Using `endpoint` rather than `function` tells Forge that your app will invoke your remote endpoint.
2. Define an `endpoint` item with a `key` matching the `endpoint` name you specified in the previous step.
   1. Set the `remote` property to the key that uniquely identifies the remote system the endpoint will communicate with.
   2. Set the `route.path` to the REST API operation path to be appended to the remote’s baseUrl, to invoke the desired REST API.
   3. If you want Forge to provide a system token, request it in the `auth` property.
3. Define a `remotes` item with a key matching the remote name you specified in the endpoint, setting the baseUrl to the site URL prefix to prepend to the routes specified in your app's route.path.

### Example manifest

Here’s an example `manifest.yml` of a module that routes an event to `/frc-event` when a Confluence comment is added:

```
```
1
2
```



```
modules:  
  trigger:
    - key: remote-comment-trigger-node
      endpoint: remote-events-node
      events:
        - avi:confluence:created:comment
  endpoint:
      - key: remote-events-node
        remote: remote-app-node
        route:
          path: /frc-event
        auth:
          appSystemToken:
            enabled: true
permissions:
  scopes:
    - read:app-system-token
    - read:confluence-content.summary         
remotes:
  - key: remote-app-node
    baseUrl: https://forge-remote-refapp-nodejs.services.atlassian.com
```
```

## Verifying requests

You will need to verify the requests received by your remote came from Atlassian and are intended for your app. For more information on how to do this, see [Verifying remote requests](/platform/forge/remote/essentials/#verifying-remote-requests).

## Handling retries

If the remote endpoint returns a non-2xx response or if the invocation times out when delivering an event to a remote endpoint (the timeout period for an event invocation is 5 seconds), redelivery will be attempted as described by the note regarding `retryOptions` below.
Information on the retry attempt will be provided in the `retryContext` property sent in the HTTP request body. For example:

```
```
1
2
```



```
{
  "payload": {
    ...
    "retryContext": {
      "retryData": null,
      "retryCount": 2,
      "retryReason": "INVALID_REMOTE_INVOCATION_ERROR"
    }
    ...
  }
}
```
```

See the developer documentation for [retrying Atlassian app events](/platform/forge/events-reference/product_events/#retry-product-events) for more information.
`retryOptions` cannot be set from remote invocations. By default:

* All remote Atlassian app event invocations will be retried with a delay of 60 seconds per request.
* Events will be retried up to a maximum of 4 attempts.
* `retryData` will always be `null`.
* `retryReason` can be the following:
  * `INVALID_REMOTE_INVOCATION_ERROR`
    General error. For example; the response from the remote server was non 2XX, the response did not follow the API contract defined in the Forge Remote Preview documentation or there was a network error.
  * `TIMEOUT_ERROR`
    The request timed out.
  * `INVALID_FORGE_INVOCATION_TOKEN`
    The invocation token could not be validated and the remote server responds with a 401.

## Atlassian app events

To see all the events that can be sent (including required scopes), see the events for each Atlassian app:

## Lifecycle events

To see what events your Forge app can subscribe to, see [Lifecycle events](/platform/forge/events-reference/life-cycle/).

## Next steps

Now that you’ve verified the requests and have received your access tokens, you can:
