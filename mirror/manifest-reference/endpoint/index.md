# Endpoint

The `endpoint` module type specifies properties of an endpoint such as its authorization, the key of the
`remote` that hosts the endpoint, and the route to that endpoint relative to the remote's base URL.

To implement custom functionality in your Forge app using a remote resolver, specify the endpoint key in the
`endpoint` property of the resolver object for the module.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the endpoint, which other modules can refer to. Must be unique within the list of endpoints and have a maximum of 23 characters.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `remote` | `string` | Yes (for `remotes`) | The remote key that defines the base portion of the path for this endpoint.  This is required if your endpoint is targeting a [Forge Remote](/platform/forge/remote/). |
| `service` (EAP) | `string` | Yes (for `services`) | The key of the containerised service that defines the base portion of this endpoint's path.  This is required if your endpoint is targeting a containerised service provisioned through [Forge Containers](/platform/forge/containers-reference/). |
| `route` | `{path:string}` | No | The path appended to the `baseUrl` property of the `remote` object when invoking this endpoint.  This property is only required for backend module endpoints.  UI module remote resolver endpoint paths are always specified in [invokeRemote](/platform/forge/apis-reference/ui-api-bridge/invokeRemote) requests in the app's front end. |
| `auth` | `object` | No | An object that defines the auth options available to the remote endpoint when calling Forge functions |
| `auth.appUserToken.enabled` | `boolean` | No | If `true` and the remote endpoint is invoked within a user's login session, Forge includes an `appUserToken` in the Forge Invocation Token it sends to the remote app.  This token can be used by the remote app when invoking an Atlassian app API, to invoke the API with the permissions of the user in whose login session the app is running.  Specifically, the API will have only as much access to the site's data as that user does. For example, if the user does not have permission to see pages in a particular space or issues in a particular project, the API won't provide them access to that space or page, either.  Forge modules that run outside of a user's login session, such as an app lifecycle event or product event are not associated with a user and cannot send an `appUserToken` to the remote app.  If an endpoint opts to enable remote user token access, the `read:app-user-token` scope must also be specified in the [Permissions](/platform/forge/manifest-reference/permissions) section of the manifest. |
| `auth.appSystemToken.enabled` | `boolean` | No | If `true`, Forge includes an `appSystemToken` in the Forge Invocation Token it sends to the remote app.  This token can be used by the remote app when invoking an Atlassian app API, to invoke the API with the permissions of the generic "bot user" for the app.  If an endpoint opts to enable remote system token access, the `read:app-system-token` scope must also be specified in the [Permissions](/platform/forge/manifest-reference/permissions) section of the manifest. |

Modifying the endpoint entries results in a major version upgrade of your app upon deploy. Your app users will again
be required to consent to your app's permissions.

## Example: Forge Remote

The following snippet provides a basic example of an endpoint targeting a Forge Remote service.

```
```
1
2
```



```
modules:
  scheduledTrigger:
    - key: remote-scheduled-trigger-boot
      endpoint: remote-trigger-boot
      interval: hour
  endpoint:
    - key: remote-trigger-boot
      remote: remote-app-node
      route:
        path: /forge-trigger
      auth:
        appUserToken:
          enabled: true
        appSystemToken:
          enabled: false
```
```

## Example: Forge Containers (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

The following snippet shows a service named `java-service`, which is backed by a container of the same name. The service is accessible via the `/webtrigger` route on the `webtrigger-ep` [endpoint module](/platform/forge/manifest-reference/endpoint/#endpoint).

```
```
1
2
```



```
modules:
  webtrigger:
    - key: container-webtrigger
      endpoint: webtrigger-ep
  endpoint:
    - key: webtrigger-ep
      service: java-service
      route:
        path: /webtrigger

services:
  - key: java-service
    containers:
      - key: java-service
        tag: latest
        resources:
          cpu: "1"
          memory: "2Gi"
        health:
          type: http
          route:
            path: "/healthcheck"
    scaling: 
      min: 1
      max: 1
```
```
