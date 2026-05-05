# Forge Containers reference: API contract (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Forge Containers uses a *sidecar* service to act as a proxy and handle your containerised service’s inbound and outbound requests. This sidecar authenticates invocation requests to your service.

## Inbound requests

Forge adds the following headers to requests sent to your containerised service’s REST API:

| **Header** | **Description** |
| --- | --- |
| `x-b3-traceid` | Indicates the overall ID of the trace. Every span in a trace shares this ID. |
| `x-b3-spanid` | Indicates the position of the current operation in the trace tree. The value should not be interpreted: it may or may not be derived from the value of the TraceId. |
| `x-forge-invocation-id` | A unique ID for an invocation, which you can use to attach context from the invocation to an [outbound request](#outbound-requests) (including authentication). |
| `x-forge-invocation-log-attributes` | An opaque string of log-related metadata (encoded in `base64`). This should be added to JSON-structured logs with a `forge_invocation` key to [improve the log filtering experience](/platform/forge/containers-reference/ref-logging/#invocation-metadata) in the Developer Console. |

## Outbound requests

Your app’s containerised service can send requests to the REST APIs of:

In order to make outbound requests from your container you will need to send requests via the egress sidecar.
The URL to communicate with the egress sidecar can be retrieved from the `FORGE_EGRESS_PROXY_URL` environment variable.
Requests to the egress sidecar must contain a `forge-proxy-authorization` header with the following information:

| **Field** | **Required?** | **Description** |
| --- | --- | --- |
| `id` | Yes (The request must include either `installationId` or `id`) | An invocation ID that provides the context and authentication for this request (namely, `x-forge-invocation-id` from a corresponding [inbound request](#inbound-requests)). |
| `installationId` | An installation ID that provides the context and authentication for this request (see [Call a containerised service without an invocationId](/platform/forge/containers-reference/int-installbased/) for more details). |
| `as=<user|app>` | No | Specifies whether to call the API using either the app or its user as its context. |
| `accountId=<accountId>` | No | Specify an accountId to make a request using offline user impersonation. The `as` field must be set to user. See [Offline user impersonation](/platform/forge/remote/calling-product-apis/#offline-user-impersonation) for more information. |

For example:

```
```
1
2
```



```
GET <FORGE_EGRESS_PROXY_URL>/jira/<path>
  -H forge-proxy-authorization: Forge as=<user|app>,id=<x-forge-invocation-id>,accountId=<accountId>
```
```

To fetch information on a Forge Invocation Context you can call the following API:

```
```
1
2
```



```
GET <FORGE_EGRESS_PROXY_URL>/invocation/context
  -H forge-proxy-authorization: Forge id=<x-forge-invocation-id>
```
```

All `@forge/*` packages are *not currently supported* in Forge Containers, including:

## Environment Variables

When your container is started it will be injected with the following environment variables:

| **Variable** | **Description** |
| --- | --- |
| `SERVER_PORT` | The port at which the container service should listen for incoming requests.  For example:   `8080` |
| `FORGE_APP_ARI` | A unique Atlassian resource identifier (`ari`) assigned to your app. The Forge CLI supplies this identifier when you [create](/platform/forge/cli-reference/create/) or [register](/platform/forge/cli-reference/register/) an app for the first time. For example:`ari:cloud:ecosystem::app/d60dfafb-a14d-4d56-bf03-0c3823d39e2b` |
| `FORGE_CONTAINER_KEY` | The key of the container, which is the value of the `services:container:key` field in the Forge manifest.  For example:   `java-service` |
| `FORGE_EGRESS_PROXY_URL` | The URL to the Forge Containers sidecar service. For example: `http://localhost:7072` |
| `FORGE_ENV_ARI` | A unique Atlassian resource identifier (`ari`) assigned to your app environment.  For example:   `ari:cloud:ecosystem::environment/d60dfafb-a14d-4d56-bf03-0c3823d39e2b/d67ce878-3e91-404b-b523-9e1d9bf867d5` |
| `FORGE_IMAGE_TAG` | The tag of the image that is currently running.  For example:   `1.0.0` |
| `FORGE_SERVICE_KEY` | The key of the service, which is the value of the `services:key` field in the Forge manifest.  For example:   `java-service` |

When running `forge deploy`, all environment variables set through the `forge variables set` [command](/platform/forge/cli-reference/variables-set/) will also be injected into the container.
